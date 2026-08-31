import os
import shutil


def copy_static(src,dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    else:
        for item in os.listdir(dst):
            os.remove(os.path.join(dst,item))
        os.rmdir(dst)
        os.mkdir(dst)
        for item in os.listdir(src):
            from_path = os.path.join(src,item)
            to_path = os.path.join(dst,item)
            if os.path.isfile(from_path):
                shutil.copy(from_path,to_path)
            else:
                copy_static(from_path,to_path)
            
        