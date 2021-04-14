import re
import os
import glob
import shutil

vmfName = 'test.vmf'
garrysmodGarrysmodPath = "D:\Program Files (x86)\SteamLibrary\steamapps\common\GarrysMod\garrysmod"

vmfFileName, vmfExtension = os.path.splitext(vmfName)

with open(vmfName) as vmfFile:
    vmfContent = vmfFile.read()

materials = re.findall(r"\"material\" \"(.+)\"", vmfContent)
materials = set(materials)
materials = {"materials" + (material[0]=='/' and material or '/'+material).lower() + ".vmt" for material in materials}
materials = {material.replace('/','\\') for material in materials}


models = re.findall(r"\"model\" \"(.+)\"", vmfContent)
models = set(models)
models = {model.replace('/','\\') for model in models}

contentsDistPath = os.path.join(os.getcwd(),vmfFileName+"_map_contents\\")

if os.path.isdir(contentsDistPath):
    shutil.rmtree(contentsDistPath)

os.mkdir(contentsDistPath)

def findVtfPathsFromVmt(vmtPath):
    with open(vmtPath) as materialFile:
        materialFileContents = materialFile.read()

    possibleVtfFileNames = re.findall(r"\"([^%$ {[\n,]+?)\"", materialFileContents)
    possibleVtfFileNames = {vtfPath for vtfPath in possibleVtfFileNames }
    possibleVtfFileNames = {vtfPath.replace('/','\\').lower() for vtfPath in possibleVtfFileNames}
    possibleVtfFileNames = {vtfPath.endswith('.vtf') and vtfPath or vtfPath+".vtf" for vtfPath in possibleVtfFileNames}
    
    paths = set()

    for name in possibleVtfFileNames:
        paths.add(os.path.join(os.path.dirname(sourcePath), name))
        paths.add(os.path.join(garrysmodGarrysmodPath, 'materials', name))

    paths = {path for path in paths if os.path.isfile(path)}

    return paths
    

for material in materials:
    sourcePath = os.path.join(garrysmodGarrysmodPath,material)

    if os.path.isfile(sourcePath):
        targetPath = os.path.join(contentsDistPath, os.path.dirname(os.path.relpath(sourcePath, garrysmodGarrysmodPath)))
        os.makedirs(targetPath, exist_ok=True)

        shutil.copy(sourcePath, targetPath)

        for path in findVtfPathsFromVmt(sourcePath):
            targetPath = os.path.join(contentsDistPath, os.path.dirname(os.path.relpath(path, garrysmodGarrysmodPath)))
            os.makedirs(targetPath, exist_ok=True)

            shutil.copy(path, targetPath)
            break

for model in models:
    sourcePath = os.path.join(garrysmodGarrysmodPath,model)
    targetPath = os.path.join(contentsDistPath, os.path.dirname(model))
    
    if os.path.isfile(sourcePath):
        os.makedirs(targetPath, exist_ok=True)
        for file in glob.glob(sourcePath[:-3]+'*'):
            shutil.copy(file,targetPath)
    else:
        print("BULUNAMADI - "+model)