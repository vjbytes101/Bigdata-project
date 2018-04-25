import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import time
import re
import string

def time_checker(cmt_time):

	if cmt_time is "" or cmt_time is " ":
		return ("INVALID")
	else :
		time_x = cmt_time
		try:
			if time.strptime(cmt_time,"%H:%M:%S"):
				mat_res=re.match('([01][0-9]|2[0-3]|0?[1-9]):([0-5][0-9]|0?[1-9]):([0-5][0-9]|0?[1-9])$', cmt_time)
				if mat_res:
					return("VALID")
				else:
					return( "INVALID")
		except:
			return( "INVALID")


if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	#Header Extraction
	header = data.first()
	data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))

	#filtering on CMPLNT_FR_TM
    col_frmtime = data.map(lambda x: (x[0],x[2]))
	col_frmtime = col_frmtime.map(lambda x: (x[0],x[1],time_checker(x[1])))
	col_fromtime_valid = col_frmtime.filter(lambda x: (x[2] == 'VALID'))
	col_fromtime_valid = col_fromtime_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t CMPLNT_FR_TM"])
	sc.union([colName, col_fromtime_valid]).saveAsTextFile("/Output/Cleaning/col2/CMPLNT_TIME_FROM_VALID.out")
	col_fromtime_invalid = col_frmtime.filter(lambda x: (x[2] == 'INVALID'))
	col_fromtime_invalid = col_fromtime_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	sc.union([colName, col_fromtime_invalid]).saveAsTextFile("/Output/Cleaning/col2/CMPLNT_TIME_FROM_INVALID.out")

	#filtering on CMPLNT_TO_TM
	col_totime = data.map(lambda x: (x[0],x[4]))
	col_totime = col_totime.map(lambda x: (x[0],x[1],time_checker(x[1])))
	col_totime_valid = col_totime.filter(lambda x: (x[2] == 'VALID'))
	col_totime_valid = col_totime_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t CMPLNT_TO_TM"])
	sc.union([colName, col_totime_valid]).saveAsTextFile("/Output/Cleaning/col4/CMPLNT_TIME_TO_VALID.out")
	col_totime_invalid = col_totime.filter(lambda x: (x[2] == 'INVALID'))
	col_totime_invalid = col_totime_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	sc.union([colName, col_totime_invalid]).saveAsTextFile("/Output/Cleaning/col4/CMPLNT_TIME_TO_INVALID.out")

    sc.stop()