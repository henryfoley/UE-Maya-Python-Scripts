# Prefix Formatting - Maya
# Henry Foley, 2023

# import PrefixFormatting
# import importlib
# importlib.reload(PrefixFormatting)
# PrefixFormatting.displayUI()

import maya.cmds as cmds
import json
import os
import sys

prefixFormattingOptionsJson = []


def PrefixFormattingMain():
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "prefixFormattingSettings.json")
    loadJsonFile(filePath)
    PrefixFormattingUI()
    setObjectPrefix()
    assignPrefix()


def PrefixFormattingUI():
    # Delete Window if it already exists
    if cmds.window('PrefixFormattingWin', exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI('PrefixFormattingWin', window=True)

    cmds.window('PrefixFormattingWin', t="Prefix Formatting", mnb=False, mxb=False, s=False)

    cmds.columnLayout('mainUI_A', parent='PrefixFormattingWin')
    cmds.rowColumnLayout(nc=1, cw=[(1, 200)], p='mainUI_A')

    cmds.separator(h=10, style='none')
    cmds.iconTextStaticLabel(st='textOnly', l='Prefix Format Options', align='center', font='boldLabelFont')
    cmds.separator(h=10, style='none')

    cmds.rowColumnLayout('CheckBoxColumn', nc=2, cw=[(1, 100), (2, 100)], cs=[(1, 10), (2, 10)], p='mainUI_A')

    # Check Boxes
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn')
    cmds.iconTextStaticLabel(st='textOnly', l="Object Type")
    cmds.checkBox('Asset_CB', l="Asset", height=20, value=False, cc = lambda args: printSomething())
    cmds.separator(height=10, style='in')
    cmds.checkBox('Geometry_CB', l="Geometry", height=20, value=True)
    cmds.separator(height=10, style='in')
    cmds.checkBox('NURBS_Objects_CB', l="NURBS Objects", height=20, value=False)
    cmds.separator(height=10, style='in')

    # Text Fields
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn')
    cmds.iconTextStaticLabel(st='textOnly', l='Prefix')
    cmds.textField('Asset_TF', height=20)
    cmds.separator(height=10, style='in')
    cmds.textField('Geometry_TF', height=20)
    cmds.separator(height=10, style='in')
    cmds.textField('NURBS_Objects_TF', height=20)
    cmds.separator(height=10, style='in')

    cmds.showWindow('PrefixFormattingWin')


def loadJsonFile(filePath):
    global prefixFormattingOptionsJson

    if os.path.exists(filePath):
        prefixFormattingOptionsJson = json.load(open(filePath))
    else:
        # Display file not found message
        cmds.warning("Cannot find the JSON file: prefixFormattingSettings.json")

        # Open a file explorer to locate the file
        fileFilter = "JSON Files (*.json)"
        filePath = cmds.fileDialog2(dialogStyle=1, fileMode=1, cap="Load Prefix Formatting Settings File",
                                           ff=fileFilter)
        if filePath:
            return loadJsonFile(filePath[0])
        else:
            return None


def setObjectPrefix():
    cmds.textField('Asset_TF', w=5, e=True, tx=prefixFormattingOptionsJson['Asset'])
    cmds.textField('Geometry_TF', e=True, tx=prefixFormattingOptionsJson['Geometry'])
    cmds.textField('NURBS_Objects_TF', e=True, tx=prefixFormattingOptionsJson['NURBS_Objects'])
    """cmds.textField('Polygon Objects_TF', e=True, tx=prefixFormattingOptionsJson['Polygon_Objects'])
    cmds.textField('Subdiv Objects_TF', e=True, tx=prefixFormattingOptionsJson['Subdiv_Objects'])
    cmds.textField('GPU Cache_TF', e=True, tx=prefixFormattingOptionsJson['GPU_Cache'])
    cmds.textField('Cameras_TF', e=True, tx=prefixFormattingOptionsJson['Cameras'])
    cmds.textField('Joints_TF', e=True, tx=prefixFormattingOptionsJson['Joints'])"""


def assignPrefix():
    objects = cmds.ls()
    objects.sort(key=len, reverse=True)
    print(objects)


def printSomething():
    print("Something")