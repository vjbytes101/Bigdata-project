import sys
from pyspark import SparkContext, SparkConf
from csv import reader

def checker(crm_cd):
	if crm_cd is "" or crm_cd is " ":
		return ("INVALID")
	else :
		ind = ["SUCCESSFULLY COMPLETED", "COMPLETED", "ATTEMPTED", "FAILED", "INTERRUPTED PREMATURELY"]
	if crm_cd not in ind:
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
    col_cat = data.map(lambda x: (x[0],x[10]))
    col_cat1 = col_cat.map(lambda x: (x[0],x[1],checker(x[1])))
	crm_valid = col_cat1.filter(lambda x: (x[2] == 'VALID'))
	crm_valid = crm_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t CRM_ATPT_CPTD_CD"])
	sc.union([colName, crm_valid]).saveAsTextFile("/Output/Cleaning/col10/CRM_VALID.out")
	crm_invalid = col_cat1.filter(lambda x: (x[2] == 'INVALID'))
	crm_invalid = crm_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
    sc.union([colName, crm_invalid]).saveAsTextFile("/Output/Cleaning/col10/CRM_INVALID.out")
    sc.stop()