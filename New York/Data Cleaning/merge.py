import sys
from pyspark import SparkContext, SparkConf
from csv import reader

response = ""
def csv_file(x, flag):
	global response

	if flag == 1:
		response = ""
	if not type(x) is tuple:
		return
	for n in x:
		if type(n) is tuple:
			csv_file(n,0)
		else:
			if response == "":
				response = str(n)
			else:
				response = response + ',"' +  str(n) + '"'
	return response

def ordering(x):
	y = x.split(",")
	y[2],y[3]=y[3],y[2]
	return ",".join(y)

if __name__ == "__main__":
	conf = SparkConf().setAppName('app')
	sc   = SparkContext(conf=conf)
	header = sc.parallelize(["CMPLNT_NUM,CMPLNT_FR_DT,CMPLNT_FR_TM,CMPLNT_TO_DT,CMPLNT_TO_TM,RPT_DT,KY_CD,OFNS_DESC,PD_CD,PD_DESC,CRM_ATPT_CPTD_CD,LAW_CAT_CD,JURIS_DESC,BORO_NM,ADDR_PCT_CD,LOC_OF_OCCUR_DESC,PREM_TYP_DESC,PARKS_NM,X_COORD_CD,Y_COORD_CD,Latitude,Longitude"])
    for i in range(1,22):
		if i == 1:
			lines = sc.textFile("/Output/Cleaning/col1_3/CMB_DT_VALID.out", 1)
		if i == 2:
			lines = sc.textFile("/Output/Cleaning/col2/CMPLNT_TIME_FROM_VALID.out", 1)
		if i == 3:
			continue
		if i == 4:
			lines = sc.textFile("/Output/Cleaning/col4/CMPLNT_TIME_TO_VALID.out", 1)
		if i == 5:
			lines = sc.textFile("/Output/Cleaning/col5/RPT_DT_VALID.out", 1)
		if i == 6:
			lines = sc.textFile("/Output/Cleaning/col6/KEY_CD_VALID.out", 1)
		if i == 7:
			lines = sc.textFile("/Output/Cleaning/col7/KEY_DESC_VALID.out", 1)
		if i == 8:
			lines = sc.textFile("/Output/Cleaning/col8/PD_CD_VALID.out", 1)
		if i == 9:
			lines = sc.textFile("/Output/Cleaning/col9/PD_DESC_VALID.out", 1)
		if i == 10:
			lines = sc.textFile("/Output/Cleaning/col10/CRM_VALID.out", 1)
		if i == 11:
			lines = sc.textFile("/Output/Cleaning/col11/LAW_CAT_VALID.out", 1)
		if i == 12:
			lines = sc.textFile("/Output/Cleaning/col12/JURIS_DESC_VALID.out", 1)
		if i == 13:
			lines = sc.textFile("/Output/Cleaning/col13/BORO_NM_VALID.out", 1)
		if i == 14:
			lines = sc.textFile("/Output/Cleaning/col14/ADDR_CD_VALID.out", 1)
		if i == 15:
			lines = sc.textFile("/Output/Cleaning/col15/LOC_DESC_VALID.out", 1)
		if i == 16:
			lines = sc.textFile("/Output/Cleaning/col16/PREM_DESC_VALID.out", 1)
		if i == 17:
			lines = sc.textFile("/Output/Cleaning/col17/PARKS_NM_VALID.out", 1)
		if i == 18:
			lines = sc.textFile("/Output/Cleaning/col19/X_COORD_VALID.out", 1)
		if i == 19:
			lines = sc.textFile("/Output/Cleaning/col20/Y_COORD_VALID.out", 1)
		if i == 20:
			lines = sc.textFile("/Output/Cleaning/col21/LATITUDE_VALID.out", 1)
		if i == 21:
			lines = sc.textFile("/Output/Cleaning/col22/LONGITUDE_VALID.out", 1)

		if i == 1:
			lines = lines.map(lambda x:(x.split('\t')[0],(x.split('\t')[1],x.split('\t')[2])))
			data = lines
		else:
			lines = lines.map(lambda x:(x.split('\t')[0],x.split('\t')[1]))
			data = data.join(lines)

		if i ==21:
			data = data.map(lambda x: csv_file(x, 1))
			data = data.map(lambda x: ordering(x))
			sc.union([header, data]).saveAsTextFile("/Output/data.csv")
