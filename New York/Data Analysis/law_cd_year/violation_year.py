import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
temp = df_parking.withColumn("tx_date", to_date(unix_timestamp(df_parking['RPT_DT'], "mm/dd/yyyy").cast("timestamp")))
df=temp
df.createOrReplaceTempView("df")
result = spark.sql("Select year(tx_date) as year_val,count(LAW_CAT_CD) as crime_count from df where tx_date !='tx_date' and LAW_CAT_CD ='VIOLATION' group by year(tx_date) ORDER BY year(tx_date)")
result.select(format_string('%s\t%d', result.year_val,result.crime_count)).write.save("/Output/Analysis/crime_by_violation_year.csv",format="csv")