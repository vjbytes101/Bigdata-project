import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView('crime')
result = spark.sql("Select OFNS_DESC as ofns,count(OFNS_DESC) as count_val from crime where BORO_NM = 'MANHATTAN' group by OFNS_DESC ORDER BY count(OFNS_DESC) desc limit 10")
result.select(format_string('%s\t%d', result.ofns,result.count_val)).write.save("/Output/Analysis/crime_by_type_manhattan.csv",format="csv")