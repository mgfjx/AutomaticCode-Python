# -*- coding: utf-8 -*-
import json

def judgeNillDict():
	pass

def parseJSON(dictionary):
	keys = []
	for key,value in dictionary.items():
		
		if isinstance(value, list):
			for json in list:
				# keys.append(parseJSON(json))
		else:
			keys.append(key)
	return keys

with open('/Users/xiexiaolong1/pythonCode/json.txt','r') as jsonString:
	dic = json.load(jsonString)
	parseJSON(dic);
