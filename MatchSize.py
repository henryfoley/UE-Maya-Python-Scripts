# import MatchSize
# import importlib
# importlib.reload(MatchSize)
# MatchSize.showUI()

import sys

import shiboken2
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance
from functools import partial

import maya.cmds as cmds
import maya.OpenMayaUI as omui

windowName = 'Match Size'
objects = cmds.ls(selection=True)[:2]

# Make sure we have only two objects selected
if len(objects) != 2:
    raise ValueError("Please select two objects")

originalPos = cmds.xform(objects[0], query=True, ws=True, translation=True)
print(originalPos)


def matchSize(comboBoxInput):
    # cmds.makeIdentity(*objects, apply=True, scale=True)
    # cmds.makeIdentity(*objects, apply=True, t=True)

    stackAxis = ['x', 'y', ' z']

    scaleAxis = 'z'
    uniform = True
    bestFit = True

    # Stack Based on Axis
    # matchScale(*objects, scaleAxis, uniform, bestFit)

    newPos = cmds.xform(objects[0], query=True, ws=True, translation=True)

    # Stack Based on Axis
    if comboBoxInput[0] == 'None':
        cmds.move(originalPos[0], 0, 0, objects[0], ws=True)
        print('return to original pos: ' + str(newPos))
    else:
        stack(*objects, stackAxis[0], comboBoxInput[0], comboBoxInput[1])
    if comboBoxInput[2] == 'None':
        cmds.move(0, originalPos[1], 0, objects[0], ws=True)
        print('return to original pos: ' + str(newPos))
    else:
        stack(*objects, stackAxis[1], comboBoxInput[2], comboBoxInput[3])
    if comboBoxInput[4] == 'None':
        cmds.move(0, 0, originalPos[2], objects[0], ws=True)
        print('return to original pos: ' + str(newPos))
    else:
        stack(*objects, stackAxis[2], comboBoxInput[4], comboBoxInput[5])

    """for i, axis in enumerate(['X', 'Y', 'Z']):
        moveValues = [0] * len(originalPos)
        moveValues[i] = originalPos[i]
        if comboBoxInput[2 * i] == 'None':
            # cmds.move(*moveValues, objects[0], ws=True)
            print(f'return to original pos: {newPos}')
        else:
            stack(*objects, stackAxis[i], comboBoxInput[2 * i], comboBoxInput[2 * i + 1])"""


def stack(targetObject, boundObject, axis, target, bound):
    # USE LISTS FOR FINAL
    boundXMin, boundYMin, boundZMin, boundXMax, boundYMax, boundZMax = cmds.xform(boundObject, query=True, bb=True,
                                                                                  os=True)
    targetXMin, targetYMin, targetZMin, targetXMax, targetYMax, targetZMax = cmds.xform(targetObject, query=True,
                                                                                        bb=True, os=True)
    targetTransformValues = getTransforms(targetObject)

    # Calculate the position of the target object based on axis
    if axis == 'x':
        targetPositions = {
            'Max': targetXMax,
            'Min': targetXMin,
            'Center': (targetXMax + targetXMin) / 2
        }
    elif axis == 'y':
        targetPositions = {
            'Max': targetYMax,
            'Min': targetYMin,
            'Center': (targetYMax + targetYMin) / 2
        }
    elif axis == 'z':
        targetPositions = {
            'Max': targetZMax,
            'Min': targetZMin,
            'Center': (targetZMax + targetZMin) / 2
        }

    # Calculate the position of the bounding object based on axis
    if axis == 'x':
        boundPositions = {
            'Max': boundXMax,
            'Min': boundXMin,
            'Center': (boundXMax + boundXMin) / 2
        }
    elif axis == 'y':
        boundPositions = {
            'Max': boundYMax,
            'Min': boundYMin,
            'Center': (boundYMax + boundYMin) / 2
        }
    elif axis == 'z':
        boundPositions = {
            'Max': boundZMax,
            'Min': boundZMin,
            'Center': (boundZMax + boundZMin) / 2
        }

    # Generate New Positions
    newPos = boundPositions[bound] - targetPositions[target]

    # Set the position of the target object based on axis
    if axis == 'x':
        cmds.move(newPos, targetTransformValues[1], targetTransformValues[2], targetObject, ws=True)
    elif axis == 'y':
        cmds.move(targetTransformValues[0], newPos, targetTransformValues[2], targetObject, ws=True)
    elif axis == 'z':
        cmds.move(targetTransformValues[0], targetTransformValues[1], newPos, targetObject, ws=True)


def getBounds(object):
    # Get bounding box of the target object
    boundingInformation = cmds.xform(object, query=True, bb=True, ws=True)
    targetWidth = boundingInformation[3] - boundingInformation[0]
    targetHeight = boundingInformation[4] - boundingInformation[1]
    targetDepth = boundingInformation[5] - boundingInformation[2]
    targetWidthCenter = targetWidth / 2
    targetHeightCenter = targetHeight / 2
    targetDepthCenter = targetDepth / 2

    # Create a list to store bounds information]
    results = [targetWidth, targetHeight, targetDepth, targetWidthCenter, targetHeightCenter, targetDepthCenter]

    # Return Value
    return results

