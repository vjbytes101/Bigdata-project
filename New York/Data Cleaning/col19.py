import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import math

def checker(x_coord):
	if x_coord == "" or x_coord == " " or x_coord =="\t":
		return ("INVALID")
	try:
		x_coord = float(x_coord.replace(",", ""))
		if x_coord >= 909900 and x_coord <= 1067600:
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
    col_cat = data.map(lambda x: (x[0],x[19]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	x_coord_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	x_coord_valid = x_coord_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t X_COORD_CD"])
	sc.union([colName, x_coord_valid]).saveAsTextFile("/Output/Cleaning/col19/X_COORD_VALID.out")
	x_coord_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	x_coord_invalid = x_coord_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, x_coord_invalid]).saveAsTextFile("/Output/Cleaning/col19/X_COORD_INVALID.out")
    sc.stop()