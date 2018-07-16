import zipfile
import os
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from PIL import Image
import time

# 原作者见：http://www.cnblogs.com/TTyb/p/6011947.html

# 设置全局变量
filepath = "D:/mycode/github/webpage2img/image/"
outzipfilepath = "D:/mycode/github/webpage2img/output/"
outpdffilepath = "D:/mycode/github/webpage2img/output/"
cropimgpath = "D:/mycode/github/webpage2img/output/crop/"


# 找出文件夹下所有.xml后缀的文件
def listfiles(rootdir, prefix='.xml'):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    file.append(filename)
            return file
        else:
            pass


# 创建文件夹
def createjia(path):
    try:
        os.makedirs(path)
    except:
        pass


# 这里是裁剪图片
# 传入的是图片的名字
def cropimg_tranpdf(imgname):
    # 新生成的文件夹的名字
    tempfilename = str(imgname.replace(".png", ""))

    # 创建保存裁剪后的图片的文件夹
    createpath = "../jpg/image/" + str(tempfilename)
    createjia(createpath)

    # 打开图片
    imgpath = filepath + imgname
    img = Image.open(imgpath)

    # 获得图片的宽高
    width = int(img.size[0])
    height = int(img.size[1])

    item_height = width * 1.5
    
    countheight = height // item_height
    if height % item_height != 0:
        countheight = countheight + 1

    countheight = int(countheight)
    # 将要保存的pdf的位置和名字
    pdfname = str(outpdffilepath) + str(tempfilename) + ".pdf"

    # 保存pdf
    c = canvas.Canvas(str(pdfname), pagesize=(width, item_height))
    # number of page
    newheight = 0
    for i in range(0, countheight):
        newheight = newheight + item_height
        # 裁剪的位置
        # (起始宽的位置，起始高的位置，裁剪宽度，裁剪高度)
        # 左上角的坐标为(0,0)
        region = (0, newheight - item_height, width, newheight)
        # 裁剪
        cropImg = img.crop(region)
        # 保存
        jpgname = str(i) + ".png"
        # 保存裁剪后的图片
        cropImg.save(str(createpath) + "/" + str(jpgname),)

        # 写入的jpg将其组合成pdf
        filepath_jpgname = str(createpath) + "/" + str(jpgname)
        c.drawImage(filepath_jpgname, 0, 0, width, item_height)
        c.showPage()
    c.save()
    print("完成PDF：" + str(tempfilename))


# 这里是裁剪和转化pdf的多进程
# 开启多进程
def threadingcrop_pdf(number):
    # 进程数
    pool = ThreadPoolExecutor(int(number))
    # 读取文件夹名字
    namelist = listfiles(filepath, "png")

    # 进程开跑
    for name in namelist:
        print(name)
        pool.submit(cropimg_tranpdf, name)
        # 太快电脑受不了
        time.sleep(1)



# 这里传入的是pdf的名字
# 写入压缩文件
def zipfiles(names):
    # 需要压缩到的文件目录和名字
    zipname = str(outzipfilepath) + str(names.replace(".pdf", "")) + ".zip"
    # 需要压缩的文件位置和名字
    name = outpdffilepath + names
    files = zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED)

    # 写入压缩包
    files.write(name)
    files.close()
    print("完成压缩：" + str(zipname))


# 这里是压缩zip的多进程
# 开启多进程
def threadingzip(number):
    # 先转化为pdf
    threadingcrop_pdf(number)
    # 进程数
    pool = ThreadPoolExecutor(int(number))
    # 读取文件名字
    namelist = listfiles(outpdffilepath, "pdf")
    # 进程开跑
    for name in namelist:
        print(name)
        pool.submit(zipfiles, name)
        # 太快电脑受不了
        time.sleep(1)


if __name__ == '__main__':
    # 多进程
    #number = 8
    #threadingzip(number)

    # 写入pdf
    namelistpdf = listfiles(filepath, "png")
    for name in namelistpdf:
        print(name)
        cropimg_tranpdf(name)

    # 写入zip
    namelistzip = listfiles(outpdffilepath, "pdf")
    for name in namelistzip:
        print(name)
        #zipfiles(name)