def getTransforms(object):
    # Create list to store all transform values
    transformValues = []

    # Get Transform Values of the Target and Bound Objects
    objectTranslation = cmds.xform(object, query=True, translation=True)
    objectRotation = cmds.xform(object, query=True, rotation=True)

    # Add bound variables to the list
    for element in objectTranslation:
        transformValues.append(element)
    for element in objectRotation:
        transformValues.append(element)

    # Return Values
    return transformValues


def matchScale(targetObject, boundObject, axis, uniform, bestFit):
    targetBoundingInformation = getBounds(targetObject)
    boundBoundingInformation = getBounds(boundObject)

    scaleValues = [boundBoundingInformation[0] / targetBoundingInformation[0],
                   boundBoundingInformation[1] / targetBoundingInformation[1],
                   boundBoundingInformation[2] / targetBoundingInformation[2]]

    bestFitScale = min(scaleValues)
    # Calculate the scale factors to match the size of the bounding
    scaleByAxis = {
        'x': scaleValues[0],
        'y': scaleValues[1],
        'z': scaleValues[2]
    }
    scaleAttrib = {
        'x': ".scaleX",
        'y': ".scaleY",
        'z': ".scaleZ"
    }

    # Set scale of the target object
    if uniform == True:
        if bestFit == True:
            cmds.setAttr(targetObject + scaleAttrib['x'], bestFitScale)
            cmds.setAttr(targetObject + scaleAttrib['y'], bestFitScale)
            cmds.setAttr(targetObject + scaleAttrib['z'], bestFitScale)
        else:
            cmds.setAttr(targetObject + scaleAttrib['x'], scaleByAxis[axis])
            cmds.setAttr(targetObject + scaleAttrib['y'], scaleByAxis[axis])
            cmds.setAttr(targetObject + scaleAttrib['z'], scaleByAxis[axis])

    else:
        cmds.setAttr(targetObject + scaleAttrib[axis], scaleByAxis[axis])


# Return the Maya main window widget as a Python object
def mayaMainWindow():
    mainWindowPtr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)


