#!/usr/bin/env python3
# coding: utf-8

from PIL import Image
import sys
import os

outPutPath = os.path.expanduser('~') + '/Desktop/AppIcon/'

if not os.path.exists(outPutPath):
    os.mkdir(outPutPath)

ImageName = sys.argv[1]
# print('图片名字为：' + ImageName)
originImg = Image.open(ImageName)

# 20x20
img1 = originImg.resize((40,40), Image.ANTIALIAS)
img2 = originImg.resize((60,60), Image.ANTIALIAS)
img1.save(outPutPath + 'appIcon20x20@2x.png',"png")
img2.save(outPutPath + 'appIcon20x20@3x.png',"png")

# 29x29
img3 = originImg.resize((29,29), Image.ANTIALIAS)
img4 = originImg.resize((58,58), Image.ANTIALIAS)
img5 = originImg.resize((87,87), Image.ANTIALIAS)
img3.save(outPutPath + 'appIcon29x29.png',"png")
img4.save(outPutPath + 'appIcon29x29@2x.png',"png")
img5.save(outPutPath + 'appIcon29x29@3x.png',"png")

# 40x40
img6 = originImg.resize((80,80), Image.ANTIALIAS)
img7 = originImg.resize((120,120), Image.ANTIALIAS)
img6.save(outPutPath + 'appIcon40x40@2x.png',"png")
img7.save(outPutPath + 'appIcon40x40@3x.png',"png")

# 60x60
img8 = originImg.resize((120,120), Image.ANTIALIAS)
img9 = originImg.resize((180,180), Image.ANTIALIAS)
img8.save(outPutPath + 'appIcon60x60@2x.png',"png")
img9.save(outPutPath + 'appIcon60x60@3x.png',"png")

# ipad
img10 = originImg.resize((76,76), Image.ANTIALIAS)
img11 = originImg.resize((152,152), Image.ANTIALIAS)
img12 = originImg.resize((167,167), Image.ANTIALIAS)
img10.save(outPutPath + 'appIcon76x76.png',"png")
img11.save(outPutPath + 'appIcon76x76@2x.png',"png")
img12.save(outPutPath + 'appIcon83.5x83.5@2x.png',"png")

# 创建Contents.json文件

content = '''
{
  "images" : [
    {
      "size" : "40x40",
      "idiom" : "ipad",
      "filename" : "appIcon40x40.png",
      "scale" : "1x"
    },
    {
      "size" : "40x40",
      "idiom" : "ipad",
      "filename" : "appIcon40x40@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "76x76",
      "idiom" : "ipad",
      "filename" : "appIcon76x76.png",
      "scale" : "1x"
    },
    {
      "size" : "76x76",
      "idiom" : "ipad",
      "filename" : "appIcon76x76@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "83.5x83.5",
      "idiom" : "ipad",
      "filename" : "appIcon83.5x83.5@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "29x29",
      "idiom" : "ipad",
      "filename" : "appIcon29x29.png",
      "scale" : "1x"
    },
    {
      "size" : "29x29",
      "idiom" : "ipad",
      "filename" : "appIcon29x29@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "29x29",
      "idiom" : "iphone",
      "filename" : "appIcon29x29.png",
      "scale" : "1x"
    },
    {
      "size" : "29x29",
      "idiom" : "iphone",
      "filename" : "appIcon29x29@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "29x29",
      "idiom" : "iphone",
      "filename" : "appIcon29x29@3x.png",
      "scale" : "3x"
    },
    {
      "size" : "40x40",
      "idiom" : "iphone",
      "filename" : "appIcon40x40@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "40x40",
      "idiom" : "iphone",
      "filename" : "appIcon40x40@3x.png",
      "scale" : "3x"
    },
    {
      "size" : "60x60",
      "idiom" : "iphone",
      "filename" : "appIcon60x60@2x.png",
      "scale" : "2x"
    },
    {
      "size" : "60x60",
      "idiom" : "iphone",
      "filename" : "appIcon60x60@3x.png",
      "scale" : "3x"
    }
  ],
  "info" : {
    "version" : 1,
    "author" : "mgfjxxiexiaolong@gmial.com"
  }
}
'''
f = open(outPutPath + 'Contents.json', 'w')
f.write(content)

print('\033[7;32m' + '文件输出文件夹：' + outPutPath + '\033[0m')
os.system('open ' + outPutPath)
