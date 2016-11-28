# -*- coding: utf-8 -*-

import os

class Xcodebuild(object):

    # __slots__ = ('name', 'age')

    def __init__(self, plistPath=None):
        self.plistPath = plistPath

    def existXcworkspaceFile(self):
        workspace = os.popen('find . -maxdepth 1 -name *.xcworkspace -print')
        path = workspace.read()
        if not path:
            return

xcode = Xcodebuild()
print(xcode.existXcworkspaceFile())