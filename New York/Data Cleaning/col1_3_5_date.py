import sys
from pyspark import SparkContext, SparkConf
from csv import reader
import datetime

def checker(cmt_date):

	if cmt_date is "" or cmt_date is " ":
		return ("INVALID")
	else :
		date = cmt_date
		cmt_date = cmt_date.split("/")
		try:
			month = int(cmt_date[0])
			day = int(cmt_date[1])
			year = int(cmt_date[2])
			
			if year >= 2006 and year <= 2017:
				return("VALID")
			else:
				return( "INVALID")
		except:
			return( "INVALID")

def date_checker(x_date):
	CMPLNT_FR_DT = x_date[0]
	CMPLNT_TO_DT = x_date[1]
	if CMPLNT_FR_DT.strip() and not CMPLNT_TO_DT.strip():
		return("PERFECT")
	elif not CMPLNT_FR_DT.strip() and CMPLNT_TO_DT.strip():
		return("ENDDATE")
	elif not CMPLNT_FR_DT.strip() and not CMPLNT_TO_DT.strip():
		return("INVALID")
	else:
		return("TIMERANGE")

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	data = sc.textFile('/user/edureka_123073/NYPD_Complaint_Data_Historic.csv')
	#Header Extraction
	header = data.first()
	data = data.filter(lambda x: x != header)
    data = data.mapPartitions(lambda x: reader(x))

	#filtering on CMPLNT_FR_DT
    col_frmdate = data.map(lambda x: (x[0],x[1]))
	col_frmdate = col_frmdate.map(lambda x: (x[0],x[1],checker(x[1])))
	col_fromdate_valid = col_frmdate.filter(lambda x: (x[2] == 'VALID'))
	col_fromdate_valid = col_fromdate_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	col_fromdate_valid.saveAsTextFile("/Output/Cleaning/col1/CMPLNT_DATE_FROM_VALID.out")
	col_fromdate_invalid = col_frmdate.filter(lambda x: (x[2] == 'INVALID'))
	col_fromdate_invalid = col_fromdate_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	col_fromdate_invalid.saveAsTextFile("/Output/Cleaning/col1/CMPLNT_DATE_FROM_INVALID.out")

	#filtering on CMPLNT_TO_DT
	col_todate = data.map(lambda x: (x[0],x[3]))
	col_todate = col_todate.map(lambda x: (x[0],x[1],checker(x[1])))
	col_todate_valid = col_todate.filter(lambda x: (x[2] == 'VALID'))
	col_todate_valid = col_todate_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	col_todate_valid.saveAsTextFile("/Output/Cleaning/col3/CMPLNT_TO_VALID.out")
	col_todate_invalid = col_todate.filter(lambda x: (x[2] == 'INVALID'))
	col_todate_invalid = col_todate_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	col_todate_invalid.saveAsTextFile("/Output/Cleaning/col3/CMPLNT_TO_INVALID.out")

	#filtering on RPT_DT
	col_rptdate = data.map(lambda x: (x[0],x[5]))
	col_rptdate = col_rptdate.map(lambda x: (x[0],x[1],checker(x[1])))
	col_rptdate_valid = col_rptdate.filter(lambda x: (x[2] == 'VALID'))
	col_rptdate_valid = col_rptdate_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t RPT_DT"])
	sc.union([colName, col_rptdate_valid]).saveAsTextFile("/Output/Cleaning/col5/RPT_DT_VALID.out")
	col_rptdate_invalid = col_rptdate.filter(lambda x: (x[2] == 'INVALID'))
	col_rptdate_invalid = col_rptdate_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	sc.union([colName, col_rptdate_invalid]).saveAsTextFile("/Output/Cleaning/col5/RPT_DT_INVALID.out")

	#combined filter on dates
	col_cmbdate = data.map(lambda x: (x[0],x[1],x[3]))
	col_cmbdate = col_cmbdate.map(lambda x: (x[0],x[1],x[2],date_checker(x[1:])))
	col_cmbdate_valid = col_cmbdate.filter(lambda x: (x[3] != 'INVALID'))
	col_cmbdate_valid = col_cmbdate_valid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	colName = sc.parallelize(["CMPLNT_NUM \t CMPLNT_FR_DT \t CMPLNT_TO_DT"])
	sc.union([colName, col_cmbdate_valid]).saveAsTextFile("/Output/Cleaning/col1_3/CMB_DT_VALID.out")
	col_cmbdate_invalid = col_cmbdate.filter(lambda x: (x[3] == 'INVALID'))
	col_cmbdate_invalid = col_cmbdate_invalid.map(lambda x: str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]))
	sc.union([colName, col_cmbdate_invalid]).saveAsTextFile("/Output/Cleaning/col1_3/CMB_DT_INVALID.out")

    sc.stop()