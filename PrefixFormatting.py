# Prefix Formatting - Maya
# Henry Foley, 2023

# import PrefixFormatting
# import importlib
# importlib.reload(PrefixFormatting)
# PrefixFormatting.PrefixFormattingMain()

import maya.cmds as cmds
import json
import os

prefixFormattingOptionsJson = []


def PrefixFormattingMain():
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "prefixFormattingSettings.json")
    loadJsonFile(filePath)
    PrefixFormattingUI()
    initObjectPrefix()


def PrefixFormattingUI():
    # Delete Window if it already exists
    if cmds.window('PrefixFormattingWin', exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI('PrefixFormattingWin', window=True)

    # Main Layouts
    cmds.window('PrefixFormattingWin', t="Prefix Formatting", mnb=False, mxb=False, s=False)
    cmds.columnLayout('mainUI_A', parent='PrefixFormattingWin')
    cmds.columnLayout('ButtonsColumn', parent='mainUI_A', cal="center")

    # Button Layouts
    cmds.frameLayout(labelVisible=False, width=400, la='center', p='ButtonsColumn')
    cmds.iconTextStaticLabel(st='textOnly', l='Prefix Format Options', align='center', font='boldLabelFont')
    cmds.button(l='Assign Prefixes', command=lambda args: assignAllPrefixes(getObjects()))
    cmds.button(l='Remove Prefixes', command=lambda args: removeAllPrefixes(getObjects()))
    cmds.button(l='Revert Prefixes', command=lambda args: initObjectPrefix())
    cmds.separator(h=10, style='none')

    # Columns
    cmds.rowColumnLayout('CheckTextParent', nc=4, cw=[(1, 100), (2, 100), (3, 100), (4, 100)], p='mainUI_A')
    cmds.rowColumnLayout('TextBoxColumn_1', nc=1, cw=[(1, 100)], p='CheckTextParent')
    cmds.rowColumnLayout('CheckBoxColumn_1', nc=1, cw=[(1, 100)], p='CheckTextParent')
    cmds.rowColumnLayout('TextBoxColumn_2', nc=1, cw=[(1, 100)], p='CheckTextParent')
    cmds.rowColumnLayout('CheckBoxColumn_2', nc=1, cw=[(1, 100)], p='CheckTextParent')

    cmds.rowColumnLayout('SelectColumn', nc=1, cw=[(1, 400)], p='mainUI_A')

    # Text Fields Column 1
    cmds.frameLayout(labelVisible=False, width=75, p='TextBoxColumn_1')
    cmds.textField('Mesh_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('ImagePlane_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('NURBS_Objects_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('NURBS_Curve_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Cameras_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Asset_TF', height=20, w=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Joints_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Sets_TF', height=20)
    cmds.separator(height=3, style='in')

    # Text Fields Column 2
    cmds.frameLayout(labelVisible=False, width=75, p='TextBoxColumn_2')
    cmds.textField('Lights_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Locator_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Material_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('MASH_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('ConstructionPlane_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('Volume_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('IkHandles_TF', height=20)
    cmds.separator(height=3, style='in')
    cmds.textField('ParticleCloud_TF', height=20)
    cmds.separator(height=3, style='in')

    # Check Boxes Column 1
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn_1')
    cmds.checkBox('Mesh_CB', l="Mesh", height=20, value=True)
    cmds.separator(height=3, style='in')
    cmds.checkBox('ImagePlane_CB', l="Image Plane", height=20, value=True)
    cmds.separator(height=3, style='in')
    cmds.checkBox('NURBS_Objects_CB', l="NURBS Objects", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('NURBS_Curve_CB', l="NURBS Curve", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Cameras_CB', l="Cameras", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Asset_CB', l="Asset", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Joints_CB', l="Joints", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Sets_CB', l="Sets", height=20, value=False)
    cmds.separator(height=3, style='in')

    # Check Boxes Column 2
    cmds.frameLayout(labelVisible=False, width=75, p='CheckBoxColumn_2')
    cmds.checkBox('Lights_CB', l="Lights", height=20, value=True)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Locator_CB', l="Locator", height=20, value=True)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Material_CB', l="Material", height=20, value=True)
    cmds.separator(height=3, style='in')
    cmds.checkBox('MASH_CB', l="MASH", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('ConstructionPlane_CB', l="Construction P.", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('Volume_CB', l="Volume", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('IkHandles_CB', l="Ik Handles", height=20, value=False)
    cmds.separator(height=3, style='in')
    cmds.checkBox('ParticleCloud_CB', l="Particle Cloud", height=20, value=False)
    cmds.separator(height=3, style='in')

    # Selection Prefixes
    cmds.frameLayout(labelVisible=False, width=100, p='SelectColumn')
    cmds.iconTextStaticLabel(st='textOnly', l='Selection Prefix/Suffx', align='center', font='boldLabelFont')
    cmds.rowLayout(nc=3, cw3=[110, 100, 100], h=50, p='SelectColumn')
    cmds.separator()
    cmds.radioCollection('rc_PrefixSuffix')
    cmds.radioButton('PrefixRadio', l='Prefix', sl=True)
    cmds.radioButton('SuffixRadio', l='Suffix')
    cmds.frameLayout(labelVisible=False, width=100, p='SelectColumn')
    cmds.textField('Selection_TF', text='Default', height=20)
    cmds.button(l='Assign', command=lambda args: assignSelection(getSelectedObjects()))
    cmds.button(l='Remove', command=lambda args: removeSelection(getSelectedObjects()))

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


def initObjectPrefix():
    cmds.textField('Mesh_TF', e=True, tx=prefixFormattingOptionsJson['Mesh'])
    cmds.textField('Lights_TF', e=True, tx=prefixFormattingOptionsJson['Lights'])
    cmds.textField('ImagePlane_TF', e=True, tx=prefixFormattingOptionsJson['Image_Plane'])
    cmds.textField('Locator_TF', e=True, tx=prefixFormattingOptionsJson['Locator'])
    cmds.textField('NURBS_Objects_TF', e=True, tx=prefixFormattingOptionsJson['NURBS_Objects'])
    cmds.textField('Material_TF', e=True, tx=prefixFormattingOptionsJson['Material'])
    cmds.textField('NURBS_Curve_TF', e=True, tx=prefixFormattingOptionsJson['NURBS_Curve'])
    cmds.textField('MASH_TF', e=True, tx=prefixFormattingOptionsJson['MASH'])
    cmds.textField('Cameras_TF', e=True, tx=prefixFormattingOptionsJson['Cameras'])
    cmds.textField('ConstructionPlane_TF', e=True, tx=prefixFormattingOptionsJson['Construction_Plane'])
    cmds.textField('Asset_TF', w=5, e=True, tx=prefixFormattingOptionsJson['Asset'])
    cmds.textField('Volume_TF', e=True, tx=prefixFormattingOptionsJson['Volume'])
    cmds.textField('Joints_TF', e=True, tx=prefixFormattingOptionsJson['Joints'])
    cmds.textField('IkHandles_TF', e=True, tx=prefixFormattingOptionsJson['IkHandles'])
    cmds.textField('Sets_TF', e=True, tx=prefixFormattingOptionsJson['Sets'])
    cmds.textField('ParticleCloud_TF', e=True, tx=prefixFormattingOptionsJson['Particle_Cloud'])


def getObjects():
    # For some reason setting containers to True in the object list prevents sets and shapes from
    # being selected. This a stupid fix, but hey it works
    objectList = cmds.ls(shapes=True, materials=True, sets=True,
                         type=['joint', 'ikRPsolver', 'ikSCsolver', 'ikSplineSolver', 'ikSystem'])
    containerList = cmds.ls(con=True)
    objectList += containerList
    return objectList


def getSelectedObjects():
    objectList = cmds.ls(selection=True)
    objectList.sort()
    return objectList


def classifyObject(obj):
    try:
        classification = cmds.objectType(obj)
        return classification
    except:
        cmds.warning(str(obj) + " cannot be classified! Skipping object!")
    # print(classification)


def assignAllPrefixes(objects):
    for obj in objects:
        classification = classifyObject(obj)
        if classification == 'mesh' and cmds.checkBox('Mesh_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Mesh_TF', q=True, tx=True), obj)
        elif classification in ('ambientLight', 'directionalLight', 'pointLight', 'spotLight', 'areaLight'
                                , 'volumeLight') and cmds.checkBox('Lights_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Lights_TF', q=True, tx=True), obj)
        elif classification == 'imagePlane' and cmds.checkBox('ImagePlane_CB', q=True, v=True):
            assignPrefixes(cmds.textField('ImagePlane_TF', q=True, tx=True), obj)
        elif classification == 'locator' and cmds.checkBox('Locator_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Locator_TF', q=True, tx=True), obj)
        elif classification == 'nurbsSurface' and cmds.checkBox('NURBS_Objects_CB', q=True, v=True):
            assignPrefixes(cmds.textField('NURBS_Objects_TF', q=True, tx=True), obj)
        # Add Additional Materials Here
        elif classification in ('standardSurface', 'anisotropic', 'blinn', 'lambert', 'phong'
                                , 'phongE', 'layeredShader', 'rampShader', 'shadingMap'
                                , 'surfaceShader', 'useBackground') \
                and cmds.checkBox('Material_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Material_TF', q=True, tx=True), obj)
        elif classification == 'nurbsCurve' and cmds.checkBox('NURBS_Curve_CB', q=True, v=True):
            assignPrefixes(cmds.textField('NURBS_Curve_TF', q=True, tx=True), obj)
        elif classification == 'MASH_Waiter' and cmds.checkBox('MASH_CB', q=True, v=True):
            assignPrefixes(cmds.textField('MASH_TF', q=True, tx=True), obj)
        elif classification == 'camera' and cmds.checkBox('Cameras_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Cameras_TF', q=True, tx=True), obj)
        elif classification == 'sketchPlane' and cmds.checkBox('ConstructionPlane_CB', q=True, v=True):
            assignPrefixes(cmds.textField('ConstructionPlane_TF', q=True, tx=True), obj)
        elif classification == 'container' and cmds.checkBox('Asset_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Asset_TF', q=True, tx=True), obj)
        elif classification in ('renderCone', 'renderBox', 'renderSphere', 'volumeFog') \
                and cmds.checkBox('Volume_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Volume_TF', q=True, tx=True), obj)
        elif classification == 'joint' and cmds.checkBox('Joints_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Joints_TF', q=True, tx=True), obj)
        elif classification in ('ikRPsolver', 'ikSCsolver', 'ikSplineSolver', 'ikSystem') \
                and cmds.checkBox('IkHandles_CB', q=True, v=True):
            assignPrefixes(cmds.textField('IkHandles_TF', q=True, tx=True), obj)
        elif classification == 'objectSet' and cmds.checkBox('Sets_CB', q=True, v=True):
            assignPrefixes(cmds.textField('Sets_TF', q=True, tx=True), obj)
        elif classification == 'particleCloud' and cmds.checkBox('ParticleCloud_CB', q=True, v=True):
            assignPrefixes(cmds.textField('ParticleCloud_TF', q=True, tx=True), obj)


