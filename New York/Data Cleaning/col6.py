import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import re

def checker(ky_cd):

	if ky_cd is "" or ky_cd is " ":
		return ("INVALID")
	elif re.match('[1-9][0-9][0-9]',ky_cd):
		return ("VALID")
	else :
		return ("INVALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat =  data.map(lambda x: (x[0],x[6]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	key_cd_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	key_cd_valid = key_cd_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t KY_CD"])
	sc.union([colName, key_cd_valid]).saveAsTextFile("/Output/Cleaning/col6/KEY_CD_VALID.out")
	key_cd_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	key_cd_invalid = key_cd_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, key_cd_invalid]).saveAsTextFile("/Output/Cleaning/col6/KEY_CD_INVALID.out")
    sc.stop()