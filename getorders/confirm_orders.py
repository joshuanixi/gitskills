import os,time,shutil,configparser,requests,random
from app.local import newlocal
from mws import mws
root_path=os.path.split(os.path.abspath(__file__))[0]+'/'
root_path=root_path.replace('\\','/')
mws_config_path=newlocal.get_path(root_path,['app','config'])+'mwsconfig.ini'
config_path=newlocal.get_path(root_path,['app','config'])+'config.ini'
#market_place_ids
market_place_ids={'UK':'A1F83G8C2ARO7P',
    'FR':'A13V1IB3VIYZZH',
    'DE':'A1PA6795UKMFR9',
    'IT':'APJ6JRA9NG5V4',
    'ES':'A1RKKUPIHCS9HS',
    'US':'ATVPDKIKX0DER',
	'JP':'A1VC38T7YXB528',
	'CA':'A2EUQ1WTGCTBG2',
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
# reprice_file_path=getpath.get_path(root_path,['src','upload','reprice','used'])+'xtest_reprice.txt'
confirm_file_path=newlocal.get_path(root_path,['src','upload','confirm'])+'confirm.txt'
history_confirm_file_path=newlocal.get_path(root_path,['src','upload','history'])+str(time.time())+'confirm.txt'
feed_client=mws.Feeds(access_key,secret_key,account_id,region)
# feed_type='_POST_FLAT_FILE_ORDER_ACKNOWLEDGEMENT_DATA_'
feed_type='_POST_FLAT_FILE_FULFILLMENT_DATA_'
content_type='application/octet-stream'
if os.path.exists(confirm_file_path):
	FeedContent=open(confirm_file_path,'r').read()
	feed_client.submit_feed(FeedContent,feed_type,content_type=content_type,marketplaceids=[market_place_id])
	os.rename(confirm_file_path,history_confirm_file_path)
	print('confirmed orders')
else:
	print('please check confirm file, not exist.')
time.sleep(3)