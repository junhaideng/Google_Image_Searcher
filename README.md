## Google_Image_Searcher

### 1. requirements

- selenium
- beautifulsoup4
- requests

### 2. How does it work

The mirror website is : [https://images.wjbaike.site/imghp](https://images.wjbaike.site/imghp)

Its main steps are as follows:

<img src='process.png' >

### 3. How to use

1. 在main.py 同目录下新建一个upload文件夹(或者可以在`初始化`的时候指定自己的上传文件夹名称)
2. 在upload文件夹中上传自己的图片
3. 运行main.py，即可在同目录下的`download`(可自定义)文件夹中获取搜索到的图片(暂且仅获取搜索页面的第一页)
