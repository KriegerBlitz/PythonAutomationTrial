import os
import shutil
import zipfile
import csv
from os import DirEntry

stack = []

loc = 'dummy_data'
os.makedirs('result', exist_ok=True)

log = {}
def copy(sub: os.DirEntry):
    if not sub.name in log:
        shutil.copy2(sub.path, os.path.join('result', sub.name))
        log[sub.name] = {'new name': sub.name, 'path': sub.path, 'old name': sub.name, 'kill': False}
    else:
        rename = str(os.path.abspath(sub.path).replace(os.path.sep, '_'))
        shutil.copy2(sub.path, os.path.join('result', rename))  # Why is this yellow
        log[rename] = {'new name': rename, 'path': sub.path, 'old name': sub.name, 'kill': False}
        log[sub.name]['kill'] = True
        # dic = log.pop(sub.name)
        # rename = str(os.path.abspath(dic['path']).replace(os.path.sep, '_'))
        # os.rename(os.path.join('result', sub.name), os.path.join('result', rename))
        # log[rename] = {'new name': rename, 'path': dic['path'], 'old name': sub.name}

def checkimg(name:str):
    return name.endswith(('.png', '.jpg', '.jpeg','.tif','tiff','.webp','.arw','.bmp'))

stack.append((loc, False))

while stack:
    loc, isOCT = stack.pop()
    try:
        for sub in os.scandir(loc):
            if sub.is_dir(): #Probably shouldn't have called the path var dir
                if sub.name!= 'FUNDUS': stack.append((sub.path, isOCT or sub.name == "OCT"))
                else:
                    for fun in os.scandir(sub.path):
                        if fun.name.startswith('0'):
                            continue
                        elif checkimg(fun.name):
                            copy(fun)

            elif sub.is_file():
                if not isOCT and checkimg(sub.name) or (sub.name == "016.png"):
                    copy(sub)

                elif isOCT:
                    name, ext = os.path.splitext(sub.name)




    except PermissionError:
        continue