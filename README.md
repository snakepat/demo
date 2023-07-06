### 还可以改进的地方：

1. 执行linux命令以获得所有文件的操作权-用于删除等操作

2. 对响应的成功与否进行判断。
3. 设置更新功能，把fsave.ini文件清处理成为初始状态
4. 可以通过https://graph.microsoft.com/v1.0/me/drive可以知道目标Onedrive是否是onedriveofbusiness
5. refresh更新的频率
6. 添加对readme.md是否存在的判断，不然运行可能会判错



### 问题的解决进程

鲁棒性出现大问题——但是在我1G的微软免费VPS下却能流畅运行，可能跟网络链接有关，也可能跟win11的臃肿有关

关于refresh更新，需要注意OneDrive for business与一般OneDrive账号的参数有些不同，我仔细看文档才发现的。——而且文档里有不少内容已经过期了，蛋疼，什么sb操作。





