## Google 以图搜图

**旨在通过 Google 或者相关镜像网站达到获取现有图片的相似图片**。

请使用最新提交代码，见 [v6](google_image_searcher_v6)，`v6 中直接向接口 POST 数据，速度较之前大幅度提升` :tada:

另外也使用 Go 进行了实现([点这里](https://github.com/junhaideng/go-gis))，速度更快:tada:，并且提供[二进制可执行文件](https://github.com/junhaideng/go-gis/releases)。
<hr/>

## 旧版本

### 1. requirements

- selenium
- beautifulsoup4
- requests
- Chrome & webdriver(`under the Python Script folder`)

### 2. How does it work

The mirror website is : [https://images.wjbaike.site/imghp](https://images.wjbaike.site/imghp) (**目前该镜像网站会自动重导向到google.com.hk，需要能够访问google才能进行搜索**， 可使用VPN或者 [浏览器插件](https://github.com/Cyberist-Edgar/Google-visit-helper))

Its main steps are as follows:

<img src='process_2.png' >

### 3. How to use

1. 在main.py 同目录下新建一个upload文件夹(或者可以在`初始化`的时候指定自己的上传文件夹名称)
2. 在upload文件夹中上传自己的图片
3. 运行main.py，即可在同目录下的`download`(可自定义)文件夹中获取搜索到的图片(暂且仅获取搜索页面的第一页)


:star: 建议使用最新版本 :star:

### 4. New features
- #### `version 2`
  
  - 自定义睡眠时间  
  
    >  根据用户的网络情况，用户可以更改爬取网页时等待网页加载完全的时间，默认为6s
  
  - 支持两种模式(以后版本中已经撤销)
  
    - 文件模式
  
      > 图片文件直接放在`upload`文件夹下面
  
    - 文件夹模式
  
      > 图片以不同的文件夹位于`upload`文件夹下面，即upload文件夹下面的文件夹里面包含图片

- #### `version 3`
  - 自动识别上传文件夹下的为包含图片的文件夹还是直接为图片，但目前仅支持upload文件夹中的文件夹必须是包含图片，如果包含其他的文件夹，不能再进行递归
  

- #### `version 4`
  - 自动递归识别文件夹中的内容，无论图片位置如何放置，皆可进行搜索

- #### `version 4.1`
  - 在version 4 由于镜像问题进行改进，并添加进度条显示，由于含有插件`Ghelper`, 速度大幅度提升
 
- ### `version 5` 
  - 将配置放置在json文件中，更加灵活
 
 <hr/>

<table>
    <tr>
    <th>version</th>
    <th>自动识别图片类型文件</th>
    <th>upload模式(file/folder)</th>
    <th>递归upload文件夹下载图片</th>
    </tr>
    <tr>
        <td>1</td>
        <td>✖</td>
        <td>✖</td>
        <td>✖</td>
    </tr>
      <tr>
        <td>2</td>
          <td>✔</td>
        <td>✔</td>
        <td>✖</td>
    </tr>
      <tr>
        <td>3</td>
          <td>✔</td>
        <td>✖</td>
        <td>✖</td>
    </tr>
      <tr>
        <td>4</td>
        <td>✔</td>
            <td>✖</td>
        <td>✔</td>
    </tr>
  <tr>
        <td>5</td>
        <td>✔(可自定义)</td>
            <td>✖</td>
        <td>✔</td>
    </tr>
</table>


### 更新：
2020/6/26： 镜像网站可以正常访问，点击[这里](https://images.hk.53yu.com/imghp)
