import os
import zipfile
import pandas as pd

stack = []

dir = 'dummy_data'
os.makedirs('result', exist_ok=True)

log = []

stack.append((dir, False, False))

while stack:
    dir, isOCT, isFUNDUS = stack.pop()
    try:
        for sub in os.scandir(dir):
            if sub.is_dir(): #Probably shouldn't have called the path var dir
                stack.append((sub.path, isOCT or sub.name == "OCT", isFUNDUS or sub.name == "FUNDUS"))
            elif sub.is_file():
                if not isOCT or (sub.name == "016.png" and not isFUNDUS):

                else



    except PermissionError:
        continue