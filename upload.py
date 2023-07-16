#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

from fsave import fsave as Fsave
import sys #用以获取输入参数
import os
import logging
import configparser    #填写配置文件
import multiprocessing #创建多进程工作，尝试



def onedrive_process(fsave,filename,filepath,result_queue_onedrive):

    i = 0
    status_of_upload = ""
    #上传OneDrive的步骤
    while (status_of_upload != 201) and (i <= 2):
        json_pre_response = fsave.Onedrive_pre_upload(filename)
        status_of_upload = fsave.Onedrive_upload(filepath,json_pre_response['uploadUrl'])    
        i = i + 1
    result_queue_onedrive.put(status_of_upload)
    

def baidu_process(fsave,filename,filepath,result_queue_panbaidu):
    
    error_num = ""
    i = 0
    #上传Panbaidu的步骤
    while (error_num != 0) and (i <= 2):
        if os.path.getsize(filepath) > fsave.panbaidu_chunk_size:
            slice_filepath_list = fsave.Split_file(filepath,fsave.panbaidu_chunk_size)
        else:
            slice_filepath_list = []
            slice_filepath_list.append(filepath)
        
        # father_path = os.path.dirname(os.path.abspath(__file__))
        # filename = os.path.basename(filepath)

        # print(slice_filepath_list)
        md5_list = []
        for filepath in slice_filepath_list:
            value_md5 = fsave.get_md5(filepath)
            md5_list.append(value_md5)
        
        # print(md5_list)

        size = os.path.getsize(filepath)
        json_pre_response = fsave.Panbaidu_pre_upload(filename, size , md5_list)
        # print(json_pre_response)

        fsave.Panbaidu_upload(filename,slice_filepath_list,json_pre_response['uploadid'])
        error_num = fsave.Panbaidu_createfile(filename,size,md5_list,json_pre_response['uploadid'])
        
        i = i + 1
    # return error_num
    result_queue_panbaidu.put(error_num)
    

if __name__ == '__main__':
    fsave = Fsave()
    arguments = sys.argv[1:]
    # print(arguments)
    # arguments = ["[Ioroid] The IDOLM@STER Cinderella Girls U149 - 01 [AMZN WEB-DL 1080p AVC E-AC3] - 副本.mkv"]

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
            #更新access_token
            if(config.getint('config_oneDrive','isupload')==1):
                fsave.Onedrive_First_Access_Token()
                fsave.Onedrive_Refresh_Access_Token()
            if(config.getint("config_panbaidu","isupload")==1):
                fsave.Panbaidu_First_Access_Token()
                fsave.Panbaidu_Refresh_Access_Token()
            
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
                fsave.deeper_dir('',filepath,file_dir)
                #test
                print(file_dir)
                for i in range(len(file_dir)):
                    #如果上传目标是文件夹的话，该步骤可以得到每个文件在
                    filename = file_dir[i].split(father_path)[-1:][0]
                    #test
                    print(filename)
                    if(config.getint("config_panbaidu","isupload")==1):
                        p = multiprocessing.Process(target=baidu_process, args=(fsave,filename,file_dir[i],result_queue_panbaidu))
                        processes.append(p)
                        p.start()
                    if(config.getint("config_oneDrive","isupload")==1):
                        p = multiprocessing.Process(target=onedrive_process, args=(fsave,filename,file_dir[i],result_queue_ondrive))
                        processes.append(p)
                        p.start()
                    #双进程同时结束
                    for p in processes:
                        p.join()
                    
                    status_of_upload = ""
                    value_of_error = ""
                    #根据上传的返回值判断是否上传成功
                    if(config.getint("config_oneDrive","isupload")==1):
                        status_of_upload = result_queue_ondrive.get()
                    if(config.getint("config_panbaidu","isupload")==1):
                        value_of_error = result_queue_panbaidu.get()
                    
                    #删除分片文件
                    if (value_of_error == 0):
                        if(os.path.getsize(file_dir[i]) > fsave.panbaidu_chunk_size):
                            fsave.del_slice_file(file_dir[i])
                    
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
                if(config.getint("config_panbaidu","isupload")==1):
                        p = multiprocessing.Process(target=baidu_process, args=(fsave,filename,filepath,result_queue_panbaidu))
                        processes.append(p)
                        p.start()
                if(config.getint("config_oneDrive","isupload")==1):
                    p = multiprocessing.Process(target=onedrive_process, args=(fsave,filename,filepath,result_queue_ondrive))
                    processes.append(p)
                    p.start()
                
                for p in processes:
                    p.join()
                
                status_of_upload = ""
                value_of_error = ""
                #根据上传的返回值判断是否上传成功
                if(config.getint("config_oneDrive","isupload")==1):
                    status_of_upload = result_queue_ondrive.get()
                if(config.getint("config_panbaidu","isupload")==1):
                    value_of_error = result_queue_panbaidu.get()
                    
                

                #删除分片文件
                if (value_of_error == 0):
                    fsave.del_slice_file(filepath)
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
