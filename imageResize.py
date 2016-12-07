#!/usr/bin/env python
# coding: utf-8

import sys
import os

try:
    from PIL import Image
except:
    print ('\033[31m' + '缺少Image模块，正在安装Image模块，请等待...' + '\033[0m')
    success = os.system('python -m pip install Image')
    if success == 0:
      print('\033[7;32m' + 'Image模块安装成功.' + '\033[0m')
      from PIL import Image
    else:
      print ('\033[31m' + 'Image安装失败，请手动在终端执行：\'python -m pip install Image\'重新安装.' + '\033[0m')
      quit()


outPutPath = os.path.expanduser('~') + '/Desktop/'

if len(sys.argv) < 4 :
    print ('\033[31m' + '请输入正确命令,eg: \'python autoExportAppIcon.py /path/xxx.png 20 30\',表示把图片重置为宽20高30的图片' + '\033[0m')
    quit()

ImageName = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])

originImg = ''
try:
    originImg = Image.open(ImageName)
except:
    print ('\033[31m' + '\'' + ImageName + '\'' + '，该文件不是图片文件，请检查文件路径.' + '\033[0m')
    quit()

print('width = ' + str(width) + ', height = ' + str(height))
print(outPutPath)
img0 = originImg.resize((width, height), Image.ANTIALIAS)
img1 = originImg.resize((width*2, height*2), Image.ANTIALIAS)
img2 = originImg.resize((width*3,height*3), Image.ANTIALIAS)
img0.save(outPutPath + 'imageIcon.png',"png")
img1.save(outPutPath + 'imageIcon@2x.png',"png")
img2.save(outPutPath + 'imageIcon@3x.png',"png")
os.system('open ' + outPutPath)



