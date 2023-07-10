#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

import fsave
import sys #用以获取输入参数
import os

if __name__ == '__main__':

    fsave.Onedrive_First_Access_Token()
    fsave.Onedrive_Refresh_Access_Token()

    arguments = sys.argv[1:]
    print(arguments)

    for filepath in arguments:
        #test
        print(os.path.exists(filepath))
        if os.path.exists(filepath):
            # default_path = "/fsave"#百度开发平台要求的格式,也是本软件的命名方式          
            # current_path = os.path.join(default_path,filepath)
            # current_path = current_path.replace('\\','/')
            # print(current_path)
            #如果是绝对路径的话，就把该路径的父路径给替换了
            father_path = os.path.dirname(os.path.abspath(__file__))
            filename =filepath.split(father_path)[-1:][0]

            #上传OneDrive的步骤
            json_pre_response = fsave.Onedrive_pre_upload(filename)
            fsave.Onedrive_upload(filepath,json_pre_response['uploadUrl'])
        else:
            print("不存在该路径")
            assert 0
