import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView("crime")
result = spark.sql("Select PARKS_NM as park_nm, count(PARKS_NM) as crime_count from crime where BORO_NM = 'QUEENS' group by PARKS_NM ORDER BY count(PARKS_NM) ASC limit 6")
result.select(format_string('%s\t%d', result.park_nm,result.crime_count)).write.save("/Output/Analysis/safe_park_queens.csv",format="csv")