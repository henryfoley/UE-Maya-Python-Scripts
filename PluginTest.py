import sys
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass

kPluginCmdName = 'pyPrintPaths'

##########################################################
# Plug-in
##########################################################
class printPathsCmd(OpenMaya.MPxCommand):

    def __init__(self):
        ''' Constructor. '''
        OpenMaya.MPxCommand.__init__(self)

    def doIt(self, args):
        print("did it")

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Creates an instance of our command class. '''
    return printPathsCmd()

def initializePlugin(mobject):
    ''' Initializes the plug-in.'''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )

def uninitializePlugin(mobject):
    ''' Uninitializes the plug-in '''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )