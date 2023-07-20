#!/usr/bin/python3
# -*- coding: utf-8 -*- 
#考虑到python3默认的编译格式本来就是utf-8,这条多余了`

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

from fsave import fsave as Fsave
from fsave import deeper_dir
import sys #用以获取输入参数
import os
import logging
import configparser    #填写配置文件
import multiprocessing #创建多进程工作，尝试


def onedrive_process(fsave,result_queue_onedrive):

    i = 0
    status_of_upload = ""
    #上传OneDrive的步骤
    while status_of_upload != 201:
        json_pre_response = fsave.Onedrive_pre_upload()
        status_of_upload = fsave.Onedrive_upload()    
        if i > 2:
            break
        i = i + 1
    result_queue_onedrive.put(status_of_upload)
    pass
    

def baidu_process(fsave):
    
    error_num = ""
    i = 0
    # #上传Panbaidu的步骤
    while error_num != 0:
        fsave.Panbaidu_upload()
        error_num = fsave.Panbaidu_createfile()
        if i > 2:
            break
        i = i + 1
    return error_num

    

if __name__ == '__main__':
    
    arguments = sys.argv[1:]
    # print(arguments)
    # arguments = ["喜欢的角色 - 副本"]

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
        logging.info("new missing happen")
        logging.info(f'This path is:{filepath}')
        
        if os.path.exists(filepath):
            #通过读取配置文件来判断是否需要上传文件到百度
        
            config = configparser.ConfigParser()
            config.read("fsave.ini")
            
            #如果是相对路径，先转化为绝对路径
            #如果上传目标是文件夹的话，该步骤可以得到文件夹中每个文件在文件夹中的相对位置。
            filepath = os.path.abspath(filepath)
            father_path = os.path.dirname(filepath)
    
            #进程
            processes = []
            result_queue_ondrive = multiprocessing.Queue()  # 创建一个队列用于存储返回值
            result_queue_panbaidu = multiprocessing.Queue()  # 创建一个队列用于存储返回值

            #如果该文件是路径
            if os.path.isdir(filepath):
                file_dir = []
                deeper_dir('',filepath,file_dir)
                #test
                print(file_dir)
                for i in range(len(file_dir)):
                    #如果上传目标是文件夹的话，该步骤可以得到每个文件在文件夹的相对位置
                    filename = file_dir[i].split(father_path)[-1:][0]
                    #test
                    print(filename)
                    fsave = Fsave(remotefilepath=filename,absfilepath = file_dir[i])
                    if(config.getint('config_oneDrive','isupload')==1):
                        fsave.Onedrive_First_Access_Token()
                        fsave.Onedrive_Refresh_Access_Token()
                    if(config.getint("config_panbaidu","isupload")==1):
                        fsave.Panbaidu_First_Access_Token()
                        fsave.Panbaidu_Refresh_Access_Token()

                    
                    if(config.getint("config_oneDrive","isupload")==1):
                        p = multiprocessing.Process(target=onedrive_process, args=(fsave,result_queue_ondrive))
                        processes.append(p)
                        p.start()
                    value_of_error = ""
                    if(config.getint("config_panbaidu","isupload")==1):
                        value_of_error = baidu_process(fsave)
                    #双进程同时结束
                    for p in processes:
                        p.join()
                    
                    status_of_upload = ""
                    #根据上传的返回值判断是否上传成功
                    if(config.getint("config_oneDrive","isupload")==1):
                        status_of_upload = result_queue_ondrive.get()
                    
                    if((status_of_upload == 201) and (value_of_error == 0)) or \
                        ((status_of_upload == "") and (value_of_error == 0)) or \
                        ((status_of_upload == 201) and (value_of_error == "")):
                        try:
                            os.remove(file_dir[i])
                            logging.info(f"upload complete: {file_dir[i]}")
                        except OSError as e:
                            logging.error(f"Error deleting file: {e}")
                    else:
                        logging.error(f'error uploading file:{filepath}')
                        logging.error(f'the response of OneDrive is:{status_of_upload}')
                        logging.error(f'the response of Panbaidu is:{value_of_error}')

                file_list = os.listdir(filepath)
                if len(file_list) == 0:
                    os.rmdir(filepath)

            else:
                filename =filepath.split(father_path)[-1:][0]

                fsave = Fsave(remotefilepath=filename,absfilepath = filepath)
                if(config.getint('config_oneDrive','isupload')==1):
                    fsave.Onedrive_First_Access_Token()
                    fsave.Onedrive_Refresh_Access_Token()
                if(config.getint("config_panbaidu","isupload")==1):
                    fsave.Panbaidu_First_Access_Token()
                    fsave.Panbaidu_Refresh_Access_Token()

                if(config.getint("config_oneDrive","isupload")==1):
                    p = multiprocessing.Process(target=onedrive_process, args=(fsave,result_queue_ondrive))
                    processes.append(p)
                    p.start()
                value_of_error = ""
                if(config.getint("config_panbaidu","isupload")==1):
                    value_of_error = baidu_process(fsave)
                
                for p in processes:
                    p.join()
                
                status_of_upload = ""
                #根据上传的返回值判断是否上传成功
                if(config.getint("config_oneDrive","isupload")==1):
                    status_of_upload = result_queue_ondrive.get()
                    
                
                if((status_of_upload == 201) and (value_of_error == 0)) or \
                    ((status_of_upload == "") and (value_of_error == 0)) or \
                    ((status_of_upload == 201) and (value_of_error == "")):                    
                    try:
                        os.remove(filepath)
                        logging.info(f"upload complete: {filepath}")
                    except OSError as e:
                        logging.error(f"Error deleting file: {e}")               
                else:
                    logging.error(f'error uploading file:{filepath}')
                    logging.error(f'the response of OneDrive is:{status_of_upload}')
                    logging.error(f'the response of Panbaidu is:{value_of_error}')
        else:
            logging.error(f"This path isn't exsit:{filepath}")
