#import Iterators
#import importlib
#importlib.reload(Iterators)
#Iterators.Iterator()

def Iterator():
    # Import the OpenMaya module
    import maya.OpenMaya as OpenMaya

    # Create an iterator that traverses the DAG in depth-first order
    dagIterator = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kInvalid)
    # Create an MFnDagNode object to access the attributes of the DAG node
    dagNodeFn = OpenMaya.MFnDagNode()

    # Iterate over all the nodes in the DAG
    while(not dagIterator.isDone()):
        # Get the current DAG node object
        currentObj = dagIterator.currentItem()
        # Get the depth of the current DAG node in the DAG tree
        depth = dagIterator.depth()
        # Set the MFnDagNode object to the current DAG node object
        dagNodeFn.setObject(currentObj)

        # Get the name of the current DAG node
        name = dagNodeFn.name()
        # Get the type of the current DAG node as a string
        type = currentObj.apiTypeStr()
        # Get the full path name of the current DAG node
        path = dagNodeFn.fullPathName()

        # Create a string to print the name, type, and depth of the current DAG node
        printOut = ""
        for i in range(0, depth):
            printOut += "----->"
        printOut += name + "   :   " + type
        # Print the string
        print(printOut)

        # Move to the next DAG node
        dagIterator.next()
