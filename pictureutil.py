from PIL import Image
import os

def merge_pic(dir, pic_list, save_file):
    file_list = []
    for item in pic_list:
        file_list.append(os.path.join(dir, item))
    merge_pic_files(file_list,save_file)
    



def merge_pic_files(files, save_file):
    from PIL import Image
    import numpy as np
    baseimg=Image.open(files[0])
    sz = baseimg.size
    basemat=np.atleast_2d(baseimg)
    for file in files[1:]:
        im=Image.open(file)
    #resize to same width
        sz2 = im.size
        if sz2!=sz:
            im=im.resize((sz[0],round(sz2[0] / sz[0] * sz2[1])),Image.ANTIALIAS)
        mat=np.atleast_2d(im)
        basemat=np.append(basemat,mat,axis=0)
    report_img=Image.fromarray(basemat)

    report_img.save(save_file)