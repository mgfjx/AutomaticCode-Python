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
AlowUploadToPgyer = 1 #值为1表示上传到蒲公英，为0亦然
UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
BASE_URL = "http://www.pgyer.com"
USER_KEY = "3834f11d73cd7d0e419734b68a539bf2" #蒲公英User Key(在账户设置中获取)
API_KEY = "700ffc367a1d86863d40370c3e95da66" #蒲公英API Key
PGY_Description = '' #上传app时的描述信息
PGY_Password = '' #安装应用时的密码
PGY_Upload_Method = 0 #0为命令行方式上传，1为post请求方式上传

#configuration for fir.im
#上传至fir.im使用的是命令行上传，需要安装fir命令，具体安装请到：https://github.com/FIRHQ/fir-cli/blob/master/README.md
AlowUploadToFir = 0 #值为1表示上传到fir.im，为0亦然
FirIm_BaseUrl = 'http://api.fir.im/apps'
FirIm_API_Token = '2e42187f2685d81c28a87dccc546c2b1'

#上传到蒲公英代码托管,begin-----------------------------------------------------------------------------------------------------------------------------------------------
def uploadToPgyer(ipaPath):
	if PGY_Upload_Method == 0:
		uploadToPgyer_Cmd(ipaPath)
	elif PGY_Upload_Method == 1:
		uploadToPgyer_Request(ipaPath)

def uploadToPgyer_Cmd(ipaPath):
	print('\033[31m'+'uploading To 蒲公英....'+'\033[0m')
	cmdStr = 'curl -F "file=@%s" -F "uKey=%s" -F "_api_key=%s" -F "publishRange=3" -F "isPublishToPublic=2" -F "password=%s" -F "updateDescription=%s" -F "enctype=multipart/form-data" %s' % (ipaPath, USER_KEY, API_KEY, PGY_Password, PGY_Description, UPLOAD_URL)
	# print(cmdStr)
	r = os.popen(cmdStr)
	text = r.read()
	r.close();
	returnJson = json.loads(text)
	downUrl = returnJson['data']['appShortcutUrl']
	if not downUrl == '':
		print('\033[7;32m' + '上传到蒲公英完成,下载地址:' + BASE_URL + '/' + downUrl + '\033[0m')
	elif text == '':
		print ('\033[31m' + '上传到蒲公英失败!' + '\033[0m')

def uploadToPgyer_Request(ipaPath):
	with open(ipaPath, 'rb') as f:
		files = {'file': f}
		headers = {'enctype':'multipart/form-data'}
		payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'3','isPublishToPublic':'2','password':PGY_Password,'updateDescription':PGY_Description}
		print('\033[31m'+'uploading To 蒲公英....'+'\033[0m')
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
		print('\033[7;32m' + '上传到蒲公英完成,下载地址:' + downUrl + '\033[0m')
	else:
		print ('\033[31m' + '上传到蒲公英失败!' + 'Reason:'+jsonResult['message'] + '\033[0m')
		print(jsonResult)

#上传到蒲公英代码托管,end-----------------------------------------------------------------------------------------------------------------------------------------------

#上传到fir.im代码托管,begin-----------------------------------------------------------------------------------------------------------------------------------------------
def uploadToFir(ipaPath):
	uploadCmd = 'fir publish %s --token==%s' %(ipaPath,FirIm_API_Token)
	print(uploadCmd)
	print('\033[31m'+'uploading To fir.im....'+'\033[0m')
	isUploaded = os.popen(uploadCmd)
	text = isUploaded.read()
	isUploaded.close()
	print(text)
	# if isUploaded == 0:
	# 	print('\033[32m' + '上传到fir.im完成,下载地址:' + '\033[0m')
	# else:
	# 	print ('\033[31m' + '上传到fir.im失败!' + '\033[0m')
#上传到fir.im代码托管,end-----------------------------------------------------------------------------------------------------------------------------------------------


#编译工程，begin--------------------------------------------------------------------------------------------------------------------------------------------------------
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
			print('\033[7;32m' + '打包完成,请到%s获取ipa文件'%ipaPath + '\033[0m')
			if AlowUploadToPgyer == 1:
				uploadToPgyer(ipaPath)
			if AlowUploadToFir == 1:
				uploadToFir(ipaPath)
	os.system('rm -rf ./build')

#打包.xcworkspace工程
def buildWorkspace(ProjectName):
	#xcodebuild  -workspace $projectName.xcworkspace -scheme $projectName  -configuration $buildConfig clean build SYMROOT=$buildAppToDir
	buildDir = os.path.join(cur_file_dir(),'build')#确保编译输出路径是完整路径编译才不会报错
	buildCmd = 'xcodebuild -workspace %s.xcworkspace -scheme %s -configuration %s CONFIGURATION_BUILD_DIR=%s' % (ProjectName, ProjectName, CONFIGURATION, buildDir)
	isBuilded = os.system(buildCmd);
	fileName = ProjectName + getNowTime() + '.ipa'
	if isBuilded == 0:
		isPackaged = os.system('xcrun -sdk iphoneos -v PackageApplication %s/%s.app -o ~/Desktop/%s' % (buildDir, ProjectName, fileName))	
		if isPackaged == 0:
			ipaPath = os.environ['HOME']
			ipaPath = os.path.join(ipaPath, 'Desktop')
			ipaPath = os.path.join(ipaPath, fileName)
			print('\033[7;32m' + '打包完成,请到%s获取ipa文件'%ipaPath + '\033[0m')
			if AlowUploadToPgyer == 1:
				uploadToPgyer(ipaPath)
			if AlowUploadToFir == 1:
				uploadToFir(ipaPath)
	os.system('rm -rf ./build')
#编译工程，end--------------------------------------------------------------------------------------------------------------------------------------------------------

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