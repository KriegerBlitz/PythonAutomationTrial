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
        print("Created:", log[sub.name])
    else:
        rename = str(os.path.abspath(sub.path).replace(os.path.sep, '_'))
        shutil.copy2(sub.path, os.path.join('result', rename))  # Why is this yellow
        log[rename] = {'new name': rename, 'path': sub.path, 'old name': sub.name, 'kill': False}
        log[sub.name]['kill'] = True
        print("Killed:", log[sub.name])
        print("Created:", log[rename])
        # dic = log.pop(sub.name)
        # rename = str(os.path.abspath(dic['path']).replace(os.path.sep, '_'))
        # os.rename(os.path.join('result', sub.name), os.path.join('result', rename))
        # log[rename] = {'new name': rename, 'path': dic['path'], 'old name': sub.name}

def checkimg(name:str):
    return name.endswith(('.png', '.jpg', '.jpeg','.tif','.tiff','.webp','.arw','.bmp'))

stack.append((loc, False))

while stack:
    loc, isOCT = stack.pop()
    try:
        for sub in os.scandir(loc):
            if sub.is_dir():
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
                    if ext == '.zip':
                        with zipfile.ZipFile(sub.path) as zip_ref:
                            zip_ref.extractall(os.path.join('result', name))
                        stack.append((os.path.join('result', name), True))
    except PermissionError:
        continue

for k in list(log):
    if log[k]['kill']:
        rename = str(os.path.abspath(log[k]['path']).replace(os.path.sep, '_'))
        os.rename(os.path.join('result', k), os.path.join('result', rename))
        log[rename] = {'new name': rename, 'path': log[k]['path'], 'old name' : log[k]['old name'], 'kill': False}
        log.pop(k)
        print("Executed:", k)


headers = ['new name', 'old name', 'path']

with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
    writer.writeheader()
    for k, v in log.items():
        writer.writerow(v)