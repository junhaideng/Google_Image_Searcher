# coding=utf-8
import os
import re
import time
from tkinter.messagebox import NO
import traceback
from urllib.parse import urlparse

import requests
import tqdm
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore

from settings import load_settings
from utils import download_img_via_base64, is_img, welcome

# 避免警告
urllib3.disable_warnings()


class GoogleSearcher:
    def __init__(self):
        super().__init__()
        welcome()
        settings = load_settings()
        self._upload = settings['upload']  # 上传的图片所在目录
        self._download = settings['download']  # 下载的文件
        self.separate = settings["separate"]  # 是否分割开下载的数据文件和当前的图片
        self.extention = settings["extention"]
        self.session = requests.Session()
        self.url = settings["url"]
        self.getOriginPic = settings["getOriginPic"]  # 是否下载原始图片

        # 解析 url 获取主机号
        result = urlparse(self.url)

        self.session.headers = {
            "Host": result.netloc,
            "Origin": result.netloc,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44",
        }

        self.session.verify = False

    def upload_img_get_html(self, file):
        """上传图片，并获取对应的html源码"""
        print(f"{Fore.GREEN}开始上传图片 {os.path.split(file)[1]} {Fore.RESET}")

        files = {
            "encoded_image": open(file, "rb")
        }
        data = {
            "image_url": "",
            "image_content": "",
            "filename": "",
            "hl": "hl"
        }
        res = self.session.post(self.url, files=files, data=data)
        res.encoding = res.apparent_encoding

        print(f"{Fore.GREEN}网页源码获取完成{Fore.RESET}")
        return res.text

    def analyse(self, html, img_dir, data_text_name):
        """
        解析html, 下载网页中的图片和文本
        """
                  
        try:
            soup = BeautifulSoup(html, "lxml")

            # 查找图片， 页面中需要的图片都是base64 的加密形式
            pattern = re.compile("<script.*?>.*?(data:image.*?)['|\"];.*?</script>",
                                 re.I | re.M)

        except:
            html_name = "{}.html".format(os.path.join(img_dir, "a"))
            with open(html_name, 'w', encoding='utf-8', errors='ignore') as file:
                file.write("<!--下载源码时间: " + time.asctime() + " -->")
                file.write(html)
            raise
          
        try:
            # 图片的相关label之类的
            possible_related_search = soup.findAll(
                "a", {"class": "fKDtNb"})[0].get_text()

            # 对网页的内容进行过滤
            for i in soup.find_all("script"):
                i.decompose()

            for i in soup.find_all("h1", {"class": "bNg8Rb"}):
                i.decompose()

            for i in soup.find_all("h2", {"class": "bNg8Rb"}):
                i.decompose()

            for i in soup.find_all("style"):
                i.decompose()

            text = soup.findAll("div", {"id": "search"})[
                0].get_text(separator="\n")
            text = re.sub("Reported.*?Done", "", text, flags=re.M | re.I | re.S)
            data_text_name = str(data_text_name) + ".txt"

            with open(data_text_name, "w", errors='ignore', encoding='utf-8') as file:
                file.write(possible_related_search + "\n" + text)
        except:
            pass
          
        print("开始下载图片")
        if not self.getOriginPic:
            # 下载图片
            t = tqdm.tqdm(total=len(re.findall(pattern, html)), dynamic_ncols=True)
            for i, s in enumerate(re.findall(pattern, html)):
                t.set_description(f"下载第{i + 1}张")
                download_img_via_base64(s, img_dir + '/' + str(i))
                t.update(1)
            t.close()
        else:
            # `Visually similar images` 链接
            title_link = soup.find("title-with-lhs-icon a")
            # 可能没有相似的图片，直接返回
            if title_link is None:
              return 
            pic_url = self.url.split("searchbyimage/upload")[0] + title_link.attrs['href']
            r = self.session.get(pic_url)
            l = re.findall(
                r'"(.*?)",[0-9]+,[0-9]+', r.text)
            pics = list()
            for i in l:
                if i[-4:] == ".jpg" or i[-4:] == ".png":
                    pics.append(i)

            pic_count = 0
            for n, pic in enumerate(pics):
                retry_count = 3
                if pic_count >= 30:
                    break
                while True:
                    try:
                        imageText = 'img_none'
                        print(pic)
                        image = requests.get(pic)
                        imageText = image.text
                        f = open(os.path.join(img_dir, str(n) + pic[-4:]), 'wb')
                        # 将下载到的图片数据写入文件
                        f.write(image.content)
                        f.close()
                        pic_count += 1
                        break
                    except Exception as e:
                        retry_count -= 1
                        print(repr(e))
                        print(imageText)
                        if retry_count <= 0:
                            print("跳过")
                            break
                        continue


    def single_file_run(self, img, download_path):
        """对单独的一个文件进行搜索"""
        if os.path.isfile(img):  # 这里的img是一个完成的路径
            img_name = os.path.splitext(os.path.split(img)[1])[0]  # 所要上传图片的名字

            print("--> 正在处理图片:  {}  ".format(img_name))
            if is_img(img, self.extention):
                # 在对应的目录下创建新的目录来储存对应获取的内容
                this_download_dir = os.path.join(
                    download_path, img_name + "_search_data_folder")

                if not os.path.exists(this_download_dir):
                    os.mkdir(this_download_dir)

                while_count = 3  # 图片下载尝试次数
                while True:
                    try:
                        html_source = self.upload_img_get_html(
                            img)  # 获取上传图片之后获取的html source

                        self.analyse(html_source, this_download_dir,
                                     this_download_dir + "/" + img_name)  # 解析网页，下载图片，写入网页文本

                        print("{}图片{}处理完成\n{}".format(Fore.GREEN, img_name, Fore.RESET))
                        break
                    except:
                        while_count -= 1
                        traceback.print_exc()
                        time.sleep(1)
                        if while_count <= 0:
                            break
                        continue
            else:
                print(f"{Fore.RED}文件 {img_name} 不是图片类型文件{Fore.RESET}")

    def run(self):
        cwd = os.getcwd()
        upload_path = os.path.join(cwd, self._upload)
        temp = self._download
        for i in os.walk(upload_path):
            current_upload_directory = i[0]

            if self.separate:
                related_upload = current_upload_directory.split(
                    self._upload)[1].lstrip("\\").lstrip("/")
                related_download = os.path.join(self._download, related_upload)
                download = os.path.join(cwd, related_download)
            else:
                download = current_upload_directory

            if not os.path.exists(download):
                os.mkdir(download)

            if i[-1]:  # 同一目录下的文件列表
                for oswalk in os.walk(download):
                    all_folder = oswalk[1]
                    all_num = list()
                    for u in all_folder:
                        for oswalk in os.walk(os.path.join(download, u)):
                            if len(oswalk[2]) == 0:
                                print("空文件夹", oswalk[0])
                            else:
                                all_num.append(u.split('_')[0])
                    break
                for j in i[-1]:  # 每一个文件
                    if j.split('.')[0] in all_num:
                        print(j, "pass")
                        continue
                    img_path = os.path.join(current_upload_directory, j)
                    self.single_file_run(img_path, download)
                    # time.sleep(10)


if __name__ == "__main__":
    start_time = time.time()
    test = GoogleSearcher()

    test.run()
    end_time = time.time()

    print(f"{Fore.GREEN}Cost: {end_time - start_time} {Fore.RESET}")
