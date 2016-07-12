#!/usr/bin/python3
#init path
import os,time,shutil,configparser,requests,random,codecs
from app.local import newlocal
from mws import mws
import csv



root_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=root_path.replace('\\','/')
reports_dir_path=newlocal.get_path(root_path,['src','reports'])
orders_dir_path=newlocal.get_path(root_path,['src','orders'])
mws_config_path=newlocal.get_path(root_path,['app','config'])+'mwsconfig.ini'
config_path=newlocal.get_path(root_path,['app','config'])+'config.ini'
#market_place_ids
market_place_ids={'UK':'A1F83G8C2ARO7P',
    'FR':'A13V1IB3VIYZZH',
    'DE':'A1PA6795UKMFR9',
    'IT':'APJ6JRA9NG5V4',
    'ES':'A1RKKUPIHCS9HS',
    'US':'ATVPDKIKX0DER',
    'CA':'A2EUQ1WTGCTBG2',
	'JP':'A1VC38T7YXB528',
	}
# get mws info
mwsconfig=configparser.ConfigParser()
mwsconfig.read(mws_config_path)
access_key=mwsconfig.get('mws','aws_access_key')
secret_key=mwsconfig.get('mws','aws_secret_key')
account_id=mwsconfig.get('mws','seller_id')

# get info
config=configparser.ConfigParser()
config.read(config_path)
days=int(config.get('info','days'))
region=config.get('info','region').upper()
account_num=config.get('info','accountnum').upper()
market_place_id=market_place_ids.get(region)
# print(access_key,secret_key,account_id,region)
Reports_client=mws.Reports(access_key,secret_key,account_id,region,domain='', uri="", version="", auth_token="")
# print(dir(Orders_client))

orders_file_name=time.strftime("%Y-%m-%d",time.localtime())+'__'+account_num.lower()+region.lower()+'.txt'
orders_file_path=orders_dir_path+orders_file_name
def downloadorder():
	# orders=Orders_client.list_orders(marketplaceids=[market_place_id,],created_after=created_after, created_before=created_before, lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(), payment_methods=(), buyer_email=None, seller_orderid=None, max_results='100')
	# report_type='_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'
	report_type='_GET_FLAT_FILE_ORDERS_DATA_'
	report_list=Reports_client.get_report_list(requestids=(), max_count=None, types=(report_type,), acknowledged=None,
							fromdate=None, todate=None)
	try:
		first_report=report_list.parsed['ReportInfo'][0]
		report_time=first_report['AvailableDate']['value']
	except:
		report_time='0'
	date_format="%Y-%m-%dT%H:%M:%SZ"
	created_before=time.strftime(date_format,time.gmtime())
	created_after=time.strftime(date_format,time.gmtime(time.time()-3600*24*days))
	acceptable_time=time.strftime(date_format,time.gmtime(time.time()-360))
	if report_time<acceptable_time:
		Reports_client.request_report(report_type, start_date=created_after, end_date=created_before, marketplaceids=())
	while report_time<acceptable_time:
		time.sleep(30)
		report_list=Reports_client.get_report_list(requestids=(), max_count=None, types=(report_type,), acknowledged=None,
								fromdate=None, todate=None)
		try:
			first_report=report_list.parsed['ReportInfo'][0]
			report_time=first_report['AvailableDate']['value']
		except:
			print('wating for report...')
			report_time='0'
		print(report_time)
	report_id=first_report['ReportId']['value']
	print(report_id)
	report=Reports_client.get_report(report_id)
	content=report.parsed
	with open(orders_file_path,'w') as f:
		try:
			f.write(codecs.decode(content,'utf8','ignore').replace('\r\n','\n'))
		except:
			f.write(codecs.decode(content,'gbk','ignore').replace('\r\n','\n'))
	return orders_file_name



def readorder(orders_file_name,account_num,region,orders_dir_path):
	

	orders_file_name=orders_file_name
	orders_file_path=orders_dir_path+orders_file_name
	f = open(orders_file_path, 'r' ,encoding='utf-8',errors='ignore')
	dailyordernumber=len(f.readlines())
	f.seek(0)
	print (dailyordernumber)
	csv_file=orders_dir_path+time.strftime("%Y-%m-%d",time.localtime())+'__'+account_num.lower()+region.lower()+'.csv'
	file_read = csv.reader(f, delimiter = '\t')
	fcsv=open(csv_file, 'wt', newline='')
	out_csv = csv.writer(fcsv)
	out_csv.writerows(file_read)
	#print (time.time()) 
	f.close()
	fcsv.close()

def ctdatabase():
	pass

def wtdatabase():
	pass

def readcsv(csvfile):
	with open(csvfile) as f:
		f_csv = csv.reader(f)
		headers = next(f_csv)
		for row in f_csv:
			print (row)

       

csvname='2016-07-08__28ca.csv'
csvfile=orders_dir_path+csvname

readcsv(csvfile)




#readorder(downloadorder(),account_num,region,orders_dir_path)    



