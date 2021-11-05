import os, sys
import math
from PIL import Image


def concatenate(name1, name2, name3, new):
    try:
        im1 = Image.open(name1)
        im2 = Image.open(name2)
        im3 = Image.open(name3)

        mult = (im1.height/2) / im2.height
        im2 = im2.resize(size=(math.floor(im2.width*mult), math.floor(im2.height*mult)))
        wd = im2.width / im3.width
        hd = min(im2.height, im1.height - im2.height) / im3.height

        if wd > hd:
            im3 = im3.resize(size=(math.floor(im3.width*hd), math.floor(im3.height*hd)))
        else:
            im3 = im3.resize(size=(math.floor(im3.width*wd), math.floor(im3.height*wd)))

        imnew = Image.new("RGB", (im1.width + im2.width, max(im1.height, im2.height + im3.height)), (255, 255, 255))
        imnew.paste(im1, (0, 0, im1.width, im1.height))
        imnew.paste(im2, (im1.width, 0, im1.width + im2.width, im2.height))
        imnew.paste(im3, (im1.width, im2.height, im1.width + im3.width, im2.height + im3.height))
        imnew.save(new)
        print("success concatenation", name1, name2, name3, new)

    except OSError:
        print("cannot convert", name1, name2, name3, new)


def sortfilesbydate(flist):
    def compare(file1, file2):
        if os.path.getmtime(file1) > os.path.getmtime(file2):
            return -1
        else:
            return 1
    from functools import cmp_to_key
    flist.sort(key=cmp_to_key(compare), reverse=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong arguments, please specify path to directory with pictures, "
              "and path to directory with output pictures")
        quit()

    filelist = os.listdir(sys.argv[1])
    filelist = ['{0}/{1}'.format(sys.argv[1], element) for element in filelist]
    if len(filelist) % 3 != 0:
        print("Error: amount of pictures is not a multiple of three")
        quit()
    sortfilesbydate(filelist)

    for i in range(len(filelist)//3):
        concatenate(filelist.pop(), filelist.pop(), filelist.pop(), sys.argv[2] + "/" + str(i) + ".jpg")
