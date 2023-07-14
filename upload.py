#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

import fsave
import sys #用以获取输入参数
import os
import time
import logging
import configparser    #填写配置文件
import multiprocessing #创建多进程工作，尝试
import time


def onedrive_process(filename,filepath,result_queue_onedrive):

    #上传OneDrive的步骤
    json_pre_response = fsave.Onedrive_pre_upload(filename)
    status_of_upload = fsave.Onedrive_upload(filepath,json_pre_response['uploadUrl'])

    result_queue_onedrive.put(status_of_upload)

def baidu_process(filename,filepath,result_queue_panbaidu):
    
    if os.path.getsize(filepath) > fsave.panbaidu_chunk_size:
        slice_filepath_list = fsave.Split_file(filepath,fsave.panbaidu_chunk_size)
    else:
        slice_filepath_list = []
        slice_filepath_list.append(filepath)

    father_path = os.path.dirname(os.path.abspath(__file__))
    filename = filepath.split(father_path)[-1:][0]

    # print(slice_filepath_list)
    md5_list = []
    for filepath in slice_filepath_list:
        value_md5 = fsave.get_md5(filepath)
        md5_list.append(value_md5)
        
    # print(md5_list)

    size = os.path.getsize(filepath,error_num)
    json_pre_response = fsave.Panbaidu_pre_upload(filename, size , md5_list)
    # print(json_pre_response)

    fsave.Panbaidu_upload(filename,slice_filepath_list,json_pre_response['uploadid'])
    error_num = fsave.Panbaidu_createfile(filename,size,md5_list,json_pre_response['uploadid'])

    # return error_num
    result_queue_panbaidu.put(error_num)
    

if __name__ == '__main__':
    
    arguments = sys.argv[1:]
    # print(arguments)
    arguments = ["./testing/"]

    #配置日志
    logging.basicConfig(
        filename='upload.log',  # 日志文件路径
        level=logging.INFO,  # 设置日志级别为INFO
        format='%(asctime)s %(levelname)s %(message)s',  # 日志格式
        datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
    )
    
    for filepath in arguments:
        #test
        # print(os.path.exists(filepath))
        logging.info(f'This path is:{filepath}')
        
        if os.path.exists(filepath):
            #通过读取配置文件来判断是否需要上传文件到百度
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'rb') as o:
                config = configparser.ConfigParser()
                config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"))
                #更新access_token
                if(int(config.get("config_oneDrive","isupload"))==1):
                    fsave.Onedrive_First_Access_Token()
                    fsave.Onedrive_Refresh_Access_Token()
                if(int(config.get("config_panbaidu","isupload"))==1):
                    fsave.Panbaidu_First_Access_Token()
                    fsave.Panbaidu_Refresh_Access_Token()
                #如果是相对路径，转化为绝对路径
                #如果是绝对路径的话，就把该路径的父路径给替换了,这一步是找到文件路径
                filepath = os.path.abspath(filepath)
                father_path = os.path.dirname(filepath)

                #进程
                processes = []
                result_queue_ondrive = multiprocessing.Queue()  # 创建一个队列用于存储返回值
                result_queue_panbaidu = multiprocessing.Queue()  # 创建一个队列用于存储返回值

                if os.path.isdir(filepath):
                    fsave.deeper_dir('',filepath)
                    #test
                    print(fsave.file_dir)
                    for i in range(len(fsave.file_dir)):
                        filename = fsave.file_dir[i].split(father_path)[-1:][0]
                        if(int(config.get("config_panbaidu","isupload"))==1):
                            p = multiprocessing.Process(target=baidu_process, args=(filename,filepath,result_queue_panbaidu))
                            processes.append(p)
                            p.start()
                        if(int(config.get("config_oneDrive","isupload"))==1):
                            p = multiprocessing.Process(target=onedrive_process, args=(filename,filepath,result_queue_ondrive))
                            processes.append(p)
                            p.start()
                        
                        for p in processes:
                            p.join()
                        status_of_upload = result_queue_ondrive.get()
                        value_of_error = result_queue_panbaidu.get()

                else:
                    filename =filepath.split(father_path)[-1:][0]



                # fsave.Onedrive_First_Access_Token()
                # fsave.Onedrive_Refresh_Access_Token()
                # #如果是相对路径，转化为绝对路径
                # #如果是绝对路径的话，就把该路径的父路径给替换了,这一步是找到文件路径
                # filepath = os.path.abspath(filepath)
                # father_path = os.path.dirname(filepath)
            
                # if os.path.isdir(filepath):
                #     fsave.deeper_dir('',filepath)
                #     #test
                #     print(fsave.file_dir)
                #     for i in range(len(fsave.file_dir)):
                #         filename = fsave.file_dir[i].split(father_path)[-1:][0]
                #         json_pre_response = fsave.Onedrive_pre_upload(filename)
                #         status_of_upload = fsave.Onedrive_upload(fsave.file_dir[i],json_pre_response['uploadUrl'])
                #         if(status_of_upload == 201):
                #             try:
                #                 os.remove(filepath)
                #                 # print("File deleted successfully.")
                #             except OSError as e:
                #                 logging.error(f"Error deleting file: {e}")
                #         time.sleep(0.1)
                #     print("finish")
                # else:
                #     #如果是绝对路径的话，就把该路径的父路径给替换了
                #     filename =filepath.split(father_path)[-1:][0]

                #     #上传OneDrive的步骤
                #     json_pre_response = fsave.Onedrive_pre_upload(filename)
                #     status_of_upload = fsave.Onedrive_upload(filepath,json_pre_response['uploadUrl'])
                #     if(status_of_upload == 201):
                #         try:
                #             os.remove(filepath)
                #             # print("File deleted successfully.")
                #         except OSError as e:
                #             logging.error(f"Error deleting file: {e}")
        else:
            logging.error("f'This path isn't exsit:{filepath}'")
            assert 0
