# -*- coding: utf-8 -*-
import json

def judgeNillDict():
	pass

def parseJSON(dictionary):
	allKeys = []
	keys = []
	for key,value in dictionary.items():
		
		if isinstance(value, list):
			for json in value:
				allKeys.append(parseJSON(json))

		elif isinstance(value, dict):
			allKeys.append(parseJSON(value))

		keys.append(key)
	allKeys.append(keys)

	return allKeys

#/Users/xiexiaolong1/Desktop/zy.txt
#/Users/xiexiaolong1/pythonCode/json.txt
with open('/Users/xiexiaolong1/Desktop/zy.txt','r') as jsonString:
	dic = json.load(jsonString)
	print(parseJSON(dic))
