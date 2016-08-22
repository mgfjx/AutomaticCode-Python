# -*- coding: utf-8 -*-
import os,sys
import subprocess
import requests
import time

#configuration for iOS build setting
CONFIGURATION = "Release"
SDK = "iphoneos"

#configuration for 蒲公英
AlowUploadToPgyer = 1 #值为1表示上传到蒲公英，为0亦然
UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
BASE_URL = "http://www.pgyer.com"
USER_KEY = "3834f11d73cd7d0e419734b68a539bf2"
API_KEY = "700ffc367a1d86863d40370c3e95da66"

def uploadToPgyer(ipaPath):
	print('ipaPath:'+ipaPath)
	files = {'file':open(ipaPath,'rb')}
	headers = {'enctype':'multipart/form-data'}
	payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'3','isPublishToPublic':'2','password':'','updateDescription':''}
	print('\033[31m'+'uploading....'+'\033[0m')
	try:
		r = requests.post(UPLOAD_URL, data = payload, files = files, headers = headers)
		if r.status_code == requests.codes.ok:
			print('\033[32m' + '上传完成' + '\033[0m')
		else:
			print('\033[31m' + 'HTTPError,Code:'+r.status_code + '\033[0m')
	except :
		print('\033[31m' + '请检查网络！' + '\033[0m')



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
	os.system('rm -rf ./build')

def buildWorkspace():
	print('buildWorkspace')


#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

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
		elif name.endswith('.workspace'):
			options['workspace'] = name

	# print(options)

	#若果存在workspace，则以workspace打包,否则判断project是否存在，存在即用project打包
	if options['workspace'].strip() != '':
		buildWorkspace()
	elif options['project'].strip() != '':
		buildProject(options['project'].replace('.xcodeproj', ''))
	else:
		print('\033[31m'+'项目不存在,请检查路径(脚本文件需放在被打包的工程目录下)'+'\033[0m')

if __name__ == '__main__':
	main()