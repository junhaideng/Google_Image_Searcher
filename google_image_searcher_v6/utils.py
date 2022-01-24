import re 
import os
import base64
import hashlib


def download_img_via_base64(string, filename):
        """当图片以base64形式存储在网页中时，可使用该方式下载该图片"""
        pattern = re.compile("data:image/(.*?);base64,(.*?$)", re.I | re.M)
        data = re.findall(pattern, string)[0]
        if not data[1].endswith("=="):
            data_ = data[1] + '=='
        else:
            data_ = data[1]
        img_data = base64.b64decode(data_)
        img_name = str(filename) + "." + data[0]
        with open(img_name, "wb") as file:
            file.write(img_data)

def process_filename(filename):
    """将文件名进行处理，尽量避免出现同名的文件"""
    if os.path.exists(filename):
        md = hashlib.md5()
        md.update("就用这个加密吧".encode("utf-8"))
        hexdigest = md.hexdigest()
        basename, extention = os.path.splitext(filename)
        filename = basename + "_" + hexdigest[-3:] + extention
        return filename
    else:
        return filename

def is_img(img_path, extention):
        """判断该文件是否是需要的图片类型"""
        ext = os.path.splitext(img_path)[1]
        if ext in extention:
            return True
        else:
            return False


def welcome():
    print("-----------------------------------------------------------")
    print("-                   Google Image Searcher                 -")
    print("-                      designed by Edgar                  -")
    print("-           for more detail usage, you can visit          -")
    print("-   https://github.com/junhaideng/Google_Image_Searcher   -")
    print("-----------------------------------------------------------")


if __name__ == "__main__":
    welcome()
