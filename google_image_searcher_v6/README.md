### 使用方法
在第一次运行main.py的时候，会生成一个json配置文件，在配置文件中配置好之后便可以运行

相关配置:
| 属性名 | 解释| default|
|---|---|--|
|upload|图片上传路径目录，必须存在对应的目录|upload|
|download|搜索之后包括图片在内的数据下载的目录|download|
|separate|搜索之后的数据是否与原来的图片分离| true|
|extention|过滤上传的图片类型后缀| [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"]|
|mirror| 是否使用镜像网站|true|

### 日志
11/24：由于镜像网站配置原因，使用该方法目前无法正确请求到信息，go版本仍然正确
