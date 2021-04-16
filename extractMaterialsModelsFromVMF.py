import re
import os
import glob
import shutil
import string
from termcolor import colored

vmfName = 'rp_expecto_day_vz4.vmf'
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

# https://stackoverflow.com/a/17197027
def strings(filename, min=1):
    strs = []

    with open(filename, errors="ignore") as f:
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                strs.append(result)
            result = ""
        if len(result) >= min:
            strs.append(result)
    
    return strs

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

def copyFileWithDirs(filePath):
    targetPath = os.path.join(contentsDistPath, os.path.dirname(os.path.relpath(filePath, garrysmodGarrysmodPath)))
    os.makedirs(targetPath, exist_ok=True)
    shutil.copy(filePath, targetPath)

for material in materials:
    sourcePath = os.path.join(garrysmodGarrysmodPath,material)

    if os.path.isfile(sourcePath):
        copyFileWithDirs(sourcePath)

        for path in findVtfPathsFromVmt(sourcePath):
            copyFileWithDirs(path)

for model in models:
    sourcePath = os.path.join(garrysmodGarrysmodPath,model)
    
    if os.path.isfile(sourcePath):
        strs = strings(sourcePath)
        materialPath = strs[-1].replace('/','\\')
        materialPath = materialPath.lower()
        materialPath = os.path.join('materials',materialPath)
        materialRealPath = os.path.join(garrysmodGarrysmodPath,materialPath)

        if (os.path.isdir(materialRealPath)):
            for possibleMaterialName in strs[1:-1]:
                possibleMaterialRealPath = os.path.join(materialRealPath,possibleMaterialName+'.vmt')
                if (os.path.isfile(possibleMaterialRealPath)):
                    copyFileWithDirs(possibleMaterialRealPath)
                    for path in findVtfPathsFromVmt(possibleMaterialRealPath):
                        copyFileWithDirs(path)
        else:
            print(colored("MATERIAL PATH NOT FOUND", 'red'), materialPath)

        for file in glob.glob(sourcePath[:-3]+'*'):
            copyFileWithDirs(file)
    else:
        print(colored("MODEL NOT FOUND", 'red'), model)