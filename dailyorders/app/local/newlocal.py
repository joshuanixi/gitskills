import os,shutil,time
def get_path(begin_path,directory_list):
	path=begin_path
	for directory in directory_list:
		path=path+directory.strip('/')+'/'
	return path