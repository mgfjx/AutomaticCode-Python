#!/usr/bin/env python3
# coding: utf-8

from PIL import Image
import sys

outPutPath = '/Users/xiexiaolong1/Desktop/'
ImageName = sys.argv[0]

originImg = Image.open(ImageName)
size = 100,100

# 20x20
img1 = originImg.resize((40,40))
img2 = originImg.resize((60,60))
img1.save(outPutPath + 'appIcon20x20@2x.png',"png")
img2.save(outPutPath + 'appIcon20x20@3x.png',"png")

# 29x29
img3 = originImg.resize((29,29))
img4 = originImg.resize((58,58))
img5 = originImg.resize((87,87))
img3.save(outPutPath + 'appIcon29x29.png',"png")
img4.save(outPutPath + 'appIcon29x29@2x.png',"png")
img5.save(outPutPath + 'appIcon29x29@3x.png',"png")

# 40x40
img6 = originImg.resize((80,80))
img7 = originImg.resize((120,120))
img6.save(outPutPath + 'appIcon40x40@2x.png',"png")
img7.save(outPutPath + 'appIcon40x40@3x.png',"png")

# 60x60
img8 = originImg.resize((120,120))
img9 = originImg.resize((180,180))
img8.save(outPutPath + 'appIcon60x60@2x.png',"png")
img9.save(outPutPath + 'appIcon60x60@3x.png',"png")