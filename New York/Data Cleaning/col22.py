import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import math

def checker(Longitude):
	if Longitude == "" or Longitude == " " or Longitude =="\t":
		return ("INVALID")
	try:
		Longitude = float(Longitude.replace(",", ""))
		if Longitude > -75 and Longitude < -73:
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
    col_cat = data.map(lambda x: (x[0],x[22]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	Longitude_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	Longitude_valid = Longitude_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t Longitude"])
	sc.union([colName, Longitude_valid]).saveAsTextFile("/Output/Cleaning/col22/LONGITUDE_VALID.out")
	Longitude_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	Longitude_invalid = Longitude_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, Longitude_invalid]).saveAsTextFile("/Output/Cleaning/col22/LONGITUDE_INVALID.out")
    sc.stop()