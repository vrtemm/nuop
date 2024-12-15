from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col, sum
import matplotlib.pyplot as plt
import seaborn as sns

# Create Spark session
spark = SparkSession.builder.appName("DisasterAnalysis").getOrCreate()

# Load CSV into Spark DataFrame
file_path = "/content/drive/My Drive/Colab Notebooks/public_emdat.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Check columns and display first rows
print("Column Names:", df.columns)
df.show(5)

# Select key columns for analysis
selected_columns = ['Disaster Type', 'Country', 'Start Year', 'Total Deaths', 'Total Affected', 'Total Damage (\'000 US$)']
df_selected = df.select([col(c) for c in selected_columns])

# Drop rows with missing values
df_cleaned = df_selected.dropna()

# Analyze total deaths by disaster type
disaster_fatalities = df_cleaned.groupBy("Disaster Type").agg(sum("Total Deaths").alias("Total_Fatalities"))
disaster_fatalities.show()

# Visualization: Total fatalities by disaster type
disaster_fatalities_pd = disaster_fatalities.toPandas()
plt.figure(figsize=(10, 6))
sns.barplot(x="Disaster Type", y="Total_Fatalities", data=disaster_fatalities_pd)
plt.xticks(rotation=90)
plt.title("Total Fatalities by Disaster Type")
plt.xlabel("Disaster Type")
plt.ylabel("Total Fatalities")
plt.show()

# Analyze most affected countries
country_impact = df_cleaned.groupBy("Country").agg(sum("Total Affected").alias("Total_Affected"))
country_impact = country_impact.orderBy(col("Total_Affected").desc())
country_impact.show(10)

# Visualization: Top 10 most affected countries
country_impact_pd = country_impact.toPandas()
plt.figure(figsize=(10, 6))
sns.barplot(x="Country", y="Total_Affected", data=country_impact_pd.head(10))
plt.xticks(rotation=90)
plt.title("Top 10 Most Affected Countries")
plt.xlabel("Country")
plt.ylabel("Total Affected")
plt.show()

# Stop Spark session
spark.stop()
