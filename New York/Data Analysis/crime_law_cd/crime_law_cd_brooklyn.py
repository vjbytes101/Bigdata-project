import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView('crime')
result = spark.sql("Select LAW_CAT_CD as lawcd,count(LAW_CAT_CD) as crime_count from crime where BORO_NM = 'BROOKLYN' group by LAW_CAT_CD")
result.select(format_string('%s\t%d', result.lawcd,result.crime_count)).write.save("/Output/Analysis/crime_by_law_cd_brooklyn.csv",format="csv")