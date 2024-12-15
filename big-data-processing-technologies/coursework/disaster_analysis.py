from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col, sum
import matplotlib.pyplot as plt
import seaborn as sns

# Створення Spark-сесії
spark = SparkSession.builder.appName("DisasterAnalysis").getOrCreate()

# Завантаження CSV у Spark DataFrame
file_path = "/content/drive/My Drive/Colab Notebooks/public_emdat.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Перевірка стовпців
print("Column Names:", df.columns)
df.show(5)

# Вибір основних стовпців для аналізу
selected_columns = ['Disaster Type', 'Country', 'Start Year', 'Total Deaths', 'Total Affected', 'Total Damage (\'000 US$)']
df_selected = df.select([col(c) for c in selected_columns])

# Видалення рядків з пропущеними значеннями
df_cleaned = df_selected.dropna()

# Аналіз типів катастроф і кількості жертв
disaster_fatalities = df_cleaned.groupBy("Disaster Type").agg(sum("Total Deaths").alias("Total_Fatalities"))
disaster_fatalities.show()

# Візуалізація: Загальна кількість жертв за типами катастроф
disaster_fatalities_pd = disaster_fatalities.toPandas()
plt.figure(figsize=(10, 6))
sns.barplot(x="Disaster Type", y="Total_Fatalities", data=disaster_fatalities_pd)
plt.xticks(rotation=90)
plt.title("Total Fatalities by Disaster Type")
plt.xlabel("Disaster Type")
plt.ylabel("Total Fatalities")
plt.show()

# Аналіз найбільш постраждалих країн
country_impact = df_cleaned.groupBy("Country").agg(sum("Total Affected").alias("Total_Affected"))
country_impact = country_impact.orderBy(col("Total_Affected").desc())
country_impact.show(10)

# Візуалізація: Топ-10 найбільш постраждалих країн
country_impact_pd = country_impact.toPandas()
plt.figure(figsize=(10, 6))
sns.barplot(x="Country", y="Total_Affected", data=country_impact_pd.head(10))
plt.xticks(rotation=90)
plt.title("Top 10 Most Affected Countries")
plt.xlabel("Country")
plt.ylabel("Total Affected")
plt.show()

# Завершення роботи зі Spark
spark.stop()
