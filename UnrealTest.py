# Unreal Prefix - Maya
# Henry Foley, 2023

import time
import unreal
import json
import os

unrealPrefixes = []

path = '/Game/TestFolder'
#path = '/Game/StarterContent/Materials'

asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(path)
#asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class()

"""print(asset_list)

for asset in asset_list:
    print(asset)"""


def main():
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "prefixFormattingSettings.json")
    loadJsonFile(filePath)


def loadJsonFile(filePath):
    global unrealPrefixes

    if os.path.exists(filePath):
        prefixFormattingOptionsJson = json.load(open(filePath))
    else:
        # Display file not found message
        unreal.log_warning('Cannot find the JSON file: prefixFormattingSettings.json')

        # Open a file explorer to locate the file
        fileFilter = "JSON Files (*.json)"
        filePath = filePath.asset_reimport('open_file_dialog')
        if filePath:
            return loadJsonFile(filePath[0])
        else:
            return None


total_frames = len(asset_list)
text_label = "Listing!"
with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
    slow_task.make_dialog(True)
    for asset in asset_list:
        if slow_task.should_cancel():
            break

        # Get Asset Type and name
        assetType = asset.get_class().get_name()
        assetFilePath = asset.get_export_text_name()

        if assetType == "Blueprint":
            print("Found Static Mesh: " + str(assetFilePath))
        elif assetType == 'Material':
            print("Found Mat" + str(assetFilePath))
        elif assetType == 'NiagaraSystem':
            print("Found Niagara")
        elif assetType == 'StaticMesh':
            print("Found Static Mesh: " + str(assetFilePath))
        else:
            print("This asset type has no prefix code: " + str(assetFilePath))
        print("Asset: " + str(asset) + "Class: " + str(asset.get_class()))
        time.sleep(0.1)
        slow_task.enter_progress_frame(1)

def assignPrefix(assetName, prefix):
    unreal.rename_asset(str(assetName), '/Game/Ops/FooBarUpdated')