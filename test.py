#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

import sys #用以获取输入参数

if __name__ == '__main__':

    arguments = sys.argv[1:]

    for i in arguments:
        print(i)
