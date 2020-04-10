# coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup
import os
import re
import time
import base64
import hashlib
import tqdm
from colorama import Fore

EXTEND = [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"]
USERNAME = os.environ['USERNAME']


class GoogleSearcher:
    def __init__(self, upload="upload",
                 download="download", sleep_time=6):
        super().__init__()
        self._upload = upload  # 上传的图片所在目录
        self._download = download  # 下载的文件
        self.sleep_time = sleep_time  # 下载网页源代码所等待的时间

        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"}

        if not os.path.exists(self.download):
            os.mkdir(self.download)  # 储存下载的文件

        if not os.path.exists(self._upload):
            os.mkdir(self._upload)  # 储存上传的文件

        self.option = webdriver.ChromeOptions()
        self.option.add_argument("--user-data-dir=" + f"C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data/")
        # self.option.add_argument("headless")  # 这样如果隐藏浏览器的话，容易报错
        self.option.add_argument("disable-gpu")

        self.driver = webdriver.Chrome(options=self.option)  # 此时将webdriver.exe 保存到python Script目录下

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
        print(f"{Fore.GREEN}开始上传图片 {os.path.split(file)[1]} {Fore.RESET}")
        # self.driver.get("https://images.wjbaike.site/imghp")
        self.driver.get("https://www.google.com/imghp")

        # 等待输入框右边的相机图片出现
        condition_1 = expected_conditions.visibility_of_element_located(
            (By.CLASS_NAME, "LM8x9c"))
        WebDriverWait(self.driver, timeout=20, poll_frequency=0.5).until(condition_1)
        # 出现之后点击该按钮
        image_button = self.driver.find_element_by_class_name("LM8x9c")
        image_button.send_keys(Keys.ENTER)

        # 等待界面上出现upload an image
        condition_2 = expected_conditions.visibility_of_element_located(
            (By.ID, "dRSWfb"))
        WebDriverWait(self.driver, timeout=20, poll_frequency=0.5).until(
            condition_2)

        # 转化到 upload an image
        upload = self.driver.find_element_by_xpath('//*[@id="dRSWfb"]/div/a')
        upload.send_keys(Keys.ENTER)

        # 查找文件上传的input
        condition_3 = expected_conditions.visibility_of_element_located(
            (By.ID, 'awyMjb'))
        WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(
            condition_3)
        input_ = self.driver.find_element_by_id('awyMjb')

        # 上传文件，此处由于图片的控件是个input，可以直接使用send_keys
        input_.send_keys(file)
        print(f"{Fore.GREEN}图片上传完成{Fore.RESET}")

        # 当转到另外一个页面的时候
        condition_4 = expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="top_nav"]'))
        WebDriverWait(self.driver, timeout=20, poll_frequency=0.5).until(condition_4)
        # driver.implicitly_wait(20)

        time.sleep(self.sleep_time)  # 网络好一点的话可以调小一点

        # current_url = driver.current_url
        # return self.get_html(current_url)

        # 可能本地网络不太好，使用下面的方法的时候比较容易出现错误
        # print(driver.current_url)
        # print(driver.page_source)
        print(f"{Fore.GREEN}网页源码获取完成{Fore.RESET}")
        return self.driver.page_source

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
        print("开始下载图片")
        t = tqdm.tqdm(total=len(re.findall(pattern, html)), dynamic_ncols=True)
        for i, s in enumerate(re.findall(pattern, html)):
            t.set_description(f"下载第{i + 1}张")
            self.download_img_via_base64(s, img_dir + '/' + str(i))
            t.update(1)
        t.close()

        # 网页的文本信息
        possible_related_search = soup.findAll("a", {"class": "fKDtNb"})[0].get_text()

        # 对网页的内容进行过滤
        for i in soup.find_all("script"):
            i.decompose()

        for i in soup.find_all("h1", {"class": "bNg8Rb"}):
            i.decompose()

        for i in soup.find_all("h2", {"class": "bNg8Rb"}):
            i.decompose()

        for i in soup.find_all("style"):
            i.decompose()

        text = soup.findAll("div", {"id": "search"})[0].get_text(separator="\n")
        text = re.sub("Reported.*?Done", "", text, flags=re.M | re.I | re.S)
        data_text_name = str(data_text_name) + ".txt"
        data_text_name = self.process_filename(data_text_name)
        with open(data_text_name, "w", errors='ignore', encoding='utf-8') as file:
            file.write(possible_related_search + "\n" + text)

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
        if ext in EXTEND:
            return True
        else:
            return False

    def simple_file_run(self, img):
        """对单独的一个文件进行搜索"""
        if os.path.isfile(img):
            img_name = os.path.splitext(os.path.split(img)[1])[0]  # 所要上传图片的名字
            # print("{}>>正在处理图片 {}  ".format(os.path.split(img)[0], img_name), end=" ")
            print("--> 正在处理图片:  {}  ".format(img_name))
            # loading = Loading()
            # loading.setDaemon(True)
            # loading.start()
            if self.is_img(img):
                # 在对应的目录下创建新的目录来储存对应获取的内容
                this_download_dir = self._download + "\\" + img_name + "_img_folder"

                if not os.path.exists(this_download_dir):
                    os.mkdir(this_download_dir)

                html_name = self.process_filename("{}.html".format(this_download_dir + "/" + img_name))
                html_source = self.upload_img_get_html(img)  # 获取上传图片之后获取的html source
                with open(html_name, 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(html_source)
                self.analyse(html_source, this_download_dir, this_download_dir + "/" + img_name)  # 解析网页，下载图片，写入网页文本
                print("{}图片{}处理完成\n{}".format(Fore.GREEN, img_name, Fore.RESET))
            else:
                print(f"{Fore.RED}文件 {img_name} 不是图片类型文件{Fore.RESET}")

    def run(self):
        cwd = os.getcwd()
        upload_path = os.path.join(cwd, self._upload)
        temp = self._download
        for i in os.walk(upload_path):
            directory = i[0]
            download = self._download + str(directory.split(self._upload, maxsplit=1)[1]).replace("\\", "\\\\")
            self._download = download
            if not os.path.exists(download):
                os.mkdir(download)
            if i[-1]:
                for j in i[-1]:
                    img_path = os.path.join(i[0], j)
                    self.simple_file_run(img_path)
            self._download = temp


if __name__ == "__main__":
    start_time = time.time()
    test = GoogleSearcher()

    test.run()
    end_time = time.time()

    print(f"{Fore.GREEN}Cost: {end_time-start_time} {Fore.RESET}")
