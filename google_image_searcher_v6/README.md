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
|url| 搜索网站地址 | https://shitu.paodekuaiweixinqun.com/searchbyimage/upload or https://www.google.com/searchbyimage/upload|

### 日志
11/24：由于镜像网站配置原因，使用该方法目前无法正确请求到信息，go 版本仍然正确，或者可以使用 VPN，https://images.google.com/ 使用该方法可以正常执行，可将配置中的 mirror 设置为 false

2021/1/7: 网站目前可以通过 `requests.post` 方式直接进行文件的上传，该版本可以直接使用，如需使用二进制文件，请到 [go-gis release](https://github.com/junhaideng/go-gis/releases)页面进行下载下载

2021/1/30：镜像网站请求链接发生改变，镜像网站更新为 https://images.soik.top  相应接口更新为 https://images.soik.top/searchbyimage/upload

2022/1/24：自定义设置请求地址，需满足镜像和原站一致