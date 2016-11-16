#!/bin/sh

echo "the number of parameters is $#"

# 20x20
sips -s format png -z 40 40 $1 --out appIcon20x20@2x.png
sips -s format png -z 60 60 $1 --out appIcon20x20@3x.png

# 29x29
sips -s format png -z 29 29 $1 --out appIcon29x29.png
sips -s format png -z 58 58 $1 --out appIcon29x29@2x.png
sips -s format png -z 87 87 $1 --out appIcon29x29@3x.png

# 40x40
sips -s format png -z 80 80 $1 --out appIcon40x40@2x.png
sips -s format png -z 120 120 $1 --out appIcon40x40@3x.png

# 60x60
sips -s format png -z 120 120 $1 --out appIcon60x60@2x.png
sips -s format png -z 180 180 $1 --out appIcon60x60@3x.png