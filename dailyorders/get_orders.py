#!/usr/bin/python3
#init path
import os,time,shutil,configparser,requests,random
from app.local import newlocal
from mws import mws
root_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=root_path.replace('\\','/')
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
	'JP':'A1VC38T7YXB528'
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
market_place_id=market_place_ids.get(region)
# print(access_key,secret_key,account_id,region)
Orders_client=mws.Orders(access_key,secret_key,account_id,region,domain='', uri="", version="", auth_token="")
# print(dir(Orders_client))
date_format="%Y-%m-%dT%H:%M:%SZ"
created_before=time.strftime(date_format,time.gmtime())
created_after=time.strftime(date_format,time.gmtime(time.time()-3600*24*days))
orders_file_name=(created_after+'-'+created_before+'.txt').replace(':','')
orders_file_path=orders_dir_path+orders_file_name
# print("after:%s\tbefore:%s\n" % (created_after,created_before))
def get_unshipped_orders(market_place_id,created_after,created_before):
	while True:
		try:
			orders=Orders_client.list_orders(marketplaceids=[market_place_id,],created_after=created_after, created_before=created_before, lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(), payment_methods=(), buyer_email=None, seller_orderid=None, max_results='100')
			break
		except:
			time.sleep(60)
	# print(dir(orders))
	try:
		orders=orders.parsed['Orders']['Order']
	except:
		orders=[]
	unshipped_orders={}
	for order in orders:
		order_id=order['AmazonOrderId']['value']
		order_status=order['OrderStatus']['value']
		if order_status.lower()!='canceled' and order_status.lower()!='pending':
			print(order_status)
			try:
				purchase_date=order['PurchaseDate']['value']
			except:
				purchase_date=''
			try:
				shipment_service_category=order['ShipmentServiceLevelCategory']['value']
			except:
				shipment_service_category=''
			try:
				buyer_name=order['BuyerName']['value']
			except:
				buyer_name=''
			try:
				shipping_address=order['ShippingAddress']
			except:
				shipping_address={}
			try:
				post_code=shipping_address['PostalCode']['value']
			except:
				post_code=''
			try:
				phone=shipping_address['Phone']['value']
			except:
				phone=''
			try:
				ship_buyer_name=shipping_address['Name']['value']
			except:
				ship_buyer_name=''
			try:
				country_code=shipping_address['CountryCode']['value']
			except:
				country_code=''
			try:
				state=shipping_address['StateOrRegion']['value']
			except:
				state=''
			try:
				address1=shipping_address['AddressLine1']['value']
			except:
				address1=''
			try:
				city=shipping_address['City']['value']
			except:
				city=''
			try:
				address2=shipping_address['AddressLine2']['value']
			except:
				address2=''
			number_of_items_shipped=order['NumberOfItemsShipped']['value']
			order_type=order['OrderType']['value']
			earliest_ship_date=order['EarliestShipDate']['value']
			order_total=order['OrderTotal']['Amount']['value']
			latest_ship_date=order['LatestShipDate']['value']
			number_of_items_unshipped=order['NumberOfItemsUnshipped']['value']
			buyer_email=order['BuyerEmail']['value']
			ship_service_level=order['ShipServiceLevel']['value']
			print(order_id,purchase_date,latest_ship_date,order_status)
			if order_status.lower()!='shipped':
				unshipped_orders[order_id]={'order_id':order_id,'purchase_date':purchase_date,'latest_ship_date':latest_ship_date,'order_status':order_status,'shipment_service_category':shipment_service_category}
				# orders_file.write("%s\t%s\t%s\t%s\t%s\n" % (order_id,purchase_date,latest_ship_date,order_status,shipment_service_category))
	return unshipped_orders
all_unshipped_orders={}
while days>0:
	created_before=time.strftime(date_format,time.gmtime(time.time()-3600*24*(days-1)))
	created_after=time.strftime(date_format,time.gmtime(time.time()-3600*24*days))
	unshipped_orders=get_unshipped_orders(market_place_id,created_after,created_before)
	all_unshipped_orders.update(unshipped_orders)
	time.sleep(5)
	days-=1
orders_file=open(orders_file_path,'w')
orders_file.write('order_id\tpurchase\tlatest_ship_date\torder_status\tshipment_service_category\n')
for order_id in all_unshipped_orders:
	order=all_unshipped_orders[order_id]
	orders_file.write("%s\t%s\t%s\t%s\t%s\n" % (order['order_id'],order['purchase_date'],order['latest_ship_date'],order['order_status'],order['shipment_service_category']))
orders_file.close()
# print(orders)


# print(orders.keys())
# print(orders.get('Orders'))
