"""
有关设置的相关操作
generate_default_settings  --> 生成默认的设置文件
load_settings  --> 加载设置文件
validate  --> 对配置文件中的值进行检验
"""

import json
import os

SETTINGS_JSON = {
    "upload": "upload",  # 上传的图片库文件夹
    "download": "download",  # 下载的文件的所属文件夹，separate=True才生效
    "separate": True,  # 下载的文件和图片是否分离
    # 需要处理的图片后缀名
    "extention": [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"],
    # https://shitu.paodekuaiweixinqun.com/searchbyimage/upload" -> 镜像
    "url": "https://www.google.com/searchbyimage/upload",  # 默认是 google 原像
    "getOriginPic": False
}


def generate_default_settings(file="settings.json"):
    """
    generate default settings
    and you can modify it in the json file
    """
    if os.path.exists(file):
        print("The settings file has existed, if you want to generate again, first delete the settings file")
    else:
        json.dump(SETTINGS_JSON, open(file, mode='w', encoding='utf8'), indent=2)


def load_settings(file="settings.json"):
    """
    load the settings 
    """
    try:
        if os.path.exists(file):
            settings = json.load(open(file, mode='r', encoding='utf8'))
            validate(settings)
            return settings
        else:
            # 如果设置文件不存在，抛出错误
            raise FileNotFoundError("settings file not exists")
    except FileNotFoundError:
        generate_default_settings()
        print("The settings has been generated successfully")
        return SETTINGS_JSON
    # except Exception as e:
    #     print(e)
    #     print("Can not load settings")
    #     exit(-1)


def validate(settings: dict):
    """
    check if the settings is validated
    """
    keys = settings.keys()

    def _check_upload():
        if "upload" not in keys:
            raise AttributeError("upload must exists")
        else:
            if not isinstance(settings["upload"], str):
                raise TypeError("expected str, not {}".format(type(settings["upload"]).__name__))
            else:
                if not os.path.exists(settings['upload']):
                    raise ValueError("Can not find the upload path")

    def _check_separate():
        if "separate" in keys:
            if not isinstance(settings['separate'], bool):
                raise TypeError("expected bool, not {}".format(type(settings["separate"]).__name__))
        else:
            raise AttributeError("Can not find attribute separate")

    def _check_download():
        if settings['separate']:
            return
        else:
            if 'download' in keys:
                if not isinstance(settings['download'], str):
                    raise TypeError("expected str, not {}".format(type(settings["download"]).__name__))
                else:
                    if not os.path.exists(settings['download']):
                        os.mkdir(settings['download'])

    def _check_extention():
        if 'extention' in keys:
            if not isinstance(settings["extention"], list):
                raise TypeError("expected list, not {}".format(type(settings["extention"]).__name__))
        else:
            raise AttributeError("Can not find attribute extention")

    _check_upload()
    _check_separate()  # first to check separate, then check download
    _check_download()
    _check_extention()


if __name__ == "__main__":
    # generate_default_settings()

    import time

    start_time = time.time()
    print(load_settings())
    end_time = time.time()
    print(end_time - start_time)
