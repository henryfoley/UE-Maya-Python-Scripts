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
    cmds.button(l='Assign Prefixes', command=lambda args:sortObjects(getObjects()))
    cmds.separator(h=10, style='none')
    cmds.button(l='Remove Prefixes', command=lambda args:removeAllPrefixes(getObjects()))
    cmds.separator(h=10, style='none')

    cmds.rowColumnLayout('CheckBoxColumn', nc=2, cw=[(1, 100), (2, 100)], cs=[(1, 10), (2, 10)], p='mainUI_A')

    # Check Boxes
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn')
    cmds.iconTextStaticLabel(st='textOnly', l="Object Type")
    cmds.checkBox('Asset_CB', l="Asset", height=20, value=False, cc = lambda args: printSomething())
    cmds.separator(height=10, style='in')
    cmds.checkBox('Mesh_CB', l="Mesh", height=20, value=True)
    cmds.separator(height=10, style='in')
    cmds.checkBox('NURBS_Objects_CB', l="NURBS Objects", height=20, value=False)
    cmds.separator(height=10, style='in')

    # Text Fields
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn')
    cmds.iconTextStaticLabel(st='textOnly', l='Prefix')
    cmds.textField('Asset_TF', height=20)
    cmds.separator(height=10, style='in')
    cmds.textField('Mesh_TF', height=20)
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
    cmds.textField('Mesh_TF', e=True, tx=prefixFormattingOptionsJson['Mesh'])
    cmds.textField('NURBS_Objects_TF', e=True, tx=prefixFormattingOptionsJson['NURBS_Objects'])
    """cmds.textField('Polygon Objects_TF', e=True, tx=prefixFormattingOptionsJson['Polygon_Objects'])
    cmds.textField('Subdiv Objects_TF', e=True, tx=prefixFormattingOptionsJson['Subdiv_Objects'])
    cmds.textField('GPU Cache_TF', e=True, tx=prefixFormattingOptionsJson['GPU_Cache'])
    cmds.textField('Cameras_TF', e=True, tx=prefixFormattingOptionsJson['Cameras'])
    cmds.textField('Joints_TF', e=True, tx=prefixFormattingOptionsJson['Joints'])"""


def getObjects():
    objectList = cmds.ls(shapes=True, materials=True)
    objectList.sort()
    return objectList


def classifyObject(object):
    classification = cmds.objectType(object)
    return classification


def sortObjects(objects):
    for obj in objects:
        classification = classifyObject(obj)
        if classification == 'nurbsSurface':
            assignPrefix(prefixFormattingOptionsJson['NURBS_Objects'], obj)
            # assignPrefix()


def assignPrefix(prefix, obj):
    if prefix in obj:
        print('Prefix assigned to ' + obj)
        cmds.select(obj)
        print("Prefix already included")
        return

    print('Prefix assigned to ' + obj)

    # Change name of objects Transform
    objectTransform = cmds.listRelatives(obj, parent=True, fullPath=True)
    for i in objectTransform:
        if prefix in i:
            print('Prefix already in object transform')
            continue
        reformattedName = i.removeprefix('|')
        newTransformName = prefix + "_" + reformattedName
        print("New Transform Name: " + newTransformName)
        cmds.rename(i, newTransformName)

    # Change name of object
    newObjectName = prefix + "_" + obj
    print("New Object Name: " + newObjectName)
    cmds.rename(obj, newObjectName)


def removeAllPrefixes(objects):
    for obj in objects:
        classification = classifyObject(obj)
        if classification == 'nurbsSurface':
            removeTransformPrefix(prefixFormattingOptionsJson['NURBS_Objects'], obj)
            removeObjectPrefix(prefixFormattingOptionsJson['NURBS_Objects'], obj)


def removeObjectPrefix(prefix, obj):
    if prefix in obj:
        prefix += '_'
        print('Removing this prefix: ' + prefix)
        print('Objects current name: ' + obj)
        newName = obj.removeprefix(prefix)
        cmds.rename(obj, newName)
        print('Prefix removed from: ' + newName)
        return


def removeTransformPrefix(prefix, obj):
    objectTransform = cmds.listRelatives(obj, parent=True, fullPath=True)
    for i in objectTransform:
        if prefix in i:
            reformattedName = i.removeprefix('|')
            prefix += '_'
            print('Removing this prefix: ' + prefix)
            print('Transforms current name: ' + reformattedName)
            newName = reformattedName.removeprefix(prefix)
            cmds.rename(i, newName)
            print('Prefix removed from: ' + newName)


def printSomething():
    print("Something")