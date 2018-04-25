import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(desc_ky):

	if desc_ky is "" or desc_ky is " ":
		return ("INVALID")
	else :
		return ("VALID")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	header = data.first()#Will extract header
    data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))
    col_cat = data.map(lambda x: (x[0],x[9]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	pd_desc_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	pd_desc_valid = pd_desc_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t PD_DESC"])
	sc.union([colName, pd_desc_valid]).saveAsTextFile("/Output/Cleaning/col9/PD_DESC_VALID.out")
	pd_desc_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	pd_desc_invalid = pd_desc_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, pd_desc_invalid]).saveAsTextFile("/Output/Cleaning/col9/PD_DESC_INVALID.out")
    sc.stop()