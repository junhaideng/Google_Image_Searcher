from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import base64
import hashlib

import threading


class Loading(threading.Thread):
    def __init__(self, name=None):
        super().__init__()
        self.name = name

    def run(self):
        while True:
            for i in ["|", "/", "-", "\\"]:
                print(f"\b{i}", flush=True, end='')
                time.sleep(0.2)


class GoogleSearcher:
    def __init__(self, upload="upload",
                 download="download", sleep_time=6, mode='file'):
        super().__init__()
        self._upload = upload  # 上传的图片所在目录
        self._download = download  # 下载的文件
        self.sleep_time = sleep_time  # 下载网页源代码所等待的时间
        self.mode = mode  # 指定两种模式，一种是直接在upload文件中存放图片内容，另外一种是在upload中存放文件夹

        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

        if not os.path.exists(self.download):
            os.mkdir(self.download)  # 储存下载的文件

        if not os.path.exists(self._upload):
            os.mkdir(self._upload)  # 储存上传的文件

    @property
    def upload(self):
        return self.upload

    @upload.setter
    def upload(self, upload):
        self._upload = upload

    @property
    def download(self):
        return self._download

    @download.setter
    def download(self, download):
        self._download = download

    def upload_img_get_html(self, file):
        """上传图片，并获取对应的html源码"""
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(options=option)  # 此时将webdriver.exe 保存到python Script目录下

        driver.get("https://images.wjbaike.site/imghp")

        # 等待输入框右边的相机图片出现
        condition_1 = expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "LM8x9c"))
        WebDriverWait(driver, timeout=20, poll_frequency=0.5).until(condition_1)
        # 出现之后点击该按钮
        image_button = driver.find_element_by_class_name("LM8x9c")
        image_button.send_keys(Keys.ENTER)

        # 等待界面上出现upload an image
        condition_2 = expected_conditions.visibility_of_element_located(
            (By.ID, "qbug"))
        WebDriverWait(driver, timeout=200, poll_frequency=0.5).until(
            condition_2)

        # 转化到 upload an image
        upload = driver.find_element_by_xpath('//*[@id="qbug"]/div/a')
        upload.send_keys(Keys.ENTER)

        # 查找文件上传的input
        condition_3 = expected_conditions.visibility_of_element_located(
            (By.ID, 'qbfile'))
        WebDriverWait(driver, timeout=100, poll_frequency=0.5).until(
            condition_3)
        input_ = driver.find_element_by_id('qbfile')

        # 上传文件，此处由于图片的控件是个input，可以直接使用send_keys
        input_.send_keys(file)

        # 当转到另外一个页面的时候
        condition_4 = expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="top_nav"]'))
        WebDriverWait(driver, timeout=20, poll_frequency=0.5).until(condition_4)
        # driver.implicitly_wait(20)

        time.sleep(self.sleep_time)  # 网络好一点的话可以调小一点

        # current_url = driver.current_url
        # return self.get_html(current_url)

        # 可能本地网络不太好，使用下面的方法的时候比较容易出现错误
        # print(driver.current_url)
        # print(driver.page_source)

        return driver.page_source

    def get_html(self, url):
        """获取网页的源代码"""
        session = requests.session()
        response = session.get(url, headers=self.header)
        response.encoding = response.apparent_encoding
        try:
            response.raise_for_status()
        except:
            return None
        else:
            return response.text

    def get_img_list(self, path=None):
        """需要查询的文件放在同目录的img下面,返回图片列表"""
        if path is None:
            cwd = os.getcwd()
            img_folder = cwd + "\\{}\\".format(self._upload)
        else:
            img_folder = path + "\\"
        return [img_folder + i for i in os.listdir(img_folder)]

    def download_img_via_url(self, url, filename):
        """以url形式下载图片"""
        img_name = str(filename) + ".png"
        img_name = self.process_filename(img_name)
        if url.startswith("//"):
            url = "http:" + url
        response = requests.get(url, headers=self.header)
        response.encoding = response.apparent_encoding
        try:
            response.raise_for_status()
        except:
            pass
        else:
            if not os.path.exists(img_name):
                with open(img_name, 'wb', errors='ignore') as file:
                    file.write(response.content)
            else:
                with open(img_name, 'wb', errors='ignore') as file:
                    file.write(response.content)

    @staticmethod
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

    def analyse(self, html, img_dir, data_text_name):
        """
        解析html, 下载网页中的图片和文本
        """
        soup = BeautifulSoup(html, "lxml")

        # 查找图片， 页面中需要的图片都是base64 的加密形式
        pattern = re.compile("<script.*?>.*?(data:image.*?)['|\"];.*?</script>",
                             re.I | re.M)
        for i, s in enumerate(re.findall(pattern, html)):
            self.download_img_via_base64(s, img_dir + '/' + str(i))

        # 网页的文本信息
        text = soup.find("div", id='search').get_text()
        data_text_name = str(data_text_name) + ".txt"
        data_text_name = self.process_filename(data_text_name)
        with open(data_text_name, "w", errors='ignore') as file:
            file.write(text)

    @staticmethod
    def process_filename(filename):
        """将文件名进行处理，尽量避免出现同名的文件"""
        if os.path.exists(filename):
            md = hashlib.md5()
            md.update("就用这个加密吧".encode("utf-8"))
            hexdigest = md.hexdigest()
            basename, extend = os.path.splitext(filename)
            filename = basename + "_" + hexdigest[-3:] + extend
            return filename
        else:
            return filename

    @staticmethod
    def is_img(img_path):
        """简单的先判断该文件是否是图片类型"""
        ext = os.path.splitext(img_path)[1]
        if ext in [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"]:
            return True
        else:
            return False

    def file_run(self, img_list):
        """文件夹下面是图片"""
        for i, img in enumerate(img_list):
            if os.path.isfile(img):
                img_name = os.path.splitext(os.path.split(img)[1])[0]  # 所要上传图片的名字
                print("正在处理文件 {}  ".format(img_name), end=" ")
                loading = Loading()
                loading.setDaemon(True)
                loading.start()
                if self.is_img(img):
                    # 在对应的目录下创建新的目录来储存对应获取的内容
                    this_download_dir = self._download + "\\" + img_name

                    if not os.path.exists(this_download_dir):
                        os.mkdir(this_download_dir)

                    html_name = self.process_filename("{}.html".format(this_download_dir + "/" + img_name))
                    html_source = self.upload_img_get_html(img)  # 获取上传图片之后获取的html source
                    with open(html_name, 'w', encoding='utf-8', errors='ignore') as file:
                        file.write(html_source)
                    self.analyse(html_source, this_download_dir, this_download_dir + "/" + img_name)  # 解析网页，下载图片，写入网页文本
                    print("\n图片{}处理完成\n".format(img_name))
                else:
                    print(f"文件 {img_name} 不是图片类型文件")

            else:
                continue

    def run(self):
        file_list = self.get_img_list()  # 先获取所有需要上传的图片

        if not file_list:
            print(self._upload + " 中间无内容")
            return

        if self.mode == 'file':
            self.file_run(file_list)
        elif self.mode == 'folder':
            temp_download = self._download
            for folder in file_list:
                if os.path.isdir(folder):
                    self._download = os.path.join(self._download, os.path.split(folder)[1])
                    if not os.path.exists(self._download):
                        os.mkdir(self._download)
                    img_list = self.get_img_list(folder)
                    self.file_run(img_list)
                self._download = temp_download
        else:
            raise Exception(f"No mode called {self.mode}")


if __name__ == "__main__":
    test = GoogleSearcher(mode='file')

    test.run()
