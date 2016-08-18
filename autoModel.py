# -*- coding: utf-8 -*-
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

		# keys.append(key)
	keys = dictionary.keys()
	allKeys.append(keys)

	return allKeys

path1 = '/Users/xiexiaolong1/Desktop/zy.txt'
path2 = '/Users/xiexiaolong1/pythonCode/json.txt'
with open(path1,'r') as jsonString:
	dic = json.load(jsonString)
	# print(judgeNillDict(dic))
	allKeys = parseJSON(dic)

	for value in allKeys:
		# print(type(value))
		if  isinstance(value, dict):
			print(value)
		else :
			print(value[0])

