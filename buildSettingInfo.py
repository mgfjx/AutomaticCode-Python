# -*- coding: utf-8 -*-
import os
import re

InfoPlistSettingName = 'PRODUCT_SETTINGS_PATH = '
InfoPlistPath = ''

result = os.popen('xcodebuild -showBuildSettings')
# print('result = ' + result.read())

content = result.read()
print('content =========== '+content)
matchObj = re.search(r'PRODUCT_SETTINGS_PATH = (.*)', content, re.M|re.I)

if matchObj:
    string = matchObj.group()
    InfoPlistPath = string[len(InfoPlistSettingName):]
    print('InfoPlistPath:'+InfoPlistPath)
else:
    print('Nothing found!!')