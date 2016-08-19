# -*- coding: utf-8 -*-

#configuration begin

path = '/Users/xiexiaolong1/Desktop/python/' #.h .m输出路径
path1 = '/Users/xiexiaolong1/Desktop/python/json.txt' #json数据文件路径

fileName = 'ContactModel' #新建.h .m 文件名
mark = 'm_' #给字段加标识
className = 'Model' #模型类名(需要手动修改)

explanation = '''
/*
 *  autoModel.py
 *  用python写的根据json数据自动创建.h和.m文件脚本，使用前请配置#configuration 中间的全局变量:
 *  eg:
 *  path = '/Users/xiexiaolong1/Desktop/python/' (#h .m输出路径)
 *  path1 = '/Users/xiexiaolong1/Desktop/python/json.txt' (#json数据文件路径)
 *  fileName = 'ContactModel' (#新建.h .m 文件名)
 *  mark = 'm_' (#给字段加标识)
 *  className = 'Model' (#模型类名(需要手动修改))
 *  github地址:https://github.com/mgfjxxiexiaolong/AutomaticCode-Python
 */\n\n
'''

#configuration end

import json
def judgeNillDict(dictionary):
	isExist = False
	for key,value in dictionary.items():
		if isinstance(value, dict) or isinstance(value, list):
			if value:
				isExist = True
				break

	return isExist

def parseJSON(dictionary):
	allKeys = []
	keys = []

	for key,value in dictionary.items():
		
		if isinstance(value, list):
			if len(value) > 0:
				allKeys.append({key:parseJSON(value[0])})

		elif isinstance(value, dict):
			allKeys.append({key:parseJSON(value)})

		keys.append(key)

	allKeys.append(keys)

	return allKeys

def getKeys(data):
	
	if isinstance(data, list):
		keys = []
		for value in data:
			if  isinstance(value, dict):
				for key,item in value.items():
					getKeys(item)
			elif isinstance(value, list):
				getKeys(value)
			else:
				# 写入到文件
				keys.append(value)

		if len(keys) > 0:
			writeToFile(keys)
			print(keys)
			print('--------------------')

	elif isinstance(data, dict):
		for key,value in data.item():
			getKeys(value)

def writeToFile(array):
	#.h文件写入
	with open(path + fileName + '.h', 'a') as writeFile:
		writeFile.write('@interface ' + className + ' : NSObject//自定义:类名需手动修改\n\n')
		for value in array:
			string = '@property (nonatomic, strong) NSString *' + mark + value + ';\n'
			writeFile.write(string)

		writeFile.write('\n- (instancetype)initDataWith:(NSDictionary *)dicttionary;\n')
		writeFile.write('\n@end\n\n\n')

	#.m文件写入
	with open(path + fileName + '.m', 'a') as writeFile:
		writeFile.write('@implementation ' + className + '//自定义:类名需手动修改\n\n')
		string = '- (instancetype)initDataWith:(NSDictionary *)dicttionary{\n\tself = [super init];\n\tif (self) {\n\n'
		writeFile.write(string)
		for value in array:
			string = '\t\tself.' + mark + value + ' = NSStringFormat(dicttionary[@"' + value + '"]);\n'
			writeFile.write(string)
		string = '\n\t}\n\treturn self;\n\n}'
		writeFile.write(string)
		writeFile.write('\n@end\n\n\n')

def createFiles():
	#.h file
	with open(path + fileName + '.h', 'a') as writeFile:
		writeFile.write(explanation)
		writeFile.write('#import <Foundation/Foundation.h>\n\n')

	#.m file
	with open(path + fileName + '.m', 'a') as writeFile:
		writeFile.write(explanation)
		writeFile.write('#import "' + fileName + '.h"\n')
		writeFile.write('#define NSStringFormat(x) [NSString stringWithFormat:@"%@",(x)]\n\n')

#程序入口
with open(path1,'r') as jsonString:
	dic = json.load(jsonString)
	# print(judgeNillDict(dic))
	allKeys = parseJSON(dic)
	#创建文件
	createFiles()
	# print(allKeys)
	getKeys(allKeys)
