### 还可以改进的地方：

1. 执行linux命令以获得所有文件的操作权-用于删除等操作
2. 对响应的成功与否进行判断。
3. 设置更新功能，把fsave.ini文件清处理成为初始状态
4. 可以通过https://graph.microsoft.com/v1.0/me/drive可以知道目标Onedrive是否是onedriveofbusiness
5. refresh更新的频率



### 总结一下之后要干啥

1. 尝试编写带参数的bash脚本，并在其中运行python脚本

2. 修改python函数当运行成功（寻找成功码）后删除相应文件，该文件应该在新的脚本中运行

3. 修改upload.sh函数实现文件的运行
4. 将token的更新设置为从服务器的数据库中获取
5. 爬虫之类的东西



### 问题的解决进程

鲁棒性出现大问题——但是在我1G的微软免费VPS下却能流畅运行，可能跟网络链接有关，也可能跟win11的臃肿有关

关于refresh更新，需要注意OneDrive for business与一般OneDrive账号的参数有些不同，我仔细看文档才发现的。——而且文档里有不少内容已经过期了，蛋疼，什么sb操作。





