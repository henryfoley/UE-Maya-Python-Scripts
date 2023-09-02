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
    assignPrefix()


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

def assignPrefix():
    objects = cmds.ls()
    objects.sort(key=len, reverse=True)
    print(objects)