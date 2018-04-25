import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import math

def checker(y_coord):
	if y_coord == "" or y_coord == " " or y_coord =="\t":
		return ("INVALID")
	try:
		y_coord = float(y_coord.replace(",", ""))
		if y_coord >= 117500 and y_coord <= 275000:
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
    col_cat = data.map(lambda x: (x[0],x[20]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	y_coord_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	y_coord_valid = y_coord_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t Y_COORD_CD"])
	sc.union([colName, y_coord_valid]).saveAsTextFile("/Output/Cleaning/col20/Y_COORD_VALID.out")
	y_coord_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	y_coord_invalid = y_coord_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, y_coord_invalid]).saveAsTextFile("/Output/Cleaning/col20/Y_COORD_INVALID.out")
    sc.stop()