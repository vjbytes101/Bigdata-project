import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(parks_nm):
	if parks_nm is "" or parks_nm is " ":
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
    col_cat = data.map(lambda x: (x[0],x[17]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],"VALID"))
	#parks_nm_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	parks_nm_valid = col_cat1.map(lambda x: str(x[0]) + "\t" + str(x[1]))
	colName = sc.parallelize(["CMPLNT_NUM \t PARKS_NM"])
	sc.union([colName, parks_nm_valid]).saveAsTextFile("/Output/Cleaning/col17/PARKS_NM_VALID.out")
	#park_nm_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	#park_nm_invalid = park_nm_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    #sc.union([colName, park_nm_invalid]).saveAsTextFile("/Output/Cleaning/col17/PARKS_NM_INVALID.out")
    sc.stop()