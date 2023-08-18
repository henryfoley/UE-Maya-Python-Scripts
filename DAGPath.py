#import DAGPath
#import importlib
#importlib.reload(DAGPath)
#DAGPath.DagPath()

import maya.OpenMaya as OpenMaya

def DagPath():
    # Create Selection List
    mSelectionList = OpenMaya.MSelectionList()
    # Grab Object from scene and add it to the 0th location of the Selection List
    mSelectionList.add("pPlane1")

    # Created a handle
    mObj = OpenMaya.MObject()
    # Create an object that contains the Dag path of the objects
    mDagPath = OpenMaya.MDagPath()

    # Requested the list to give us the dependency node of the object at the 0th location
    mSelectionList.getDependNode(0, mObj)
    print(mObj.apiTypeStr())

    # Give us the Dag path of the object that is at the 0th location of the Selection List
    mSelectionList.getDagPath(0, mDagPath)
    print(mDagPath.fullPathName())

    # Created Mesh Function Set
    mFnMesh = OpenMaya.MFnMesh(mDagPath)
    print(mFnMesh.fullPathName())

    # Create Dependency Node Function Set
    mFnDependNode = OpenMaya.MFnDependencyNode(mObj)
    print(mFnDependNode.name())

    # Get all the connections of the shape node
    mPlugArray = OpenMaya.MPlugArray()
    mFnMesh.getConnections(mPlugArray)
    mPlugArray.length()
    print(mPlugArray[0].name())
    print(mPlugArray[1].name())

    # Get all connections coming into the shape node
    mPlugArray_connections = OpenMaya.MPlugArray()
    mPlugArray[1].connectedTo(mPlugArray_connections, True, False)
    mPlugArray_connections.length()
    print(mPlugArray_connections[0].name())

    # Get the node that is connected to the shape node
    mObj2 = mPlugArray_connections[0].node()
    mFnDependNode2 = OpenMaya.MFnDependencyNode(mObj2)
    print(mFnDependNode2.name())

    # Get the properties of the plugs on connected node
    mPlug_width = mFnDependNode2.findPlug("width")
    mPlug_height = mFnDependNode2.findPlug("height")
    mPlug_subWidth = mFnDependNode2.findPlug("subdivisionsWidth")
    mPlug_subHeight = mFnDependNode2.findPlug("subdivisionsHeight")
    print(mPlug_width.asInt())
    print(mPlug_height.asInt())
    print(mPlug_subWidth.asInt())
    print(mPlug_subHeight.asInt())

    # Set new values of the plugs on the connected node
    mPlug_subWidth.setInt(10)
    mPlug_subHeight.setInt(10)
    print(mPlug_subWidth.asInt())
    print(mPlug_subHeight.asInt())