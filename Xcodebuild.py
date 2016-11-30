# -*- coding: utf-8 -*-

import os,sys
import time
import re

class Xcodebuild(object):

    # __slots__ = ('name', 'age')

    def __init__(self, plistPath=None):
        self.plistPath = plistPath
        self.archivePath = ''
        self.outPutPath = ''
        self.appName = ''

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

    def archiveAndExportProject(self):
        os.system('xcodebuild clean')
        name = ''
        archiveSucess = False
        if self.existWorkspace:
            name = self.projectName[:-13]
        else:
            name = self.projectName[:-11]
            archiveSucess = self.__archiveWithProject(name)

        self.appName = name

        if archiveSucess:
            self.exportByZipApp()
        else:
            print ('\033[7;31m' + '归档失败,请检查证书配置.' + '\033[0m')

    def exportByZipApp(self):
        payloadPath = os.path.join(self.outPutPath,'Payload')
        appPath = os.path.join(self.archivePath,'Products/Applications/%s.app' % self.appName)
        ipaPath = os.path.join(self.outPutPath,self.appName)
        cmd = 'mkdir %s&&cp -r %s %s&&zip -r %s.ipa %s&& rm -rf %s' %(payloadPath, appPath, payloadPath, ipaPath, payloadPath, payloadPath)
        print('cmd = ' + cmd)
        success = os.system(cmd)
        if success == 0:
            os.system('open ' + self.outPutPath)
            print('\033[7;32m' + '打包完成,请到%s获取ipa文件' % self.outPutPath + '\033[0m')
        else:
            print ('\033[7;31m' + '打包失败,请检查证书配置.' + '\033[0m')


    def exportByXcodebuild(self):
        infoPlistPath = os.path.join(self.archivePath,'Info.plist')
        exportCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s' % (self.archivePath, self.outPutPath, infoPlistPath)
        print('exportCmd = ' + exportCmd)
        exportSuccess = os.system(exportCmd)
        if exportSuccess == 0:
            os.system('open ' + self.outPutPath)
            print('\033[7;32m' + '打包完成,请到%s获取ipa文件' % self.outPutPath + '\033[0m')
        else:
            print ('\033[7;31m' + '打包失败,请检查证书配置.' + '\033[0m')

    def __archiveWithWorkspace(self,name):
        print('hehe')

    def __archiveWithProject(self,name):
        self.outPutPath = self.getOutPutPath(name)
        archivePath = os.path.join(self.outPutPath, name + '.xcarchive')
        self.archivePath = archivePath
        archiveCmd = 'xcodebuild archive -scheme %s -configuration "Release" -archivePath %s|tee archiveInfo.txt' % (name, archivePath)
        print(archiveCmd)
        archiveSuccess = os.system(archiveCmd)
        if archiveSuccess == 0:
            self.parseArchiveInfo()
            return True
        else:
            os.system('rm archiveInfo.txt')
            return False

    def parseArchiveInfo(self):
        archiveInfoPath = os.path.join(self.currentPath(),'archiveInfo.txt')
        if os.path.exists(archiveInfoPath):
            archiveInfo = open(archiveInfoPath,'r')
            regex = ur"ProcessInfoPlistFile (.*)"
            regexObj = re.search(regex,archiveInfo.read())
            if regexObj:
                plists = regexObj.group(1)
                arr = plists.split(' ')
                self.plistPath = arr[-1]

    def getOutPutPath(self,name):
        if not self.outPutPath:
            outPutPath = os.environ['HOME']
            outPutPath = os.path.join(outPutPath, 'Desktop')
            outPutPath = os.path.join(outPutPath, name + self.getCurrentTime())
            return outPutPath

    # 获取当前时间
    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    # 获取脚本文件的当前路径
    def currentPath(self):
        return os.getcwd()


xcode = Xcodebuild()
xcode.archiveAndExportProject()
print(xcode.plistPath)
print(xcode.outPutPath)
print(xcode.archivePath)