def assignPrefixes(prefix, obj):
    # Change name of objects Transform
    try:
        objectTransform = cmds.listRelatives(obj, parent=True)
    except:
        return

    if objectTransform:
        for objTrnsfm in objectTransform:
            if prefix in objTrnsfm:
                continue
            try:
                reformattedName = objTrnsfm.replace('|', '')
                newTransformName = prefix + "_" + reformattedName
                print("New Name: " + newTransformName)
                cmds.rename(objTrnsfm, newTransformName)
            except:
                cmds.warning(str(objTrnsfm) + " is read only! Cannot change the name!")
            return
    else:
        if prefix in obj:
            cmds.select(obj)
            return
        try:
            # Change name of object
            newObjectName = prefix + "_" + obj
            print("New Object Name: " + newObjectName)
            cmds.rename(obj, newObjectName)
        except:
            cmds.warning(str(obj) + " is read only! Cannot change the name!")


def assignSelection(objects):
    # Assigns either a prefix or suffix depending on radio selection
    hierarchy = cmds.listRelatives(ad=True)
    for obj in objects:
        if cmds.radioButton('PrefixRadio', query=True, select=True):
            assignPrefixes(cmds.textField('Selection_TF', q=True, tx=True), obj)
        elif cmds.radioButton('SuffixRadio', query=True, select=True):
            assignSuffix(cmds.textField('Selection_TF', q=True, tx=True), obj)
    if hierarchy:
        for obj in hierarchy:
            if cmds.radioButton('PrefixRadio', query=True, select=True):
                assignPrefixes(cmds.textField('Selection_TF', q=True, tx=True), obj)
            elif cmds.radioButton('SuffixRadio', query=True, select=True):
                assignSuffix(cmds.textField('Selection_TF', q=True, tx=True), obj)


