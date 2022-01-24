[![test](https://github.com/junhaideng/Google_Image_Searcher/actions/workflows/test.yml/badge.svg)](https://github.com/junhaideng/Google_Image_Searcher/actions/workflows/test.yml)
### 使用方法
在第一次运行 main.py 的时候，会生成一个 json 配置文件，在配置文件中配置好之后便可以运行

相关配置:
| 属性名 | 解释| default|
|---|---|--|
|upload|图片上传路径目录，必须存在对应的目录|upload|
|download|搜索之后包括图片在内的数据下载的目录|download|
|separate|搜索之后的数据是否与原来的图片分离| true|
|extention|过滤上传的图片类型后缀| [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"]|
|url| 搜索网站地址 | 默认： https://www.google.com/searchbyimage/upload|

Google 镜像获取可以见 [https://github.com/hmsjy2017/Google-Mirrors](https://github.com/hmsjy2017/Google-Mirrors)，搬运如下，选择的镜像必须和 Google 保持高度一致，**url 必须对应图片上传路径**，一般添加 `/searchbyimage/upload` 即可。
```
https://eurybia.サクラ.tw

https://anemoi.shuu.cf/

https://search.サクラ.tw

https://atlas.サクラ.tw

https://juno.shuu.cf/

https://ceres.shuu.cf/

https://diana.shuu.cf/

https://search.iwiki.uk/

https://mars.shuu.cf/

https://g20.i-research.edu.eu.org/

http://www.google.cn.ua/

https://txt.guoqiangti.ga

https://g3.luciaz.me/
```

> 注意部分网址中含有的字符比较特殊，比如 https://search.サクラ.tw，需要从开发者工具中的 Network 一栏获取到更一般的请求路径，比如上述的网址对应 https://search.xn--u8jta9j.tw

### 日志
11/24：由于镜像网站配置原因，使用该方法目前无法正确请求到信息，go 版本仍然正确，或者可以使用 VPN，https://images.google.com/ 使用该方法可以正常执行，可将配置中的 mirror 设置为 false

2021/1/7: 网站目前可以通过 `requests.post` 方式直接进行文件的上传，该版本可以直接使用，如需使用二进制文件，请到 [go-gis release](https://github.com/junhaideng/go-gis/releases)页面进行下载下载

2021/1/30：镜像网站请求链接发生改变，镜像网站更新为 https://images.soik.top  相应接口更新为 https://images.soik.top/searchbyimage/upload

2022/1/24：自定义设置请求地址，需满足镜像和原站一致