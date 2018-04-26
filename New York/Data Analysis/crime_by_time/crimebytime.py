import sys
from pyspark import SparkContext, SparkConf
from csv import reader
from operator import add
from datetime import datetime as dt

def convert_to_type(x):
	if x in range(4, 12):
		return "morning"
	elif x in range(12, 17):
		return "afternoon"
	elif x in range(17, 21):
		return "evening"
	else:
		return "night"

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[5]))
    col_cat1 = col.map(lambda x: x[1]).map(lambda x: dt.strptime(x, '%H:%M:%S'))
	col = col_cat1..map(lambda x: convert_to_type(x.hour)).map(lambda x: (x, 1))
    col_count = col.reduceByKey(lambda x,y: x+y)
    col_map = col_count.map(lambda x: str(x[0]) + "," + str(x[1]))
    col_map.saveAsTextFile("/Output/Analysis/crime_by_time.csv")
    sc.stop()