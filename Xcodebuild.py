# -*- coding: utf-8 -*-

import os,sys
import time
import re

class Xcodebuild(object):

    packMethod = 'development'

    def __init__(self):
        self.archivePath = ''
        self.outPutPath = ''
        self.appName = ''
        self.ipaPath = ''

    @property
    def existWorkspace(self):
        workspace = os.popen('find . -maxdepth 1 -name *.xcworkspace -print')
        workspaceName = workspace.read()
        if workspaceName:
            return True
        else:
            return False

    @property
    def projectName(self):
        workspace = os.popen('find . -maxdepth 1 -name *.xcworkspace -print')
        workspaceName = workspace.read()[2:]
        if not workspaceName:
            project = os.popen('find . -maxdepth 1 -name *.xcodeproj -print')
            projectName = project.read()[2:]
            if not projectName:
                print ('\033[7;31m' + '脚本所在目录没有xcode项目，请检查脚本所在目录。' + '\033[0m')
                quit()
            else:
                return projectName
        else:
            return workspaceName

    # 打包
    def archiveAndExportProject(self):
        os.system('xcodebuild clean')
        name = ''
        archiveSucess = False
        if self.existWorkspace:
            name = self.projectName[:-13]
            archiveSucess = self.__archiveWithWorkspace(name)
        else:
            name = self.projectName[:-11]
            archiveSucess = self.__archiveWithProject(name)

        self.appName = name

        if archiveSucess:
            self.exportByZipApp()
        else:
            print ('\033[7;31m' + '归档失败,请检查证书配置.' + '\033[0m')

    # 通过zip打包归档文件内的.app文件的方式导出ipa
    def exportByZipApp(self):
        payloadPath = 'Payload'
        appPath = os.path.join(self.archivePath,'Products/Applications/%s.app' % self.appName)
        ipaPath = self.appName + '.ipa'
        cmd = 'mkdir %s&&cp -r %s %s&&zip -r %s %s' %(payloadPath, appPath, payloadPath, ipaPath, payloadPath)
        print('cmd = ' + cmd)
        success = os.system(cmd)
        if success == 0:
            os.system('mkdir %s' % self.outPutPath)
            cpCmd = 'cp -r %s %s %s' % (self.archivePath, ipaPath, self.outPutPath)
            print('cpCmd = ' + cpCmd)
            os.system(cpCmd)
            os.system('open ' + self.outPutPath)
            self.ipaPath = os.path.join(self.outPutPath, ipaPath)
            print('\033[7;32m' + '打包完成,请到%s获取ipa文件' % self.outPutPath + '\033[0m')
        else:
            print ('\033[7;31m' + '打包失败,请检查证书配置.' + '\033[0m')
        # 删除打包产生的文件和文件夹
        deleteCmd = 'rm -rf build %s %s %s' % (ipaPath, self.archivePath, payloadPath)
        print('deleteCmd = ' + deleteCmd)
        os.system(deleteCmd)

    # 用xcodebuild -exportArchive讲归档文件打包成ipa文件
    def exportByXcodebuild(self):
        ipaPath = self.appName + '.ipa'
        self.prepareExportPlist()
        exportCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath ./ -exportOptionsPlist export.plist' % (self.archivePath)
        print('exportCmd = ' + exportCmd)
        exportSuccess = os.system(exportCmd)
        if exportSuccess == 0:
            os.system('mkdir %s' % self.outPutPath)
            cpCmd = 'cp -r %s %s %s' % (self.archivePath, ipaPath, self.outPutPath)
            print('cpCmd = ' + cpCmd)
            os.system(cpCmd)
            os.system('open ' + self.outPutPath)
            self.ipaPath = os.path.join(self.outPutPath, ipaPath)
            print('\033[7;32m' + '打包完成,请到%s获取ipa文件' % self.outPutPath + '\033[0m')
        else:
            print ('\033[7;31m' + '打包失败,请检查证书配置.' + '\033[0m')
        # 删除打包产生的文件和文件夹
        deleteCmd = 'rm -rf build %s %s' % (ipaPath, self.archivePath)
        print('deleteCmd = ' + deleteCmd)
        os.system(deleteCmd)

    # 归档.xcworkspace文件
    def __archiveWithWorkspace(self,name):
        print('hehe')

    # 归档.xcodeproj文件
    def __archiveWithProject(self,name):
        self.outPutPath = self.getOutPutPath(name)
        archivePath = name + '.xcarchive'
        self.archivePath = archivePath
        archiveCmd = 'xcodebuild archive -scheme %s -configuration "Release" -archivePath %s' % (name, archivePath)
        print(archiveCmd)
        archiveSuccess = os.system(archiveCmd)
        if archiveSuccess == 0:
            return True
        else:
            return False

    # 生产ipa和归档文件路径,用于完成后存放
    def getOutPutPath(self,name):
        if not self.outPutPath:
            outPutPath = os.environ['HOME']
            outPutPath = os.path.join(outPutPath, 'Desktop')
            outPutPath = os.path.join(outPutPath, name + self.getCurrentTime())
            self.outPutPath = outPutPath
        return self.outPutPath

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    def prepareExportPlist(self):
        # 若使用exportByXcodebuild方法导出ipa需配置packMethod,可选配置有: app-store, ad-hoc, package, enterprise, development, developer-id
        packMethod = 'development'
        content = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>compileBitcode</key>
	<false/>
	<key>embedOnDemandResourcesAssetPacksInBundle</key>
	<true/>
	<key>iCloudContainerEnvironment</key>
	<string>com.apple.developer.icloud-container-environment</string>
	<key>manifest</key>
	<dict>
		<key>appURL</key>
		<string>www.apple.com</string>
		<key>displayImageURL</key>
		<string>www.apple.com</string>
		<key>fullSizeImageURL</key>
		<string>www.apple.com</string>
		<key>assetPackManifestURL</key>
		<string>www.apple.com</string>
	</dict>
	<key>method</key>
	<string>%s</string>
	<key>thinning</key>
	<string>&lt;none&gt;</string>
	<key>uploadBitcode</key>
	<false/>
	<key>uploadSymbols</key>
	<false/>
</dict>
</plist>'''% packMethod

        f = open('export.plist','w')
        f.write(content)
        f.close()

