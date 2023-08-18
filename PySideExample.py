#import PySideExample
#import importlib
#importlib.reload(PySideExample)
#PySideExample.showUI()


import sys
from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

windowName = 'Test Dialog'

# Return the Maya main window widget as a Python object
def mayaMainWindow():
    mainWindowPtr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >=3:
        return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle(windowName)
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 500)

        # Remove Question Mark in Window
        if sys.version_info.major >= 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            self.setWindowFlag(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayouts()

    def createWidgets(self):
        self.lineedit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox("Checkbox1")
        self.checkbox2 = QtWidgets.QCheckBox("Checkbox2")
        self.button1 = QtWidgets.QPushButton("Button1")
        self.button2 = QtWidgets.QPushButton("Button2")
        self.button2.setStyleSheet('background-color: rgd(0,210,255); border: solid black 1px')

    def createLayouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.lineedit)
        main_layout.addWidget(self.checkbox1)
        main_layout.addWidget(self.checkbox2)
        main_layout.addWidget(self.button1)
        main_layout.addWidget(self.button2)



def showUI():

    # Check if window exists
    if cmds.window(windowName, exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI(windowName, window=True)

    myWin = TestDialog()
    myWin.setObjectName(windowName)
    myWin.show()

