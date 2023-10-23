# Unreal Prefix - Maya
# Henry Foley, 2023

import time
import unreal
import json
import os

@unreal.uclass()
class GlobalEditorUtilityBase(unreal.GlobalEditorUtilityBase): pass

utilBase = GlobalEditorUtilityBase()
unrealPrefixes = []

path = '/Game/TestFolder'
#path = '/Game/StarterContent/Materials'

asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(path)

#asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class()

"""print(asset_list)

for asset in asset_list:
    print(asset)"""


def main():
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "unrealPrefixes.json")
    loadJsonFile(filePath)


def loadJsonFile(filePath):
    global unrealPrefixes

    if os.path.exists(filePath):  # Change back to 'filePath'
        unrealPrefixes = json.load(open(filePath))
    else:
        # Display file not found message
        unreal.log_warning('Cannot find the JSON file: prefixFormattingSettings.json')
        print("TESTING")
        # Open a file explorer to locate the file
        fileFilter = "JSON Files (*.json)"
        filePath = unreal.DirectoryPath()
        if filePath:
            return loadJsonFile(filePath[0])
        else:
            return None


def assignPrefix(asset, prefix):

    assetName = asset.get_editor_property('asset_name')
    packagePath = asset.get_editor_property('package_name')

    assetName = prefix + str(assetName)

    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    assetTools.rename_assets([unreal.AssetRenameData(asset, packagePath, assetName)])

    print("Renamed Asset: " + str(assetName))
    #unreal.EditorAssetSubsystem.rename_asset(packageName, renamedAsset)
    #unreal.EditorAssetLibrary



main()
#for asset in unrealPrefixes:
 #   print(asset)
total_frames = len(asset_list)
text_label = "Listing!"
with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
    slow_task.make_dialog(True)
    for asset in asset_list:
        if slow_task.should_cancel():
            break

        # Get Asset Type and name
        assetType = asset.get_class().get_name()
        assetName = asset.get_editor_property('asset_name')
        assetPackageName = asset.get_editor_property('package_name')

        if assetType == "Blueprint":
            print("Found Blueprint: " + str(assetName) + " JSON Code: " + unrealPrefixes['Blueprint'])
            print("Asset: " + str(assetPackageName))
            #assetName = unrealPrefixes['Blueprint'] + str(assetName)
            assignPrefix(asset, unrealPrefixes['Blueprint'])
            #utilBase.rename_asset(asset, "{}_{}".format(unrealPrefixes['Blueprint'], assetName))
            continue
        """elif assetType == 'Material':
            print("Found Mat" + str(assetFilePath))
            continue
        elif assetType == 'NiagaraSystem':
            print("Found Niagara")
            continue
        elif assetType == 'StaticMesh':
            print("Found Static Mesh: " + str(assetFilePath))
            continue
        else:
            print("This asset type has no prefix code: " + str(assetFilePath))
        # print("Asset: " + str(asset) + "Class: " + str(asset.get_class()))"""
        time.sleep(0.1)
        slow_task.enter_progress_frame(1)

