# Unreal Test - Maya
# Henry Foley, 2023
import time

import unreal

path = '/Game/TestFolder'
#path = '/Game/StarterContent/Materials'

asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(path)
#asset_list = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_class()

"""print(asset_list)

for asset in asset_list:
    print(asset)"""

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
        print("Asset: " + str(asset) + "Class: " + str(asset.get_class()))
        time.sleep(0.1)
        slow_task.enter_progress_frame(1)