def assignSuffix(suffix, obj):
    # Change name of objects Transform
    try:
        objectTransform = cmds.listRelatives(obj, parent=True)
    except:
        return
    if objectTransform:
        for objTrnsfm in objectTransform:
            if suffix in objTrnsfm:
                continue
            try:
                reformattedName = objTrnsfm.replace('|', '')
                newTransformName = reformattedName + "_" + suffix
                print("New Name: " + newTransformName)
                cmds.rename(objTrnsfm, newTransformName)
            except:
                cmds.warning(str(objTrnsfm) + " is read only! Cannot change the name!")
            return
    else:
        if suffix in obj:
            cmds.select(obj)
            return
        try:
            # Change name of object
            newObjectName = obj + "_" + suffix
            print("New Object Name: " + newObjectName)
            cmds.rename(obj, newObjectName)
        except:
            cmds.warning(str(obj) + " is read only! Cannot change the name!")


def removeAllPrefixes(objects):
    for obj in objects:
        classification = classifyObject(obj)
        if classification == 'mesh' and cmds.checkBox('Mesh_CB', q=True, v=True):
            removePrefixes(cmds.textField('Mesh_TF', q=True, tx=True), obj)
        elif classification == 'nurbsSurface' and cmds.checkBox('NURBS_Objects_CB', q=True, v=True):
            removePrefixes(cmds.textField('NURBS_Objects_TF', q=True, tx=True), obj)
        elif classification in ('ambientLight', 'directionalLight', 'pointLight', 'spotLight', 'areaLight'
                                , 'volumeLight') and cmds.checkBox('Lights_CB', q=True, v=True):
            removePrefixes(cmds.textField('Lights_TF', q=True, tx=True), obj)
        elif classification == 'imagePlane' and cmds.checkBox('ImagePlane_CB', q=True, v=True):
            removePrefixes(cmds.textField('ImagePlane_TF', q=True, tx=True), obj)
        elif classification == 'locator' and cmds.checkBox('Locator_CB', q=True, v=True):
            removePrefixes(cmds.textField('Locator_TF', q=True, tx=True), obj)
        elif classification == 'nurbsSurface' and cmds.checkBox('NURBS_Objects_CB', q=True, v=True):
            removePrefixes(cmds.textField('NURBS_Objects_TF', q=True, tx=True), obj)
            # Add Additional Materials Here
        elif classification in ('standardSurface', 'anisotropic', 'blinn', 'lambert', 'phong'
                                , 'phongE', 'layeredShader', 'rampShader', 'shadingMap'
                                , 'surfaceShader', 'useBackground') \
                and cmds.checkBox('Material_CB', q=True, v=True):
            removePrefixes(cmds.textField('Material_TF', q=True, tx=True), obj)
        elif classification == 'nurbsCurve' and cmds.checkBox('NURBS_Curve_CB', q=True, v=True):
            removePrefixes(cmds.textField('NURBS_Curve_TF', q=True, tx=True), obj)
        elif classification == 'MASH_Waiter' and cmds.checkBox('MASH_CB', q=True, v=True):
            removePrefixes(cmds.textField('MASH_TF', q=True, tx=True), obj)
        elif classification == 'camera' and cmds.checkBox('Cameras_CB', q=True, v=True):
            removePrefixes(cmds.textField('Cameras_TF', q=True, tx=True), obj)
        elif classification == 'sketchPlane' and cmds.checkBox('ConstructionPlane_CB', q=True, v=True):
            removePrefixes(cmds.textField('ConstructionPlane_TF', q=True, tx=True), obj)
        elif classification == 'container' and cmds.checkBox('Asset_CB', q=True, v=True):
            removePrefixes(cmds.textField('Asset_TF', q=True, tx=True), obj)
        elif classification in ('renderCone', 'renderBox', 'renderSphere', 'volumeFog') \
                and cmds.checkBox('Volume_CB', q=True, v=True):
            removePrefixes(cmds.textField('Volume_TF', q=True, tx=True), obj)
        elif classification == 'joint' and cmds.checkBox('Joints_CB', q=True, v=True):
            removePrefixes(cmds.textField('Joints_TF', q=True, tx=True), obj)
        elif classification in ('ikRPsolver', 'ikSCsolver', 'ikSplineSolver', 'ikSystem') \
                and cmds.checkBox('IkHandles_CB', q=True, v=True):
            removePrefixes(cmds.textField('IkHandles_TF', q=True, tx=True), obj)
        elif classification == 'objectSet' and cmds.checkBox('Sets_CB', q=True, v=True):
            removePrefixes(cmds.textField('Sets_TF', q=True, tx=True), obj)
        elif classification == 'particleCloud' and cmds.checkBox('ParticleCloud_CB', q=True, v=True):
            removePrefixes(cmds.textField('ParticleCloud_TF', q=True, tx=True), obj)


