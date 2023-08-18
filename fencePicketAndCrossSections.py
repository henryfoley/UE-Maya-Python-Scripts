#import fencePicketAndCrossSections
#import importlib
#importlib.reload(fencePicketAndCrossSections)
#fencePicketAndCrossSections.fenceBuilder()

import maya.cmds as cmds

# Fence Layout
numPickets = 10
numCrossSections = 4

def fenceBuilder():


    #UI

    if cmds.window('FenceBuilder', exists=True):
        print('Window exists! Deleting window!')
        cmds.deleteUI('FenceBuilder', window=True)

    cmds.window('FenceBuilder', sizeable=True)

    cmds.columnLayout('mainUI_C', parent='FenceBuilder')
    cmds.rowColumnLayout(nc=1, cw=[(1, 400)], p='mainUI_C')
    cmds.separator(h=10, style='none')
    cmds.rowColumnLayout(nc=3, cw=[(1, 150), (2, 100), (3, 100)], cs=[(1, 10), (2, 10), (3, 10)], p='mainUI_C')

    cmds.text(label='Picket Amount:')
    cmds.button(l='+', command=lambda args: increasePicketValue())
    cmds.button(l='-', command=lambda args: decreasePicketValue())

    cmds.rowColumnLayout(nc=1, cw=[(1, 400)], p='mainUI_C')
    cmds.separator(h=10, style='in')
    cmds.rowColumnLayout(nc=3, cw=[(1, 150), (2, 100), (3, 100)], cs=[(1, 10), (2, 10), (3, 10)], p='mainUI_C')
    cmds.text(label='Cross Sections Amount:')
    cmds.button(l='+', command=lambda args: increaseCrossSectionValue())
    cmds.button(l='-', command=lambda args: decreaseCrossSectionValue())

    cmds.rowColumnLayout(nc=1, cw=[(1, 400)], p='mainUI_C')
    cmds.separator(h=10, style='in')
    cmds.rowColumnLayout(nc=3, cw=[(1, 150), (2, 100), (3, 100)], cs=[(1, 10), (2, 10), (3, 10)], p='mainUI_C')
    cmds.button(l='Build Fence', command=lambda args: buildFence(numPickets, numCrossSections))

    cmds.showWindow('FenceBuilder')

def buildFence(numPickets,numCrossSections):

    pWidth = 0.4
    pHeight = 4.0
    pDepth = 0.1
    pSpacing = 0.5
    pName = "picket#"


    pickets = buildPickets(pWidth,pHeight, pDepth, pSpacing, pName, numPickets)

    groupName = "fenceSections#"
    fenceSectionGroup = cmds.group(empty=True, world=True, n=groupName)
    groupObjects(pickets, fenceSectionGroup)

    crossSectionHeight = 0.4
    crossSectionDepth = 0.15
    crossSectionName = "CrossSection#"
    crossSections = buildCrossSections(crossSectionHeight, crossSectionDepth,numCrossSections, fenceSectionGroup, crossSectionName)

    groupObjects(crossSections, fenceSectionGroup)

    cmds.select(clear=True)

def buildPickets(pw, ph, pd, ps, pn, numPickets):
    pickets = []
    for x in range(numPickets):
        picket = cmds.polyCube(w=pw, h=ph, d=pd, ch=False, name=pn)
        picket = picket[0]
        cmds.move(ph/2, picket, moveY=True)
        cmds.move(pw/2, picket, moveX=True)
        pickets.append(picket)

    for x in range(len(pickets)):
        cmds.move((pw + ps) * x, pickets[x], moveX=True, relative=True)

    cmds.select(clear=True)

    return pickets

def buildCrossSections(csHeight, csDepth, numCS, fenceSectionGroup, csName):
    # BOUNDING BOX for the entire group of pickets!
    xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(fenceSectionGroup, query=True, bb=True)
    sectionWidth = round(xmax - xmin, 5)
    sectionHeight = round(ymax - ymin, 5)
    sectionDepth = round(zmax - zmin, 5)

    csOffset = 0.5

    crossSections = []
    for x in range(numCS):
        cs = cmds.polyCube(w=sectionWidth, h=csHeight, d=csDepth, ch=False, name=csName)
        cs = cs[0]
        cmds.move(sectionWidth/2.0, cs, moveX=True)
        cmds.move((csHeight/2.0) + csOffset, cs, moveY=True)
        cmds.move(-csDepth/2.0, cs, moveZ=True)
        cmds.move(-sectionDepth/2.0, moveZ=True, relative=True)
        crossSections.append(cs)

    heightWithOffset = sectionHeight - (csOffset*2.0)
    amountToMove = heightWithOffset/numCS

    for x in range(1, numCS):
        cmds.move(amountToMove * x, crossSections[x], moveY=True, relative=True)

    cmds.select(clear=True)

    return crossSections

def groupObjects(objects, theGroup):
    for each in objects:
        cmds.parent(each, theGroup)

def decreasePicketValue():
    global numPickets
    numPickets -= 1
    print(numPickets)
    return numPickets

def increasePicketValue():
    global numPickets
    numPickets += 1
    print(numPickets)
    return numPickets

def decreaseCrossSectionValue():
    global numCrossSections
    numCrossSections -= 1
    print(numCrossSections)
    return numCrossSections

def increaseCrossSectionValue():
    global numCrossSections
    numCrossSections += 1
    print(numCrossSections)
    return numCrossSections

