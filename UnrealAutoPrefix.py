# Unreal Prefix - Maya
# Henry Foley, 2023

import unreal
import json
import os

unrealPrefixes = []
asset_list = unreal.EditorUtilityLibrary.get_selected_assets()

class DialogException(Exception):
    # Spawns message dialog on error
    def __init__(self, message):
        unreal.EditorDialog.show_message('Warning', message, unreal.AppMsgType.OK)
        unreal.log_warning(message)


def main():
    filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "unrealPrefixes.json")
    loadJsonFile(filePath)
    assignAllPrefixes()


def loadJsonFile(filePath):
    global unrealPrefixes
    if os.path.exists(filePath):  # Change back to 'filePath'
        unrealPrefixes = json.load(open(filePath))
    else:
        # Display file not found message
        DialogException('Cannot find the JSON file: unrealPrefixes.json')


def assignPrefix(asset: object, prefix: object) -> object:
    assetName = asset.get_name()
    # Check if Asset has a prefix
    if "_" in str(assetName)[0:5]:
        print("Prefix already in " + str(assetName))
        return
    else:
        assetName = prefix + str(assetName)
        print("Asset:" + str(asset))
        print("JSON Code: " + prefix)
        print("Renamed Asset: " + str(assetName))
        unreal.EditorUtilityLibrary.rename_asset(asset, assetName)


def assignAllPrefixes():
    if not asset_list:
        DialogException('No Assets Selected!')
        return
    else:
        print('This is the asset list: ' + str(asset_list))
    for asset in asset_list:

        # Get Asset Type and name
        assetType = asset.get_class().get_name()

        if assetType == "AnimBlueprint":
            assignPrefix(asset, unrealPrefixes['Animation_Blueprint'])
            continue
        elif assetType == "AnimMontage":
            assignPrefix(asset, unrealPrefixes['Animation_Montages'])
            continue
        elif assetType == "AnimSequence":
            assignPrefix(asset, unrealPrefixes['Animation_Sequence'])
            continue
        elif assetType == "Blueprint":
            assignPrefix(asset, unrealPrefixes['Blueprint'])
            continue
        elif assetType == "BlendSpace":
            assignPrefix(asset, unrealPrefixes['Blend_Space'])
            continue
        elif assetType == "BehaviorTree":
            assignPrefix(asset, unrealPrefixes['Behavior_Tree'])
            continue
        elif assetType == "CurveTable":
            assignPrefix(asset, unrealPrefixes['Curve_Table'])
            continue
        elif assetType == "DataTable":
            assignPrefix(asset, unrealPrefixes['Data_Table'])
            continue
        elif assetType == "UserDefinedEnum":
            assignPrefix(asset, unrealPrefixes['Enum'])
            continue
        elif assetType == "UserDefinedStruct":
            assignPrefix(asset, unrealPrefixes['Structure'])
            continue
        elif assetType == "TextureCube":
            assignPrefix(asset, unrealPrefixes['HDRI'])
            continue
        elif assetType == "World":
            assignPrefix(asset, unrealPrefixes['Level'])
            continue
        elif assetType == "LevelSequence":
            assignPrefix(asset, unrealPrefixes['Level_Sequence'])
            continue
        elif assetType == 'Material':
            assignPrefix(asset, unrealPrefixes['Material'])
            continue
        elif assetType == "MaterialFunction":
            assignPrefix(asset, unrealPrefixes['Material_Function'])
            continue
        elif assetType == "MaterialInstanceConstant":
            assignPrefix(asset, unrealPrefixes['Material_Instance'])
            continue
        elif assetType == "MediaPlayer":
            assignPrefix(asset, unrealPrefixes['Media_Player'])
            continue
        elif assetType == "MediaTexture":
            assignPrefix(asset, unrealPrefixes['Media_Texture'])
            continue
        elif assetType == "NiagaraEmitter":
            assignPrefix(asset, unrealPrefixes['Niagara_Emitter'])
            continue
        elif assetType == "NiagaraScript":
            assignPrefix(asset, unrealPrefixes['Niagara_Function'])
            continue
        elif assetType == "NiagaraSystem":
            assignPrefix(asset, unrealPrefixes['Niagara_System'])
            continue
        elif assetType == 'PhysicsAsset':
            assignPrefix(asset, unrealPrefixes['Physics_Asset'])
            continue
        elif assetType == 'PhysicalMaterial':
            assignPrefix(asset, unrealPrefixes['Physics_Material'])
            continue
        elif assetType == 'ParticleSystem':
            assignPrefix(asset, unrealPrefixes['Particle_System'])
            continue
        elif assetType == 'ReverbEffect':
            assignPrefix(asset, unrealPrefixes['Reverb_Effect'])
            continue
        elif assetType == 'IKRigDefinition':
            assignPrefix(asset, unrealPrefixes['Rig'])
            continue
        elif assetType == 'SoundWave':
            assignPrefix(asset, unrealPrefixes['Sound_Wave'])
            continue
        elif assetType == 'SoundCue':
            assignPrefix(asset, unrealPrefixes['Sound_Cue'])
            continue
        elif assetType == 'SoundClass':
            assignPrefix(asset, unrealPrefixes['Sound_Class'])
            continue
        elif assetType == 'SkeletalMesh':
            assignPrefix(asset, unrealPrefixes['Skeletal_Mesh'])
            continue
        elif assetType == 'Skeleton':
            assignPrefix(asset, unrealPrefixes['Skeleton'])
            continue
        elif assetType == 'StaticMesh':
            assignPrefix(asset, unrealPrefixes['Static_Mesh'])
            continue
        elif assetType == 'Texture2D':
            assignPrefix(asset, unrealPrefixes['Texture'])
            continue
        elif assetType == 'WidgetBlueprint':
            assignPrefix(asset, unrealPrefixes['Widget_Blueprint'])
            continue
        elif assetType == 'ObjectRedirector':
            #Bootstrap case
            continue
        else:
            print("This asset type has no prefix code: " + str(assetType))


# RUN PROGRAM
main()
