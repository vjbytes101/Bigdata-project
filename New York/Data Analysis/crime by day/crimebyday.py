import sys
from pyspark import SparkContext, SparkConf
from csv import reader
from operator import add
from datetime import datetime as dt

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[5]))
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    col_cat1 = col_cat.map(lambda x: x[1]).map(lambda x: dt.strptime(x, '%m/%d/%Y'))
	col = col_cat1.map(lambda x: x.date().weekday()).map(lambda x: (x, 1))
    col_count = col.reduceByKey(lambda x,y: x+y)
    col_map = col_count.map(lambda x: weekdays[x[0]] + "," + str(x[1]))
    col_map.saveAsTextFile("/Output/Analysis/crime_by_days.csv")
    sc.stop()