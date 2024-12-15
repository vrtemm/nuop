# Імпортуємо необхідні бібліотеки
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator
import matplotlib.pyplot as plt
import seaborn as sns

# Створення Spark-сесії
spark = SparkSession.builder.appName("DisasterAnalysis").getOrCreate()

# Завантаження даних з CSV
df = spark.read.csv("path_to_emdat.csv", header=True, inferSchema=True)

# Перегляд перших 5 рядків для ознайомлення з даними
df.show(5)

# Очищення даних
# Перетворення стовпця "Date" в правильний формат дати
df = df.withColumn("Date", to_date(df["Date"], "yyyy-MM-dd"))

# Видалення рядків з пропущеними значеннями
df_cleaned = df.dropna()

# Вибір характеристик для аналізу
selected_columns = ['Disaster_Type', 'Date', 'Country', 'Fatalities', 'Economic_Losses', 'Total_Affected']
df_selected = df_cleaned.select(selected_columns)

# Статистика для вибірки
df_selected.describe().show()

# Аналіз типів катастроф і їх вплив на кількість жертв
disaster_fatalities = df_selected.groupBy("Disaster_Type").agg({"Fatalities": "sum"}).withColumnRenamed("sum(Fatalities)", "Total_Fatalities")
disaster_fatalities.show()

# Візуалізація
disaster_fatalities_pd = disaster_fatalities.toPandas()
plt.figure(figsize=(10,6))
sns.barplot(x="Disaster_Type", y="Total_Fatalities", data=disaster_fatalities_pd)
plt.xticks(rotation=90)
plt.title("Total Fatalities by Disaster Type")
plt.xlabel("Disaster Type")
plt.ylabel("Total Fatalities")
plt.show()

# Питання 2: Географічний аналіз: найбільш постраждалі країни
country_fatalities = df_selected.groupBy("Country").agg({"Fatalities": "sum"}).withColumnRenamed("sum(Fatalities)", "Total_Fatalities")
country_fatalities = country_fatalities.orderBy(col("Total_Fatalities").desc())
country_fatalities.show(10)

# Візуалізація найбільш постраждалих країн
country_fatalities_pd = country_fatalities.toPandas()
plt.figure(figsize=(10,6))
sns.barplot(x="Country", y="Total_Fatalities", data=country_fatalities_pd.head(10))
plt.xticks(rotation=90)
plt.title("Top 10 Countries by Total Fatalities")
plt.xlabel("Country")
plt.ylabel("Total Fatalities")
plt.show()

# Питання 3: Прогнозування економічних збитків з використанням регресії
# Вибір важливих характеристик для побудови моделі
df_features = df_selected.select("Fatalities", "Economic_Losses", "Total_Affected")

# Перевірка на пропущені значення
df_features = df_features.dropna()

# Підготовка до побудови моделі: створення векторів ознак
assembler = VectorAssembler(inputCols=["Fatalities", "Total_Affected"], outputCol="features")
df_assembled = assembler.transform(df_features)

# Побудова моделі: Random Forest регресія для прогнозування економічних збитків
rf = RandomForestRegressor(labelCol="Economic_Losses", featuresCol="features", numTrees=50)
model = rf.fit(df_assembled)

# Прогнозування
predictions = model.transform(df_assembled)

# Оцінка моделі: RMSE
evaluator = RegressionEvaluator(labelCol="Economic_Losses", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE): {rmse}")

# Візуалізація прогнозів
predictions_pd = predictions.select("Economic_Losses", "prediction").toPandas()
plt.figure(figsize=(10,6))
sns.scatterplot(x="Economic_Losses", y="prediction", data=predictions_pd)
plt.title("Actual vs Predicted Economic Losses")
plt.xlabel("Actual Economic Losses")
plt.ylabel("Predicted Economic Losses")
plt.show()

# Завершення роботи зі Spark
spark.stop()