class TestDialog(QtWidgets.QDialog):

    def __init__(self, parent=mayaMainWindow()):
        super(TestDialog, self).__init__(parent)

        self.sliders = []
        self.sliderValues = [0, 0, 0]
        self.setWindowTitle(windowName)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(600, 500)

        # Remove Question Mark in Window
        if sys.version_info.major >= 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            self.setWindowFlag(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayouts()
        self.getValues()

        # Set connections for Check Boxes
        for i in range(len(self.checkboxes)):
            self.checkboxes[i].stateChanged.connect(lambda: self.fuck())
        for i in range(len(self.scaleAxisCheckboxes)):
            self.scaleAxisCheckboxes[i].stateChanged.connect(lambda: self.fuck())

        # Set connections for Combo Boxes
        for i in range(len(self.comboBoxes)):
            self.comboBoxes[i].currentIndexChanged.connect(lambda: self.getValues())
            self.comboBoxes[i].currentIndexChanged.connect(lambda: matchSize(self.comboBoxValues))

        # Sliders
        """self.originalValues = [0,0,0]
        if any(self.originalValues[i] != self.sliderValues[i] for i in range(len(self.originalValues))):
            print("a value has changed")"""

    def fuck(self):
        print('fuck')

    def createScaleLayout(self, parent, font):
        # Create and add layout
        layout = QtWidgets.QHBoxLayout()
        parent.addLayout(layout)

        # Store Created Check Boxes
        self.scaleAxisCheckboxes = []

        # Create a checkbox for each axis
        for attr in ['X', 'Y', 'Z']:
            checkbox = QtWidgets.QCheckBox(attr)
            checkbox.setChecked(False)
            objectName = 'Scale' + attr + '_cmCheckBox'
            checkbox.setObjectName(objectName)
            layout.addWidget(checkbox)
            self.scaleAxisCheckboxes.append(checkbox)

    def createJustifyLayout(self, attribute, parent, font):
        # Create and add layout
        layout = QtWidgets.QHBoxLayout()
        parent.addLayout(layout)
        label = QtWidgets.QLabel(attribute)
        layout.addWidget(label)
        label.setFont(font)

        # Loop twice and create combo boxes
        for i in range(2):
            comboBox = QtWidgets.QComboBox()
            index = ['left', 'right']
            objectName = attribute.partition(': ')[0] + index[i] + '_cmComboBox'
            comboBox.setObjectName(objectName)
            self.comboBoxes.append(comboBox)
            text = [' to ', 'Offset by: ']
            toLabel = QtWidgets.QLabel(text[i])

            # Populate Combo Boxes
            if i == 0:
                items = ['None', 'Min', 'Center', 'Max']
                comboBox.addItems(items)
                comboBox.setCurrentIndex(items.index('None'))
            else:
                items = ['Min', 'Center', 'Max']
                comboBox.addItems(items)
                comboBox.setCurrentIndex(items.index('Center'))
            layout.addWidget(comboBox)
            layout.setAlignment(toLabel, QtCore.Qt.AlignHCenter)
            layout.addWidget(toLabel)

        # Create Pointer to Layout, set it as the parent, and create a pane layout
        layoutPtr = int(shiboken2.getCppPointer(layout)[0])
        layoutName = omui.MQtUtil.fullName(layoutPtr)
        cmds.setParent(layoutName)
        paneLayoutName = cmds.paneLayout()

        # Cmds UI
        slider = cmds.floatSliderGrp(min=-1, max=1, value=0, field=True, cc='empty')
        cmds.floatSliderGrp(slider, e=True, cc=lambda value, s=slider: self.storeSliderValue(s, value))
        self.sliders.append(slider)

        # Get the pointer to the Cmds UI, convert it into a QtWidget, and add it to the layout
        ptr = omui.MQtUtil.findControl(paneLayoutName)
        paneLayoutQt = shiboken2.wrapInstance(int(ptr), QtWidgets.QWidget)
        paneLayoutQtName = attribute.partition(': ')[0] + '_SliderValue'
        paneLayoutQt.setObjectName(paneLayoutQtName)
        layout.addWidget(paneLayoutQt)

    # Function to store slider value
    def storeSliderValue(self, slider, value):
        index = self.sliders.index(slider)
        self.sliderValues[index] = value
        print(self.sliderValues)

    def createWidgets(self):

        # Create Font
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)

        # Store Created Check Boxes
        self.checkboxes = []

        # Create Checkboxes
        for attr in ['Translate', 'Scale to Fit', 'Uniform Scale']:
            checkbox = QtWidgets.QCheckBox(attr)
            checkbox.setChecked(True)
            checkbox.setFont(font)
            newAttrName = attr.replace(" ", "")
            objectName = newAttrName + '_cmCheckBox'
            checkbox.setObjectName(objectName)
            self.checkboxes.append(checkbox)

    def createLayouts(self):
        # Create Font
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)

        mainLayout = QtWidgets.QVBoxLayout(self)

        # Create and Add to Translate Layout
        translateLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(translateLayout)

        # Add to Translate Layout
        translateLayout.addWidget(self.checkboxes[0])
        translateLayout.setAlignment(self.checkboxes[0], QtCore.Qt.AlignHCenter)

        # Store Created Combo Boxes and their values
        self.comboBoxes = []
        self.comboBoxValues = ['None', 'None', 'None', 'Center', 'Center', 'Center']

        # Create Justify Layouts
        justifyLayout = QtWidgets.QHBoxLayout()
        for attribute in ['Justify X: ', 'Justify Y: ', 'Justify Z: ']:
            justifyLayout.addLayout(self.createJustifyLayout(attribute, mainLayout, font))
        mainLayout.addLayout(justifyLayout)

        # Create and Add to Scale Layouts
        preScaleLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(preScaleLayout)
        scaleLayout = QtWidgets.QHBoxLayout()
        for i in range(2):
            i += 1
            preScaleLayout.addWidget(self.checkboxes[i])
            preScaleLayout.setAlignment(self.checkboxes[i], QtCore.Qt.AlignHCenter)
        scaleLayout.addLayout(self.createScaleLayout(mainLayout, font))
        mainLayout.addLayout(scaleLayout)

        """if self.translateCheckbox.isChecked():
            for i in range(justifyLayout.count()):
                item = justifyLayout.itemAt(i)
                item.widget().setEnabled(False)
            return True"""

    def getValues(self):

        # Get Checkbox values
        """for i in range(len(self.checkboxes)):
            print(self.checkboxes[i].objectName() + ': ' + str(self.checkboxes[i].isChecked()))

        for i in range(len(self.scaleAxisCheckboxes)):
            print(self.scaleAxisCheckboxes[i].objectName() + ': ' + str(self.scaleAxisCheckboxes[i].isChecked())))"""

        for i in range(len(self.comboBoxes)):
            self.comboBoxValues[i] = self.comboBoxes[i].currentText()
            # print(self.comboBoxValues[i]

        # Get Combo Box values
        for attribute in ['Justify X', 'Justify Y', 'Justify Z']:
            """for attr in ['left', 'right']:
                if cmds.control(attribute + attr + '_cmComboBox', exists=True):
                    ptr = omui.MQtUtil.findControl(attribute + attr + '_cmComboBox')
                    comboBox = wrapInstance(int(ptr), QtWidgets.QComboBox)
                    value = comboBox.currentText()
                    print(value)"""
        # Get Slider Values
        """if cmds.control(attribute +'_SliderValue', exists=True):
            print('Slider values found')
            for i in range(len(self.sliders)):
                print(f'Slider: {self.sliders[i]} value: {self.sliderValues[i]}')
        else:
            print('Slider values not found')"""


def showUI():
    # Check if window exists
    if cmds.window(windowName, exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI(windowName, window=True)

    myWin = TestDialog()
    myWin.setObjectName(windowName)
    myWin.show()
