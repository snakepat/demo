#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了
import requests
import os
import sys #用以获取输入参数
import platform #判断当前系统是linux or window，因为路径分隔符的不同

file_dir = []#用来存贮这一次启用程序便利文件后得到的文件

#上传该目录文件下的所有文件到百度网盘/考虑以后还有上传的Onedrive的选项
def Panbaidu_upload():
    

    return

#第一次获得access—token的内容并保存到本地文件夹的fsave.ini文件中
def Panbaidu_First_Access_Token():


    return

#获得Access Token更新并保存到本地文件夹的fsave.ini文件中
def Panbaidu_Refresh_Access_Token():


    return


#遍历当前文件列表并存贮相关信息
# find_cur(string, path)实现对path目录下文件的查找，列出文件命中含string的文件
def find_cur(string, pathcurrent):
    # print('cur_dir is %s' % os.path.abspath(path))

    # 遍历当前文件，找出符合要求的文件，将路径添加到l中
    for x in os.listdir(pathcurrent):
        # print(path+'/'+x)
        if os.path.isfile(os.path.join(pathcurrent,x)):
            if string in x:
                file_dir.append(os.path.join(pathcurrent,x))
    #debug
    # if not l:
    #     # print('no %s in %s' % (string, os.path.abspath(path)))
    #     print("This is no file at all")
    # else:
    #     print(l)

#通过递归实现对当前目录下所有文件的遍历(包括子目录的文件)
# deeper_dir(string, p)主要通过递归，在每个子目录中调用find_cur()
def deeper_dir(string='', pathcurrent=os.path.dirname(os.path.abspath(__file__))): # '.'表示当前路径，'..'表示当前路径的父目录
    
    find_cur(string, pathcurrent)
    for x in os.listdir(pathcurrent):
        # 关键，将父目录的路径保留下来，保证在完成子目录的查找之后能够返回继续遍历。
        pathson = pathcurrent 
        if os.path.isdir(pathson):
            pathson = os.path.join(pathson, x)
            if os.path.isdir(pathson) and not os.path.basename(pathson).startswith('.'):#排除隐藏文件
                deeper_dir(string, pathson)


#文件加密处理，可选服务，针对百度网盘的和谐功能
def Encrypt_Compression():


    return

#预上传
def Panbaidu_pre_upload():
    
    return


if __name__ == '__main__':
    #迭代获取所有子文件并把它们的路径保存到file_dir = []中
    deeper_dir()
    
    path = file_dir[0]
    print(path)
    statinfo = os.stat(path)
    print(statinfo)
    # file_dir.remove()





#部分内容学习参考自如下网站:
# https://blog.csdn.net/moshlwx/article/details/52694397