"""
有关设置的相关操作
generate_default_settings  --> 生成默认的设置文件
load_settings  --> 加载设置文件
validate  --> 对配置文件中的值进行检验
"""

import os
import json

SETTINGS_JSON = {
    "upload": "upload",  # 上传的图片库文件夹
    "download": "download",  # 下载的文件的所属文件夹，separate=True才生效
    "separate": True,  # 下载的文件和图片是否分离
    # "log": False,  # 生成log文件
    # "log_filename": "search.log",
    # 需要处理的图片后缀名
    "extention": [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"],
    "sleep_time": 6,  # 睡眠时间，部分操作需要休眠一段时间之后才能获取到对应的信息
    "webdriver_path": "",  # webdriver 的路径，如果webdriver在python Scripts下面，可以不声明，否则其他时候必须声明
    "brower": "firefox",  # 或者 chrome
    "profile_path": "",  # 是一个文件夹
    "mirror": True  # 是否使用镜像网站
}


def generate_default_settings():
    """
    generate default settings
    and you can modify it in the json file
    """
    if os.path.exists("google_image_search_settings.json"):
        print("The settings file has existed, if you want to generate again, first delete the settings file")
    else:
        json.dump(SETTINGS_JSON, open(
            "google_image_search_settings.json", mode='w'), indent=2)


def load_settings():
    """
    load the settings 
    """
    try:
        if os.path.exists("google_image_search_settings.json"):
            settings = json.load(open("google_image_search_settings.json", mode='r'))
            validate(settings)
            return settings
        else:
            # 如果设置文件不存在，抛出错误
            raise FileNotFoundError("settings file not exists")
    except FileNotFoundError:
        generate_default_settings()
        print("The settings has been generated successfully")
        print("Go and set your settings!")
        exit(0)
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
        if not "upload" in keys:
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
   
    def _check_log():
        if 'log' in keys:
            if not isinstance(settings["log"], bool):
                raise TypeError("expected bool, not {}".format(type(settings["log"]).__name__))
        else:
            raise AttributeError('Can not find attribute log')

    def _check_log_filename():
        if 'log_filename' in keys:
            if not isinstance(settings["log_filename"], str):
                raise TypeError("expected bool, not {}".format(type(settings["log_filename"]).__name__))
        else:
            raise AttributeError('Can not find attribute log filename')

    def _check_extention():
        if 'extention' in keys:
            if not isinstance(settings["extention"], list):
                raise TypeError("expected list, not {}".format(type(settings["extention"]).__name__))
        else:
            raise AttributeError("Can not find attribute extention")

    def _check_sleep_time():
        if "sleep_time" in keys:
            if not (isinstance(settings["sleep_time"], int) or isinstance(settings["sleep_time"], float)):
                raise TypeError("expected int or float, not {}".format(type(settings["sleep_time"]).__name__))
            elif settings["sleep_time"] < 0:
                raise ValueError("Sleep time should greater than 0!")
        else:
            raise AttributeError("Can not find attribute sleep time")

    def _check_webdriver_path():
        if "webdriver_path" in keys:
            if not isinstance(settings["webdriver_path"], str):
                raise TypeError("expected str, not {}".format(type(settings["webdriver_path"]).__name__))
            if not settings["webdriver_path"].strip(" "):
                return 
            if not os.path.isfile(settings["webdriver_path"]):
                raise ValueError(
                    "Webdriver is not existed in %s" % settings['webdriver_path'])
        else:
            raise AttributeError("Can not find attribute webdriver path")


    def _check_brower():
        if "brower" in keys:
            if not isinstance(settings['brower'], str):
                raise TypeError("expected str, not {}".format(type(settings["brower"]).__name__))
            else:
                if not settings["brower"].lower() in ["firefox", "chrome"]:
                    raise ValueError("invalid brower: {}, expected firefox, chrome".format(settings["brower"]))
        else:
            raise AttributeError("Can not find attribute brower")

    def _check_profile_path():
        if "profile_path" in keys:
            profile = settings["profile_path"]
            if not isinstance(profile, str):
                raise TypeError("expected str, not {}".format(type(profile).__name__))
            else:
                if not os.path.exists(profile):
                    raise ValueError("profile path {} not exists".format(profile))
                else:
                    if not os.path.isdir(profile):
                        raise NotADirectoryError("profile path is not a directory")
        else:
            raise AttributeError("Can not find attribute profile path")
    
    def _check_mirror():
        if "mirror" in keys:
            if not isinstance(settings["mirror"], bool):
                raise TypeError("expected bool, not {}".format(type(settings["mirror"]).__name__))
            else:
                raise AttributeError("Can not find attribute mirror")
    


    _check_upload()
    _check_separate()  # first to check separate, then check download
    _check_download()
    # _check_log()
    # _check_log_filename()
    _check_extention()
    _check_sleep_time()
    _check_webdriver_path()
    _check_profile_path()
    _check_mirror()

if __name__ == "__main__":
    # generate_default_settings()

    import time
    start_time  = time.time()
    print(load_settings())
    end_time = time.time()
    print(end_time-start_time)
