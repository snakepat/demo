#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了
import requests
import os
import sys #用以获取输入参数
import platform #用以判断当前系统是什么系统
import math 
import hashlib


if(platform.system()=='Windows'):
    path_separator = "\\"    
elif(platform.system()=='Linux'):
    path_separator = "/"
else:
    assert 0, '该系统目前只能在linux和windows下执行'

chunk_size = 1024*1024*4 

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
    # 遍历当前文件，找出符合要求的文件，将路径添加到l中
    for x in os.listdir(pathcurrent):
        pathson = os.path.join(pathcurrent,x)
        if os.path.isfile(pathson):
            if string in x :
                file_dir.append(pathson)
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
            if os.path.isdir(pathson) and not os.path.basename(pathson).startswith('.') :#排除隐藏文件
                deeper_dir(string, pathson)

#排除file_dir中本程序所用文件
def del_file(string):
    if string in file_dir:
        file_dir.remove(string)
    else:
        print( "%s isn't in the file_dir",string)

    return

#排除file_dir中本程序所用脚本或文件
def del_default_file():
    pathcurrent = os.path.dirname(os.path.abspath(__file__))
    del_file(os.path.join(pathcurrent,"testing.py"))
    del_file(os.path.join(pathcurrent,"README.md"))
    del_file(os.path.join(pathcurrent,"fsave.ini"))
    return

#文件加密处理，可选服务，针对百度网盘的和谐功能
def Encrypt_Compression():


    return

#功能：        文件分片,分片为固定大小
#输入：        需要被分片的文件路径
#返回：        被分片的子文件路径
#补充说明：    
def Split_file(file_path):
    current_path = os.path.dirname(file_path)
    filename = file_path.split(path_separator)[-1:][0]
    total_size = os.path.getsize(file_path)
    current_chunk = 0
    #根据目标大小获得分片数目
    total_chunk = math.ceil(total_size/chunk_size)
    #用来存贮分片文件路径的
    slice_filepath_list = []
    while current_chunk < total_chunk:
        start = current_chunk*chunk_size
        end = min(total_size, start+chunk_size)
        with open(file_path, 'rb') as f1:
            f1.seek(start)
            file_chunk_data = f1.read(end-start)
            slice_filename = "{fname}_{i}".format(fname = filename, i = current_chunk)
            slice_filepath = os.path.join(current_path,slice_filename)
            f2 = open(slice_filepath,"wb")
            f2.write(file_chunk_data)      
            f2.close
            slice_filepath_list.append(slice_filepath)
        current_chunk = current_chunk + 1


    return slice_filepath_list

#使用hashlib库获得文件的MD5加密信息
def get_md5(path):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    return md5code

#预上传
def Panbaidu_pre_upload():
    
    return


if __name__ == '__main__':
    #迭代获取所有子文件并把它们的路径保存到file_dir = []中
    # deeper_dir()
    # # print("%s\n",file_dir)
    # #排除本程序所用脚本文本
    # del_default_file()
    # # print("%s\n",file_dir)
    
    # path = file_dir[0]
    # print(path)
    # statinfo = os.stat(path)
    # print(statinfo)
    # file_dir.remove()

    # teststring = "E:\\code\\git\\demo\\test\\头像与背景\\头像与背景.zip"
    teststring = "/root/temp/2023.tar"
    slice_filepath_list = Split_file(teststring)
    print(slice_filepath_list)
    for filepath in slice_filepath_list:
        value_md5 = get_md5(filepath)
        print(value_md5)
    # print(os.path.getsize(teststring))













#部分内容学习参考自如下网站:
# https://blog.csdn.net/moshlwx/article/details/52694397