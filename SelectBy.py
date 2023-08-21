# Select By
# Henry Foley, 2023

# import SelectBy
# import importlib
# importlib.reload(SelectBy)
# SelectBy.displayUI()

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaUI as omu
from enum import Enum


class SelectMode(Enum):
    VERTEX = 1
    EDGE = 2
    FACE = 3
    OBJ = 4


currentSelectMode = None


def displayUI():
    myUI()


def myUI():
    # Delete Window if it already exists
    if cmds.window('SelectBy', exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI('SelectBy', window=True)

    # Create two main columns
    cmds.window('SelectBy')
    cmds.rowColumnLayout('mainWindow', nc=2, cw=[(1, 500), (2, 500)], cs=[(1, 10), (2, 10)])
    cmds.columnLayout('mainUI_A', p='mainWindow')
    cmds.columnLayout('mainUI_B', p='mainWindow')

    # Create layout with Maya Outliner in it
    cmds.frameLayout(labelVisible=False, width=500, height=300, p='mainUI_A')
    shapeFilter = cmds.itemFilter(bt='shape')
    panel = cmds.outlinerPanel()
    outliner = cmds.outlinerPanel(panel, query=True, outlinerEditor=True)
    myOut = cmds.outlinerEditor(outliner, edit=True, setFilter=shapeFilter, filter=shapeFilter)
    cmds.control(myOut, edit=True)
    cmds.setParent('..')
    cmds.separator(h=10, style='none')

    # Create Layout for Selected Objects
    cmds.iconTextStaticLabel(st='textOnly', l='Selected Objects')

    cmds.scriptJob(e=['SelectionChanged', refreshUI])

    # Initial UI refresh
    refreshUI()

    # Init Selection Mode
    global currentSelectMode
    currentSelectMode = SelectMode.OBJ

    # Selection Modes
    cmds.rowColumnLayout(nc=3, cw=[(1, 100), (2, 100), (3, 100)], cs=[(1, 10), (2, 10), (3, 10)], p='mainUI_B')
    cmds.button(l='Vertices Selection', c=lambda args: selectVerts())
    cmds.button(l='Edge Selection', c=lambda args: selectEdge())
    cmds.button(l='Face Selection', c=lambda args: selectFace())
    cmds.button(l='Obj Selection', c=lambda args: selectObj())

    # Selection Tabs
    cmds.frameLayout('selectTabs', labelVisible=False, width=500, height=400, p='mainUI_B')

    tabs = cmds.tabLayout(p='selectTabs')
    # add first tab
    firstTab = cmds.columnLayout()
    cmds.tabLayout(tabs, edit=True, tabLabel=[firstTab, 'Normals'])
    cmds.button(label='Select Hard Edges', c='cmds.polySelectConstraint(m=3,t=0x8000, sm=1)')
    cmds.button(label='Select Soft Edges', c='cmds.polySelectConstraint(m=3,t=0x8000, sm=2)')

    slider = cmds.floatSliderGrp(min=-1, max=1, value=0, field=True, cc='empty')
    cmds.floatSliderGrp(slider, e=True, cc=lambda value, s=slider: storeSliderValue(s, value))

    cmds.setParent('..')

    # Poly Tab
    newLayout = cmds.columnLayout()
    cmds.tabLayout(tabs, edit=True, tabLabel=[newLayout, 'Polys'])
    cmds.columnLayout()

    cmds.button(label='Select non-manifold geo', c=lambda args: selectNGons())

    cmds.setParent('..')
    cmds.setParent('..')

    # Size Tab
    sizeTab = cmds.columnLayout()
    cmds.tabLayout(tabs, edit=True, tabLabel=[sizeTab, 'Size'])
    cmds.button(label='Button')
    cmds.setParent('..')

    # Name Tab
    nameTab = cmds.columnLayout()
    cmds.tabLayout(tabs, edit=True, tabLabel=[nameTab, 'Name'])
    cmds.button(label='Button', c=lambda args: print(currentSelectMode))

    # Select All
    cmds.button(label='Select All', c=lambda args: cmds.select(selectAll()))

    # Select Visible
    cmds.button(label='Select Visible', c=lambda args: cmds.select(visibleObjects()))

    # Select Non-Visible
    cmds.button(label='Select Non-Visible', c=lambda args: cmds.select(inverse(visibleObjects())))

    # Select From Camera View
    cmds.button(label='Select From Camera View', c=lambda args: cmds.select(selectFromCamera()))

    # Select From Not in Camera View
    cmds.button(label='Select From Not in Camera View', c=lambda args: cmds.select(inverse(selectFromCamera())))
    cmds.setParent('..')
    cmds.showWindow('SelectBy')


def selectNGons():
    cmds.polySelectConstraint(m=3, t=8, sz=3)
    cmds.polySelectConstraint(dis=True)
    print('Ngons Selected')


def selectAll():
    shapeList = cmds.ls(typ='mesh', g=True)
    parentTransforms = cmds.listRelatives(shapeList, parent=True, fullPath=True)
    return parentTransforms


def visibleObjects():
    shapeList = cmds.ls(typ='mesh', g=True, v=True)
    parentTransforms = cmds.listRelatives(shapeList, parent=True, fullPath=True)
    return parentTransforms


def inverse(selectedObjects):
    allObjects = selectAll()
    nonSelectedObjects = list(set(allObjects).difference(selectedObjects))
    return nonSelectedObjects


def selectVerts():
    global currentSelectMode
    vertices = cmds.polyListComponentConversion(toVertex=True)
    cmds.select(vertices)
    currentSelectMode = SelectMode.VERTEX
    print(currentSelectMode)


def selectEdge():
    global currentSelectMode
    edges = cmds.polyListComponentConversion(toEdge=True)
    cmds.select(edges)
    currentSelectMode = SelectMode.EDGE


def selectFace():
    global currentSelectMode
    faces = cmds.polyListComponentConversion(toFace=True)
    cmds.select(faces)
    currentSelectMode = SelectMode.FACE


def selectObj():
    global currentSelectMode
    faces = cmds.polyListComponentConversion(toObject=True)
    cmds.select(faces)
    currentSelectMode = SelectMode.OBJ


def selectFromCamera():
    view = omu.M3dView.active3dView()
    om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)

    # Convoluted way of doing this, but hey it works ¯\_(ツ)_/¯
    shapeList = cmds.ls(selection=True)
    objectNames = cmds.listRelatives(shapeList, pa=True)
    parentTransforms = cmds.listRelatives(objectNames, parent=True, fullPath=True)

    return parentTransforms


def storeSliderValue(slider, value):
    sliderValues = [0, 0, 0]
    index = slider.index(slider)
    sliderValues[index] = value
    print(sliderValues)


def refreshUI():
    # Clear the existing UI contents
    if cmds.scrollLayout('selectedObjects', exists=True):
        cmds.deleteUI('selectedObjects', control=True)

    # Display list of currently selected objects
    selected_objects = cmds.ls(selection=True)

    if selected_objects:
        # Create a layout to hold the text
        cmds.scrollLayout('selectedObjects', w=500, h=100, p='mainUI_A', cr=True, ebg=True, bgc=[1, 0, 0])

        # Add a text label for each selected object
        for obj in selected_objects:
            cmds.text(label=obj, p='selectedObjects')
    else:
        cmds.warning("No objects selected.")
