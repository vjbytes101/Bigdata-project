import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
temp = df_parking.withColumn("tx_date", to_date(unix_timestamp(df_parking['RPT_DT'], "MM/dd/yyyy").cast("timestamp")))
df=temp
df.createOrReplaceTempView("df")
result = spark.sql("Select month(tx_date) as month_val, count(month(tx_date)) as count_val from df where tx_date !='tx_date' group by month(tx_date) ORDER BY month(tx_date)")
result.select(format_string('%s\t%d', result.month_val,result.count_val)).write.save("/Output/Analysis/crime_by_month.csv",format="csv")