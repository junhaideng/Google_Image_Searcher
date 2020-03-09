## Google_Image_Searcher

### 1. requirements

- selenium
- beautifulsoup4
- requests
- Chrome & webdriver(`under the Python Script folder`)

### 2. How does it work

The mirror website is : [https://images.wjbaike.site/imghp](https://images.wjbaike.site/imghp)

Its main steps are as follows:

<img src='process_2.png' >

### 3. How to use

1. 在main.py 同目录下新建一个upload文件夹(或者可以在`初始化`的时候指定自己的上传文件夹名称)
2. 在upload文件夹中上传自己的图片
3. 运行main.py，即可在同目录下的`download`(可自定义)文件夹中获取搜索到的图片(暂且仅获取搜索页面的第一页)


### 4. New features
- #### `version 2`
  
  - 自定义睡眠时间  
  
    >  根据用户的网络情况，用户可以更改爬取网页时等待网页加载完全的时间，默认为6s
  
  - 支持两种模式
  
    - 文件模式
  
      > 图片文件直接放在`upload`文件夹下面
  
    - 文件夹模式
  
      > 图片以不同的文件夹位于`upload`文件夹下面，即upload文件夹下面的文件夹里面包含图片

- #### `version 3`
  - 自动识别上传文件夹下的为包含图片的文件夹还是直接为图片，但目前仅支持upload文件夹中的文件夹必须是包含图片，如果包含其他的文件夹，不能再进行递归
  

- #### `version 4`
  - 自动递归识别文件夹中的内容，无论图片位置如何放置，皆可进行搜索
