### 使用方法
在第一次运行main.py的时候，会生成一个json配置文件，在配置文件中配置好之后便可以运行

相关配置:
| 属性名 | 解释| default|
|---|---|--|
|upload|图片上传路径目录，必须存在对应的目录|upload|
|download|搜索之后包括图片在内的数据下载的目录|download|
|separate|搜索之后的数据是否与原来的图片分离| true|
|extention|过滤上传的图片类型后缀| [".bmp", ".jpg", ".jpeg", ".tif", ".tiff", ".jfif", ".png", ".gif", ".iff", ".ilbm"]|
|sleep_time| 睡眠时间，因为部分网页加载需要一定的时间| 6|
|webdriver_path| webdriver的路径| |
|brower| 浏览器类型| firefox  或者 chrome|
|profile_path| 浏览器用户数据目录| |
|mirror| 是否使用镜像网站|true|

profile_path 的设置请参加: [这里](https://blog.csdn.net/weixin_44676081/article/details/106322068)
