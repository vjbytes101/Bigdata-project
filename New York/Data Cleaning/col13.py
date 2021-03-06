import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(boro_nm):
	if boro_nm is "" or boro_nm is " ":
		return ("INVALID")
	else :
		ind = ["BRONX","BROOKLYN","MANHATTAN","QUEENS","STATEN ISLAND"]
	if boro_nm not in ind:
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
    col_cat = data.map(lambda x: (x[0],x[13]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	boro_nm_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	boro_nm_valid = boro_nm_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t BORO_NM"])
	sc.union([colName, boro_nm_valid]).saveAsTextFile("/Output/Cleaning/col13/BORO_NM_VALID.out")
	boro_nm_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	boro_nm_invalid = boro_nm_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, boro_nm_invalid]).saveAsTextFile("/Output/Cleaning/col13/BORO_NM_INVALID.out")
    sc.stop()