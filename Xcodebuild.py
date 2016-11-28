# -*- coding: utf-8 -*-

import os

class Xcodebuild(object):

    # __slots__ = ('name', 'age')

    def __init__(self, plistPath=None):
        self.plistPath = plistPath

    @property
    def existWorkspace(self):
        workspace = os.popen('find . -maxdepth 1 -name *.xcworkspace -print')
        workspaceName = workspace.read()
        if workspaceName:
            return True
        else:
            return False

    def getProjectName(self):
        workspace = os.popen('find . -maxdepth 1 -name *.xcworkspace -print')
        workspaceName = workspace.read()[2:]
        if not workspaceName:
            project = os.popen('find . -maxdepth 1 -name *.xcodeproj -print')
            projectName = project.read()[2:]
            if not projectName:
                print ('\033[7;31m' + '脚本所在目录没有xcode项目，请检查脚本所在目录。' + '\033[0m')
            else:
                return projectName
        else:
            return workspaceName

xcode = Xcodebuild()
if xcode.existWorkspace:
    print (xcode.getProjectName())
# print(xcode.getProjectName())