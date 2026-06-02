import os
import shutil
import zipfile
import pandas as pd

stack = []

loc = 'dummy_data'
os.makedirs('result', exist_ok=True)

log = []

stack.append((loc, False, False))

while stack:
    loc, isOCT, isFUNDUS = stack.pop()
    try:
        for sub in os.scandir(loc):
            if sub.is_dir(): #Probably shouldn't have called the path var dir
                stack.append((sub.path, isOCT or sub.name == "OCT", isFUNDUS or sub.name == "FUNDUS"))
            elif sub.is_file():
                if not isOCT or (sub.name == "016.png" and not isFUNDUS):
                    if not os.path.exists(os.path.join('result', sub.name)):
                        shutil.copy2(sub.path, os.path.join('result', sub.name))
                    else:
                        rename = os.path.abspath(sub.path).replace(os.path.sep, '_')
                        shutil.copy2(sub.path, os.path.join('result', rename)) #Why is this yellow
                elif isOCT:
                    pass
                elif isFUNDUS:
                    pass



    except PermissionError:
        continue