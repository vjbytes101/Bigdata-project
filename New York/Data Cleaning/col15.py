import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(loc_desc):
	if loc_desc is "" or loc_desc is " ":
		return ("INVALID")
	else :
		ind = ["INSIDE", "OUTSIDE", "FRONT OF", "OPPOSITE OF", "REAR OF"]
	if loc_desc not in ind:
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
    col_cat = data.map(lambda x: (x[0],x[15]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	loc_desc_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	loc_desc_valid = loc_desc_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t LOC_OF_OCCUR_DESC"])
	sc.union([colName, loc_desc_valid]).saveAsTextFile("/Output/Cleaning/col15/LOC_DESC_VALID.out")
	loc_desc_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	loc_desc_invalid = loc_desc_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, loc_desc_invalid]).saveAsTextFile("/Output/Cleaning/col15/LOC_DESC_INVALID.out")
    sc.stop()