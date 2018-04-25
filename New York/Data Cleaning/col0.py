import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import re

def checker(complaint_num):

	if complaint_num is "" or complaint_num is " ":
		return (complaint_num,"NULL")
	elif re.match('[1-9][0-9]+',complaint_num):
		return(complaint_num,"VALID")
	else :
		return (complaint_num,"INVALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: x[0])
    col_cat1 = col_cat.map(lambda x: checker(x))
    col_cat2 = col_cat1.map(lambda x: (x[1], 1)).reduceByKey(lambda a,b : a+b)
    col_cat1.saveAsTextFile("/Output/CMPLNT_NUM_CATEGORY.out")
	col_cat2.saveAsTextFile("/Output/CMPLNT_NUM_COUNT.out")
    sc.stop()