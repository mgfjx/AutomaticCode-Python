#! /bin/sh
cd `dirname $0` #cd到当前脚本所在目录

#获取.xcodeproj名称
projectFile=`ls | grep "\.xcodeproj$"`
projectFile=${projectFile/.xcodeproj/''}

PROJECT_NAME="$projectFile"
TARGET_NAME="$projectFile"
IPA_NAME="$projectFile.ipa" #输出文件名

xcodebuild -project ${PROJECT_NAME}.xcodeproj -target ${PROJECT_NAME} -configuration Release
if [[ $? == 0 ]]; then
	xcrun -sdk iphoneos -v PackageApplication ./build/Release-iphoneos/${PROJECT_NAME}.app -o ~/Desktop/${IPA_NAME}
	fi
	if [[ $? == 0 ]]; then
		rm -r -f build
fi