def removePrefixes(prefix, obj):
    try:
        objectTransform = cmds.listRelatives(obj, parent=True)
    except:
        return
    if objectTransform:
        for i in objectTransform:
            if prefix in i:
                reformattedName = i.replace('|', '')
                prefix += '_'
                newName = reformattedName.removeprefix(prefix)
                cmds.rename(i, newName)
                print('Prefix removed from: ' + newName)
    else:
        if prefix in obj:
            try:
                # Change name of object
                prefix += '_'
                newName = obj.removeprefix(prefix)
                cmds.rename(obj, newName)
                print('Prefix removed from: ' + newName)
            except:
                cmds.warning(str(obj) + " is read only! Cannot change the name!")


def removeSuffixes(suffix, obj):
    try:
        objectTransform = cmds.listRelatives(obj, parent=True)
    except:
        return
    if objectTransform:
        for i in objectTransform:
            if suffix in i:
                reformattedName = i.replace('|', '')
                suffix = '_' + suffix
                newName = reformattedName.removesuffix(suffix)
                cmds.rename(i, newName)
                print('Prefix removed from: ' + newName)
    else:
        if suffix in obj:
            try:
                # Change name of object
                suffix = '_' + suffix
                newName = obj.removesuffix(suffix)
                cmds.rename(obj, newName)
                print('Prefix removed from: ' + newName)
            except:
                cmds.warning(str(obj) + " is read only! Cannot change the name!")


def removeSelection(objects):
    # Removes either a prefix or suffix depending on radio selection
    hierarchy = cmds.listRelatives(ad=True)
    for obj in objects:
        if cmds.radioButton('PrefixRadio', query=True, select=True):
            removePrefixes(cmds.textField('Selection_TF', q=True, tx=True), obj)
        elif cmds.radioButton('SuffixRadio', query=True, select=True):
            removeSuffixes(cmds.textField('Selection_TF', q=True, tx=True), obj)
    if hierarchy:
        for obj in hierarchy:
            if cmds.radioButton('PrefixRadio', query=True, select=True):
                removePrefixes(cmds.textField('Selection_TF', q=True, tx=True), obj)
            elif cmds.radioButton('SuffixRadio', query=True, select=True):
                removeSuffixes(cmds.textField('Selection_TF', q=True, tx=True), obj)