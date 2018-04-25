import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import re

def checker(addr_cd):
	if addr_cd is "" or addr_cd is " ":
		return ("INVALID")
	elif re.match('[0-9]+',addr_cd):
		return("VALID")
	else:
		return("INVALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[0],x[14]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	addr_cd_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	addr_cd_valid = addr_cd_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t ADDR_PCT_CD"])
	sc.union([colName, addr_cd_valid]).saveAsTextFile("/Output/Cleaning/col14/ADDR_CD_VALID.out")
	addr_cd_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	addr_cd_invalid = addr_cd_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, addr_cd_invalid]).saveAsTextFile("/Output/Cleaning/col14/ADDR_CD_INVALID.out")
    sc.stop()