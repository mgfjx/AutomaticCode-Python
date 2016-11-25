# -*- coding: utf-8 -*-
import os
import re
import time

# 所需的字段名称
# plist配置文件名及路径
InfoPlistSettingKey = 'PRODUCT_SETTINGS_PATH'
InfoPlistPath = ''
InfoPlistFileKey = 'INFOPLIST_FILE'
InfoPlistFilePath = ''

# 项目名称
ProductNameKey = 'PRODUCT_NAME'
ProductName = ''

# PRODUCT_BUNDLE_IDENTIFIER
BundleIdentifierKey = 'PRODUCT_BUNDLE_IDENTIFIER'
BundleIdentifier = ''

#获取当前时间
def getCurrentTime():
	return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

# 获取当前项目的配置文件
result = os.popen('xcodebuild -showBuildSettings')
content = result.read()
InfoDict = {}
if not content.strip():
    print("未获取到配置文件信息!!")
    quit()
else:
    regex = ur"    (.*) = (.*)"
    reobj = re.compile(regex)
    for match in reobj.finditer(content):
        InfoDict[match.group(1)] = match.group(2)

if InfoDict:
    InfoPlistPath = InfoDict[InfoPlistSettingKey]
    print('InfoPlistPath = ' + InfoPlistPath)
    InfoPlistFilePath = InfoDict[InfoPlistFileKey]
    print('InfoPlistFilePath = ' + InfoPlistFilePath)
    ProductName = InfoDict[ProductNameKey]
    print('ProductName = ' + ProductName)
    BundleIdentifier = InfoDict[BundleIdentifierKey]
    print('BundleIdentifier = ' + BundleIdentifier)

OutPutPath = os.environ['HOME']
OutPutPath = os.path.join(OutPutPath, 'Desktop')
OutPutPath = os.path.join(OutPutPath, ProductName + getCurrentTime())
ArchivePath = os.path.join(OutPutPath, ProductName + '.xcarchive')
archiveCmd = 'xcodebuild archive -scheme %s -configuration "Release" -archivePath %s'%(ProductName,ArchivePath)
archiveSuccess = os.system(archiveCmd)
if archiveSuccess == 0:
    exportCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s'%(ArchivePath, OutPutPath, InfoPlistPath)
    exportSuccess = os.system(exportCmd)
    if exportSuccess == 0:
        os.system('open ' + OutPutPath)
        print('打包成功')