# -*- coding: utf-8 -*-
import os,sys
import subprocess
import requests
import time
import json

#configuration for iOS build setting
CONFIGURATION = "Release"
SDK = "iphoneos"

#configuration for 蒲公英
AlowUploadToPgyer = 0 #值为1表示上传到蒲公英，为0亦然
UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
BASE_URL = "http://www.pgyer.com"
USER_KEY = "3834f11d73cd7d0e419734b68a539bf2" #蒲公英User Key(在账户设置中获取)
API_KEY = "700ffc367a1d86863d40370c3e95da66" #蒲公英API Key
App_Description = '' #上传app时的描述信息

#configuration for fir.im
AlowUploadToFir = 1 #值为1表示上传到fir.im，为0亦然
FirIm_BaseUrl = 'http://api.fir.im/apps'
FirIm_API_Token = '2e42187f2685d81c28a87dccc546c2b1'

#上传到蒲公英代码托管,begin-----------------------------------------------------------------------------------------------------------------------------------------------
def uploadToPgyer(ipaPath):
	print('ipaPath:'+ipaPath)
	files = {'file':open(ipaPath,'rb')}
	headers = {'enctype':'multipart/form-data'}
	payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'3','isPublishToPublic':'2','password':'','updateDescription':App_Description}
	print('\033[31m'+'uploading....'+'\033[0m')
	try:
		r = requests.post(UPLOAD_URL, data = payload, files = files, headers = headers)
		if r.status_code == requests.codes.ok:
			result = r.json()
			parserReturnData(result)
		else:
			print('\033[31m' + 'HTTPError,Code:'+r.status_code + '\033[0m')
	except :
		print('\033[31m' + '请检查网络！' + '\033[0m')

#解析上传返回数据
def parserReturnData(jsonResult):
	resultCode = jsonResult['code']
	if resultCode == 0:
		downUrl = BASE_URL + '/' + jsonResult['data']['appShortcutUrl']
		print('\033[32m' + '上传完成,下载地址:' + downUrl + '\033[0m')
	else:
		print ('\033[31m' + '上传失败!' + 'Reason:'+jsonResult['message'] + '\033[0m')
		print(jsonResult)

#上传到蒲公英代码托管,end-----------------------------------------------------------------------------------------------------------------------------------------------

#上传到fir.im代码托管,begin-----------------------------------------------------------------------------------------------------------------------------------------------
def uploadToFir(ipaPath):
	print('uploadToFir:' + ipaPath)
	param = {'type' : 'ios', 'bundle_id' : 'com.xiexiaolong.test', 'api_token' : FirIm_API_Token}
	try:
		r = requests.post(FirIm_BaseUrl, data = param)
		if r.status_code == 201:
			result = r.json()
			parserFirImData(result)
		else:
			print('\033[31m' + 'HTTPError,Code:'+r.status_code + '\033[0m')
	except :
		print('\033[31m' + '请检查网络！' + '\033[0m')

def parserFirImData(result):
	print(result)

#上传到fir.im代码托管,end-----------------------------------------------------------------------------------------------------------------------------------------------

#打包.xcodeproj工程
def buildProject(ProjectName):
	isBuilded = os.system('xcodebuild -project %s.xcodeproj -target %s -configuration Release' % (ProjectName, ProjectName));
	fileName = ProjectName + getNowTime() + '.ipa'
	if isBuilded == 0:
		isPackaged = os.system('xcrun -sdk iphoneos -v PackageApplication ./build/Release-iphoneos/%s.app -o ~/Desktop/%s' % (ProjectName, fileName))	
		if isPackaged == 0:
			ipaPath = os.environ['HOME']
			ipaPath = os.path.join(ipaPath, 'Desktop')
			ipaPath = os.path.join(ipaPath, fileName)
			print('\033[32m' + '打包完成,请到%s获取ipa文件'%ipaPath + '\033[0m')
			if AlowUploadToPgyer == 1:
				uploadToPgyer(ipaPath)
			if AlowUploadToFir == 1:
				uploadToFir(ipaPath)
	os.system('rm -rf ./build')

#打包.xcworkspace工程
def buildWorkspace(ProjectName):
	print('buildWorkspace')
	isBuilded = os.system('xcodebuild -workspace %s.xcworkspace -scheme %s -configuration Release' % (ProjectName, ProjectName));
	fileName = ProjectName + getNowTime() + '.ipa'
	if isBuilded == 0:
		isPackaged = os.system('xcrun -sdk iphoneos -v PackageApplication ./build/%s.app -o ~/Desktop/%s' % (ProjectName, fileName))	
		if isPackaged == 0:
			ipaPath = os.environ['HOME']
			ipaPath = os.path.join(ipaPath, 'Desktop')
			ipaPath = os.path.join(ipaPath, fileName)
			print('\033[32m' + '打包完成,请到%s获取ipa文件'%ipaPath + '\033[0m')
			if AlowUploadToPgyer == 1:
				uploadToPgyer(ipaPath)
	# os.system('rm -rf ./build')


#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#获取当前时间
def getNowTime():
	return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

def main():
	files = []
	path = cur_file_dir()
	print(path)
	files = os.listdir(path)
	options = {'project':'','workspace':'','scheme':'','target':''}
	for name in files:
		if name.endswith('.xcodeproj'):
			options['project'] = str(name)
		elif name.endswith('.xcworkspace'):
			options['workspace'] = name

	print(options)

	#若果存在workspace，则以workspace打包,否则判断project是否存在，存在即用project打包
	if options['workspace'].strip() != '':
		buildWorkspace(options['workspace'].replace('.xcworkspace', ''))
	elif options['project'].strip() != '':
		buildProject(options['project'].replace('.xcodeproj', ''))
	else:
		print('\033[31m'+'项目不存在,请检查路径(脚本文件需放在被打包的工程目录下)'+'\033[0m')

if __name__ == '__main__':
	main()