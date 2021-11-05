import os, sys
import math
from PIL import Image


def do_concatenate2(name1, name2, new):
    try:
        im1 = Image.open(name1)
        im2 = Image.open(name2)

        mult = im1.height / im2.height
        im2 = im2.resize(size=(math.floor(im2.width*mult), math.floor(im2.height*mult)))

        imnew = Image.new("RGB", (im1.width + im2.width, im1.height), (255, 255, 255))
        imnew.paste(im1, (0, 0, im1.width, im1.height))
        imnew.paste(im2, (im1.width, 0, im1.width + im2.width, im2.height))
        imnew.save(new)

        print("success concatenation of two", name1, name2, new)

    except OSError:
        print("cannot convert", name1, name2, new)
    pass


def do_concatenate3(name1, name2, name3, new):
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

        print("success concatenation of three", name1, name2, name3, new)

    except OSError:
        print("cannot convert", name1, name2, name3, new)


def do_concatenate4(name1, name2, name3, name4, new):
    try:
        im1 = Image.open(name1)
        im2 = Image.open(name2)
        im3 = Image.open(name3)
        im4 = Image.open(name4)

        mult12 = im1.height / im2.height
        im2 = im2.resize(size=(math.floor(im2.width*mult12), math.floor(im2.height*mult12)))

        mult13 = im1.width / im3.width
        im3 = im3.resize(size=(math.floor(im3.width * mult13), math.floor(im3.height * mult13)))

        wd = im2.width / im4.width
        hd = im3.height / im4.height

        if wd > hd:
            im4 = im4.resize(size=(math.floor(im4.width*hd), math.floor(im4.height*hd)))
        else:
            im4 = im4.resize(size=(math.floor(im4.width*wd), math.floor(im4.height*wd)))

        imnew = Image.new("RGB", (im1.width + im2.width, im1.height + im3.height), (255, 255, 255))
        imnew.paste(im1, (0, 0, im1.width, im1.height))
        imnew.paste(im2, (im1.width, 0, im1.width + im2.width, im2.height))
        imnew.paste(im3, (0, im1.height, im3.width, im1.height + im3.height))
        imnew.paste(im4, (im1.width, im2.height, im1.width + im4.width, im2.height + im4.height))
        imnew.save(new)

        print("success concatenation of four", name1, name2, name3, name4, new)

    except OSError:
        print("cannot convert", name1, name2, name3, name4, new)


def sortfilesbydate(flist):
    def compare(file1, file2):
        if os.path.getmtime(file1) > os.path.getmtime(file2):
            return -1
        else:
            return 1
    from functools import cmp_to_key
    flist.sort(key=cmp_to_key(compare), reverse=False)


def concatenate2(_in, _out):
    filelist = os.listdir(_in)
    filelist = ['{0}/{1}'.format(_in, element) for element in filelist]
    if len(filelist) % 2 != 0:
        print("Error: amount of pictures is not a multiple of two")
        quit()
    sortfilesbydate(filelist)

    for i in range(len(filelist)//2):
        do_concatenate2(filelist.pop(), filelist.pop(), _out + "/" + str(i) + ".jpg")


def concatenate3(_in, _out):
    filelist = os.listdir(_in)
    filelist = ['{0}/{1}'.format(_in, element) for element in filelist]
    if len(filelist) % 3 != 0:
        print("Error: amount of pictures is not a multiple of three")
        quit()
    sortfilesbydate(filelist)

    for i in range(len(filelist)//3):
        do_concatenate3(filelist.pop(), filelist.pop(), filelist.pop(), _out + "/" + str(i) + ".jpg")


def concatenate4(_in, _out):
    filelist = os.listdir(_in)
    filelist = ['{0}/{1}'.format(_in, element) for element in filelist]
    if len(filelist) % 4 != 0:
        print("Error: amount of pictures is not a multiple of four")
        quit()
    sortfilesbydate(filelist)

    for i in range(len(filelist)//4):
        do_concatenate4(filelist.pop(), filelist.pop(), filelist.pop(), filelist.pop(), _out + "/" + str(i) + ".jpg")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong arguments, please specify path to directory with pictures, "
              "and path to directory with output pictures")
        quit()

    mode = int(sys.argv[1])
    _input = sys.argv[2]
    _output = sys.argv[3]

    match mode:
        case 2:
            concatenate2(_input, _output)
            pass
        case 3:
            concatenate3(_input, _output)
            pass
        case 4:
            concatenate4(_input, _output)
            pass
