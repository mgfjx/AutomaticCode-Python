#!/bin/sh

# iPhone Portrait iOS 8-Retina HD 5.5 （1242×2208） @3x
# iPhone Portrait iOS 8-Retina HD 4.7 （750×1334） @2x

# iPhone Portrait iOS 7,8-2x （640×960） @2x
# iPhone Portrait iOS 7,8-Retina 4 （640×1136） @2x

# iPhone Portrait iOS 5,6-1x （320×480） @1x
# iPhone Portrait iOS 5,6-2x （640×960） @2x
# iPhone Portrait iOS 5,6-Retina4 （640×1136） @2x

# 3.5寸屏幕
sips -s format png -z 480 320 launchImag.png --out launchImage3_5.png
sips -s format png -z 960 640 launchImag.png --out launchImage3_5@2x.png

# 4.0寸屏幕
sips -s format png -z 1136 640 launchImag.png --out launchImage4_0@2x.png

# 4.7寸屏幕
sips -s format png -z 1334 750 launchImag.png --out launchImage4_7@2x.png

# 5.5寸屏幕
sips -s format png -z 2208 1242 launchImag.png --out launchImage5_5@3x.png