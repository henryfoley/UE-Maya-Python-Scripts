#import MayaFunctions
#import importlib
#importlib.reload(MayaFunctions)
#MayaFunctions.myFunction()

import maya.cmds as cmds

def myFunction():
    numCubes = 10
    w =1.245
    h = 4.0
    d = 0.5
    allTheCubes = []
    for x in range(numCubes):
        cube = cmds.polyCube(w=w, h=h, d=d, n = "aCube#", ch=False)
        cube = cube[0]
        cmds.move(h/2, cube, moveY=True)
        cmds.move(w*x, cube, moveX=True)
        allTheCubes.append(cube)
    cubesGroup = cmds.group(empty =True, world =True, n="groupOfCubes#")
    print(cubesGroup)
    for each in allTheCubes:
        cmds.parent(each, cubesGroup)
    cmds.select(clear=True)