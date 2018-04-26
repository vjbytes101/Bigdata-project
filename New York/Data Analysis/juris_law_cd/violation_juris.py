import sys
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession.builder.appName("Python Spark SQL basic example").config("spark.some.config.option", "some-value").getOrCreate()
df_parking = spark.read.format("csv").option("header", "true").load("/user/edureka_123073/result.csv")
df_parking.createOrReplaceTempView('crime')
result = spark.sql("Select JURIS_DESC as cmpt_cd,LAW_CAT_CD as law_cd, count(JURIS_DESC) as crime_count from crime where LAW_CAT_CD = 'VIOLATION' group by JURIS_DESC,LAW_CAT_CD")
result.select(format_string('%s\t%s\t%d', result.cmpt_cd,result.law_cd,result.crime_count)).write.save("/Output/Analysis/crime_by_juris_violation.csv",format="csv")