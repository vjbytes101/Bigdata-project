import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(juris_desc):
	if juris_desc is "" or juris_desc is " ":
		return ("INVALID")
	else :
		invalidval = ["OTHER"]
	if juris_desc in invalidval:
		return ("INVALID")
	else:
		return("VALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[0],x[12]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	jusris_desc_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	jusris_desc_valid = jusris_desc_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t JURIS_DESC"])
	sc.union([colName, jusris_desc_valid]).saveAsTextFile("/Output/Cleaning/col12/JURIS_DESC_VALID.out")
	jusris_desc_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	jusris_desc_invalid = jusris_desc_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, jusris_desc_invalid]).saveAsTextFile("/Output/Cleaning/col12/JURIS_DESC_INVALID.out")
    sc.stop()