import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView('crime')
result = spark.sql("Select ADDR_PCT_CD as cmpt_cd, count(ADDR_PCT_CD) as crime_count from crime where BORO_NM = 'BRONX' group by ADDR_PCT_CD")
result.select(format_string('%s\t%d', result.cmpt_cd,result.crime_count)).write.save("/Output/Analysis/crime_by_prec_bronx.csv",format="csv")