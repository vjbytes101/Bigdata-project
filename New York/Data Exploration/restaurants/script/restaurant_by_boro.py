import sys
from pyspark import SparkContext, SparkConf
from csv import reader
from itertools import islice
from operator import add


if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/Pre-Permit-Restaurant-Inspections.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
	restaurants = data.map(lambda x: (x[0], x[2])).reduceByKey(lambda a, b: a)
	restaurants = restaurants.map(lambda x: (x[1], 1)).reduceByKey(add).sortByKey()
	restaurants.saveAsTextFile("/Output/new_restaurants_by_boro.csv")
    sc.stop()