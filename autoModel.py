# -*- coding: utf-8 -*-

#configuration begin

outPutPath = '' #.h .m输出路径
jsonPath = '/Users/xiexiaolong/pythonCode/AutomaticCode-Python/json.txt' #json数据文件路径,不填默认输出到当前用户桌面

fileName = 'Model' #新建.h .m 文件名
mark = 'm_' #给字段加标识
className = 'Model' #模型类名(需要手动修改)

#configuration end

explanation = '''
/*
 *  autoModel.py
 *  用python写的根据json数据自动创建.h和.m文件脚本，使用前请配置#configuration 中间的全局变量:
 *  eg:
 *  outPutPath = '/Users/xiexiaolong1/Desktop/python/' (#.h和.m输出路径,不填默认输出到当前用户桌面)
 *  jsonPath = '/Users/xiexiaolong1/Desktop/python/json.txt' (#json数据文件路径)
 *  fileName = 'ContactModel' (#新建.h .m 文件名)
 *  mark = 'm_' (#给字段加标识)
 *  className = 'Model' (#模型类名(需要手动修改))
 *  github地址:https://github.com/mgfjxxiexiaolong/AutomaticCode-Python
 */\n\n
'''

import json
import os
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
			key = 'List-' + key
			if len(value) > 0:
				allKeys.append({key:parseJSON(value[0])})

		elif isinstance(value, dict):
			key = 'List-' + key
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
			# print(keys)
			# print('--------------------')

	elif isinstance(data, dict):
		for key,value in data.item():
			getKeys(value)

def writeToFile(array):
	#.h文件写入
	with open(os.path.join(outPutPath, fileName + '.h'), 'a') as writeFile:
		writeFile.write('@interface ' + '<#' + className + '#>' + ' : NSObject//自定义:类名需手动修改\n\n')
		for value in array:
			string = ''
			if value.startswith('List-'):
				value = value.replace('List-','')
				string = '@property (nonatomic, strong) NSArray  *' + mark + value + ';\n'
			else:
				string = '@property (nonatomic, strong) NSString *' + mark + value + ';\n'
			writeFile.write(string)

		writeFile.write('\n- (instancetype)initDataWith:(NSDictionary *)dicttionary;\n')
		writeFile.write('\n@end\n\n\n')

	#.m文件写入
	with open(os.path.join(outPutPath, fileName + '.m'), 'a') as writeFile:
		writeFile.write('@implementation ' + '<#' + className + '#>' + '//自定义:类名需手动修改\n\n')
		string = '- (instancetype)initDataWith:(NSDictionary *)dicttionary{\n\tself = [super init];\n\tif (self) {\n\n'
		writeFile.write(string)
		string = ''
		for value in array:
			if value.startswith('List-'):
				value = value.replace('List-','')
				string = '''
        NSMutableArray *array = [NSMutableArray array];
        NSArray *list = dicttionary[@"''' + value +'''"];
        for (NSDictionary *dict in list) {
            <#当前数组元素对应类#> *model = [[<#当前数组元素对应类#> alloc] initDataWith:dict];
            [array addObject:model];
        }
        self.''' + mark + value + ''' = [array copy];\n\n'''
				# string = '\t\tself.' + mark + value + ' = (NSArray *)dicttionary[@"' + value + '"];\n'
			else:
				string = '\t\tself.' + mark + value + ' = NSStringFormat(dicttionary[@"' + value + '"]);\n'
			writeFile.write(string)
		string = '\n\t}\n\treturn self;\n\n}'
		writeFile.write(string)
		writeFile.write('\n@end\n\n\n')

def createFiles():
	global outPutPath
	if outPutPath == '':
		outPutPath = os.path.join(os.environ['HOME'], 'Desktop')
	#.h file
	with open(os.path.join(outPutPath, fileName + '.h'), 'a') as writeFile:
		writeFile.write(explanation)
		writeFile.write('#import <Foundation/Foundation.h>\n\n')

	#.m file
	with open(os.path.join(outPutPath, fileName + '.m'), 'a') as writeFile:
		writeFile.write(explanation)
		writeFile.write('#import "' + fileName + '.h"\n')
		writeFile.write('#define NSStringFormat(x) [NSString stringWithFormat:@"%@",(x)]\n\n')

#程序入口
with open(jsonPath,'r') as jsonString:
	dic = {}
	try:
		print('\033[1;32m' + '正在从' + jsonPath + '获取json数据...' + '\033[0m')
		dic = json.load(jsonString)
		print('\033[1;32m' + '正在解析并创建文件...' + '\033[0m')
		allKeys = parseJSON(dic)
		#创建文件
		createFiles()
		# print(allKeys)
		getKeys(allKeys)

		print('\033[7;32m' + '文件创建完成!请到路径:' + outPutPath + ' 获取。' + '\033[0m')
	except ValueError:
		print('\033[7;31m' + 'Json解析错误，请校验Json格式是否正确:http://tool.oschina.net/codeformat/json' + '\033[0m')


