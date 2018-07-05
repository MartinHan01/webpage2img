
import os

def mkdirs_if_not_exist(path):
    if os.path.exists(path) == False:
        os.makedirs(path)
