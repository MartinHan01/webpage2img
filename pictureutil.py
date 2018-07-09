from PIL import Image
import os

def merge_pic(dir, pic_list, save_file):
    file_list = []
    for item in pic_list:
        file_list.append(os.path.join(dir, item))
    merge_pic_files(file_list,save_file)
    



def merge_pic_files(files, save_file):
    ims = []
    width = 0
    height = 0
    for item in files:
        img = Image.open(item)
        ims.append(img)
        if width != 0:
            width = ims.size[0]
        height = height + img.size[1]

    result = Image.new(ims[0].mode, (width, height))
    now_height_begin = 0
    
    for i, im in enumerate(ims):
        now_height_end = now_height_begin + im.size[1]
        result.paste(im, box=(now_height_begin, now_height_end))
        now_height_begin = now_height_end
    result.save(save_file)

