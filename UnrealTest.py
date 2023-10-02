# Unreal Test - Maya
# Henry Foley, 2023
import time

import unreal

path = '/Game/StarterContent/Materials'

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
        #if asset.get_class() == 'Materials':
        print(asset)
        time.sleep(0.1)
        slow_task.enter_progress_frame(1)
