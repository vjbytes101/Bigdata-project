import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView('crime')
result = spark.sql("Select LOC_OF_OCCUR_DESC as cmpt_cd, count(LOC_OF_OCCUR_DESC) as crime_count from crime group by LOC_OF_OCCUR_DESC")
result.select(format_string('%s\t%d', result.cmpt_cd,result.crime_count)).write.save("/Output/Analysis/crime_location.csv",format="csv")