import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import math

def checker(latitude):
	if latitude == "" or latitude == " " or latitude =="\t":
		return ("INVALID")
	try:
		latitude = float(latitude.replace(",", ""))
		if latitude > 40 and latitude < 41:
			return ("VALID")
		else:
			return("INVALID")
	except:
		return("INVALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[0],x[21]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	latitude_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	latitude_valid = latitude_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t Latitude"])
	sc.union([colName, latitude_valid]).saveAsTextFile("/Output/Cleaning/col21/LATITUDE_VALID.out")
	latitude_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	latitude_invalid = latitude_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, latitude_invalid]).saveAsTextFile("/Output/Cleaning/col21/LATITUDE_INVALID.out")
    sc.stop()