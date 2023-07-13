#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了
import requests
import os
import platform #用以判断当前系统是什么系统
import math 
import hashlib
import configparser    #填写配置文件
import datetime         #时间计算问题
import time

# from requests_toolbelt import MultipartEncoder 

from urllib.parse import urlencode
import json

if(platform.system()=='Windows'):
    path_separator = "\\"    
elif(platform.system()=='Linux'):
    path_separator = "/"
else:
    assert 0, '该系统目前只能在linux和windows下执行'

#分片大小
panbaidu_chunk_size = 1024*1024*4
Onedrive_chunk_size = 1024*1024*25 #320*1024的80倍25Mib,越大上传越快

file_dir = []#用来存贮这一次启用程序便利文件后得到的文件
# access_token获取地址
pan_access_token_api = 'https://openapi.baidu.com/oauth/2.0/token?'
# 预创建文件接口
pan_precreate_api = 'https://pan.baidu.com/rest/2.0/xpan/file?'
# 分片上传api
pan_upload_api = 'https://d.pcs.baidu.com/rest/2.0/pcs/superfile2?'
# 创建文件api
pan_create_api = 'https://pan.baidu.com/rest/2.0/xpan/file?'

###############################################################
##OneDrive相关api
#access_token获取地址
Onedrive_authorize_api = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?'

Onedrive_access_token_api = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

Onedrive_refresh_token_api = 'https://login.live.com/oauth20_token.srf'

Oofbusiness_refresh_token_api = 'https://login.microsoftonline.com/common/oauth2/token'
#通过 Microsoft Graph API 获取 OneDrive for Business 终结点 URL的api,现在只能用graph，原有的api可能被抛弃了
# Onedrive_serviceResourceId_api = 'https://api.office.com/discovery/v2.0/me/services'
Onedrive_serviceResourceId_api = 'https://graph.microsoft.com/v1.0/me/drive'

#上传该目录文件下的所有文件到百度网盘/考虑以后还有上传的Onedrive的选项
def Panbaidu_file_upload():
    Panbaidu_First_Access_Token()
    Panbaidu_Refresh_Access_Token()    
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
    teststring = "D:\\git\\code\\test\\test\\头像与背景\\头像与背景.zip"
    # teststring = "E:\\code\\git\\demo\\test\\头像与背景\\头像与背景.zip"
    # teststring = "E:\\code\\git\\demo\\test\\头像与背景\\FZU0h2laMAIzzF5.jpg"
    # teststring = "/root/temp/2023.tar"
    
    #根据目标文件的大小选择是否分片
    if os.path.getsize(teststring) > panbaidu_chunk_size:
        slice_filepath_list = Split_file(teststring,panbaidu_chunk_size)
    else:
        slice_filepath_list = []
        slice_filepath_list.append(teststring)

    father_path = os.path.dirname(os.path.abspath(__file__))
    filename = teststring.split(father_path)[-1:][0]

    # print(slice_filepath_list)
    md5_list = []
    for filepath in slice_filepath_list:
        value_md5 = get_md5(filepath)
        md5_list.append(value_md5)
        
    # print(md5_list)

    size = os.path.getsize(teststring)
    json_pre_response = Panbaidu_pre_upload(filename, size , md5_list)
    print(json_pre_response)

    Panbaidu_upload(filename,slice_filepath_list,json_pre_response['uploadid'])
    Panbaidu_createfile(filename,size,md5_list,json_pre_response['uploadid'])


    return

#第一次获得access—token的内容并保存到本地文件夹的fsave.ini文件中
def Panbaidu_First_Access_Token():

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'wb') as o:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"))
        config.write(o)

        client_id = config.get("config_panbaidu","client_id")
        client_secret = config.get("config_panbaidu","client_secret")

        params_code = {
            'response_type': 'code',
            'client_id':  client_id,
            # 'client_secret':  client_secret,
            'redirect_uri': 'oob',
            'scope': 'basic,netdisk',
            'device_id': '34097783'
        }

        code_url = pan_access_token_api + urlencode(params_code)

        if(config.getint("config_panbaidu","isfirsttime")):
            print("请浏览出现的网址，完成百度网盘的授权，并将获得的code值输入:\n")
            print(code_url,"\n")
            code = input("请输入你得到的code值\n")

            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'client_id':  client_id,
                'client_secret':  client_secret,
                'redirect_uri': 'oob'
            }  

            url = pan_access_token_api + urlencode(params)
            
            payload = {}
            headers = {
            'User-Agent': 'pan.baidu.com'
            }
            response = requests.request("GET", url, headers=headers, data = payload,timeout=(10,30))
            # print(response.text.encode('utf8'))
            # time.sleep(1)
            json_resp = json.loads(response.content)
            # print(json_resp)

            nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            config.set("config_panbaidu","access_token",json_resp['access_token'])
            config.set("config_panbaidu","refresh_token",json_resp['refresh_token'])
            config.set("config_panbaidu","lastkeytime",nowtime)
            config.set("config_panbaidu","isfirsttime","0")

        time_str = config.get("config_panbaidu","lastkeytime")
        client_id = config.get("config_panbaidu","client_id")
        client_secret = config.get("config_panbaidu","client_secret")

        lastkeytime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        nowkeytime = datetime.datetime.now()
        days_after_30 = lastkeytime + datetime.timedelta(days=30)
        if ((days_after_30)<nowkeytime):
            print("距离上次授权已经超过太长时间，需要重新授权。请浏览出现的网址，并将获得的code值输入:\n")
            print(code_url,"\n")
            code = input("请输入你得到的code值\n")
            
            params = {
                        'grant_type': 'authorization_code',
                        'code': code,
                        'client_id':  client_id,
                        'client_secret':  client_secret,
                        'redirect_uri': 'oob'
                    }  

            url = pan_access_token_api + urlencode(params)
            payload = {}
            headers = {
            'User-Agent': 'pan.baidu.com'
            }

            response = requests.request("GET", url, headers=headers, data = payload,timeout=(10,30))
            json_resp = json.loads(response.content)
            # print(json_resp)

            config.set("config_panbaidu","access_token",json_resp['access_token'])
            config.set("config_panbaidu","refresh_token",json_resp['refresh_token'])
            config.set("config_panbaidu","lastkeytime",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    return

#获得Access Token更新并保存到本地文件夹的fsave.ini文件中
def Panbaidu_Refresh_Access_Token():
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    refresh_token = config.get("config_panbaidu","refresh_token")
    client_id = config.get("config_panbaidu","client_id")
    client_secret = config.get("config_panbaidu","client_secret")

    payload = {}
    headers = {
    'User-Agent': 'pan.baidu.com'
    }
    params = {
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id':  client_id,
                    'client_secret':  client_secret,
                }  

    url = pan_access_token_api + urlencode(params)

    response = requests.request("GET", url, headers=headers, data = payload,timeout=(10,30))
    json_resp = json.loads(response.content)

    config.set("config_panbaidu","access_token",json_resp['access_token'])
    config.set("config_panbaidu","refresh_token",json_resp['refresh_token'])
    config.set("config_panbaidu","lastkeytime",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
    config.write(o)
    o.close()
    return

#遍历当前文件列表并存贮相关信息
#   find_cur(string, path)实现对path目录下文件的查找，列出文件命中含string的文件
#   输出相对路径
def find_cur(string, pathcurrent):
    # 遍历当前文件，找出符合要求的文件，将路径添加到l中
    for x in os.listdir(pathcurrent):
        pathson = os.path.join(pathcurrent,x)
        if os.path.isfile(pathson):
            if string in x :
                file_dir.append(pathson)

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
    # else:
        # print( "%s isn't in the file_dir",string)
        # assert 0
    return


#排除file_dir中本程序所用脚本或文件
def del_default_file():
    pathcurrent = os.path.dirname(os.path.abspath(__file__))
    del_file(os.path.join(pathcurrent,"fsave.py"))
    del_file(os.path.join(pathcurrent,"README.md"))
    del_file(os.path.join(pathcurrent,"fsave.ini"))
    return

#文件加密处理，可选服务，针对百度网盘的和谐功能
def Encrypt_Compression():


    return

#功能：    文件分片,分片为固定大小
#输入：    需要被分片的文件路径
#返回：    被分片的子文件路径
#补充说明：需要修改部分参数——被分片的大小
def Split_file(file_path,chunk_size):
    current_path = os.path.dirname(file_path)
    # filename = file_path.split(path_separator)[-1:][0]
    filename = file_path.split("/")[-1:][0]
    total_size = os.path.getsize(file_path)
    current_chunk = 0
    #根据目标大小获得分片数目
    total_chunk = math.ceil(total_size/chunk_size)
    #用来存贮分片文件路径
    slice_filepath_list = []
    #循环分解出每一个分片
    while current_chunk < total_chunk:
        start = current_chunk*chunk_size
        end = min(total_size, start+chunk_size)
        with open(file_path, 'rb') as f1:
            f1.seek(start)
            file_chunk_data = f1.read(end-start)
            #分片文件命名规则
            slice_filename = "{fname}_{i}".format(fname = filename, i = current_chunk)
            slice_filepath = os.path.join(current_path,slice_filename)
            #新建分片文件
            f2 = open(slice_filepath,"wb")
            f2.write(file_chunk_data)      
            f2.close()
            f1.close()
            slice_filepath_list.append(slice_filepath)
        current_chunk = current_chunk + 1
    
    #运行结束后删除源文件/需谨慎，确认无误再删除
    

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
#输入：1.目标文件在系统中的目录，2.分片前的目标文件的大小 3.按顺序排列的分片文件的md5列表
#输出：返回相应
#access_token的获取方式需要修改
#注意python列表作为json形式的值的时候需要用json.dumps()函数
#或者 使用'[""]'的形式，注意这是python里少数需要注意单双引号区别的情况
def Panbaidu_pre_upload(path, size, md5_list):
    
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    
    default_path = "/apps/fsave"#百度开发平台要求的格式
    path_tmp = path.replace('\\','/')
    current_path = default_path + path_tmp
    print(current_path)

    access_token = config.get("config_panbaidu","access_token")

    params = {
                    'method': 'precreate',
                    'access_token': access_token,
                }  

    url = pan_precreate_api + urlencode(params)
    
    md5_list = json.dumps(md5_list)
    payload = {'path': current_path,
    'size': size,
    # 'rtype': '2',
    'isdir': '0',
    'autoinit': '1',
    'block_list': md5_list}

    response = requests.request("POST", url, data=payload,timeout=(10,30))
    json_resp = json.loads(response.content)

    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
    config.write(o)
    o.close()
    
    if not int(json_resp['errno']):
        return json_resp
    else:
        print(json_resp)
        assert 0, '预上传失败，请检查失败原因'
        
#输入：目标文件在系统中的相对路径、分片后分片文件路径列表、预上传得到的uploadid
#无输出
def Panbaidu_upload(filename,path_list,uploadid):
    
    config = configparser.ConfigParser()
    config.read('fsave.ini')


    access_token = config.get("config_panbaidu","access_token")

    default_path = "/apps/fsave"#百度开发平台要求的格式
    path_tmp = filename.replace('\\','/')
    current_path = default_path + path_tmp#在百度文件中的存储模式
    
    for i in range(len(path_list)):

        params = {
                        'method': 'upload',
                        'access_token': access_token,
                        'uploadid': uploadid,
                        'type': 'tmpfile',
                        'partseq': i,
                        'path': current_path
                    }  

        url = pan_upload_api + urlencode(params)
        
        payload = {}
        headers = {}
        files = [
        ('file', open(path_list[i],'rb'))
        ]
        response = requests.request("POST",url=url, headers=headers, data = payload, files = files,timeout=(10,30))
        json_resp = json.loads(response.content)
    
    return 
        
#输入：1.目标文件在系统中的相对路径，2.分片前的目标文件的大小 3.按顺序排列的分片文件的md5列表，预上传得到的uploadid
#输出：响应结果
def Panbaidu_createfile(filename,size,md5_list,uploadid):
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    access_token = config.get("config_panbaidu","access_token")

    #url
    params = {
        'method': 'create',
        'access_token': access_token,
    }  
    url = pan_create_api + urlencode(params)

    #date要求的基本内容
    md5_list = json.dumps(md5_list)#
    default_path = "/apps/fsave"#百度开发平台要求的格式
    path_tmp = filename.replace('\\','/')
    current_path = default_path + path_tmp#在百度文件中的存储模式

    payload = {
        'path': current_path,
        'size': size,
        'rtype': '1',
        'isdir': '0',
        'uploadid': uploadid,
        'block_list': md5_list
        }
    headers = {}
    files = []
    response = requests.request("POST",url=url, headers=headers, data = payload, files = files,timeout=(10,30))
    json_resp = json.loads(response.content)

    print(json_resp)

    return
    

def Onedrive_file_upload():

    Onedrive_First_Access_Token()
    Onedrive_Refresh_Access_Token()

    #迭代获取所有子文件并把它们的路径保存到file_dir = []中
    deeper_dir()
    # #排除本程序所用脚本文本
    del_default_file()
    # # print("%s\n",file_dir)
    father_path = os.path.dirname(os.path.abspath(__file__))
    
    for i in range(len(file_dir)):
    
        filename = file_dir[i].split(father_path)[-1:][0]
        json_pre_response = Onedrive_pre_upload(filename)
        Onedrive_upload(file_dir[i],json_pre_response['uploadUrl'])
        time.sleep(0.2)
    # print(json_upload_response)
    print("finish")
    return


# 创建上传会话
def Onedrive_pre_upload(path):
    
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    
    default_path = "/fsave"#百度开发平台要求的格式,也是本软件的命名方式
    path = path.replace('\\','/')#针对windows系统使用的功能
    current_path = default_path + path

    access_token = config.get("config_oneDrive","access_token")

    response = requests.post(
        f'https://graph.microsoft.com/v1.0/me/drive/root:{current_path}:/createUploadSession',
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'item': {
                #是指如果存在同名文件则为新上传的文件重命名
                '@microsoft.graph.conflictBehavior': 'rename',
            },
        }),

    )

    json_resp = json.loads(response.content)
    #testing
    # print(json_resp)
    return json_resp

#上传文件
#输入：文件的本地目录，上传会话的uploadurl
#输出：返回响应，用来判断访问情况
#功能，对大于5Mib的文件进行分片，然后
def Onedrive_upload(file,uploadurl):
    json_resp_list = []
    fsize = os.path.getsize(file)
    
    current_chunk = 1
    total_chunk = math.ceil(fsize/Onedrive_chunk_size)

    if fsize >= Onedrive_chunk_size:
        while current_chunk <= total_chunk:
            start = (current_chunk - 1)*Onedrive_chunk_size
            end = min(fsize, start+Onedrive_chunk_size)
            with open(file, 'rb') as f:
                f.seek(start)
                file_chunk_data = f.read(end-start)
                response = requests.put(
                    uploadurl,
                    data=file_chunk_data,
                    headers={
                        'Content-Length': f'{Onedrive_chunk_size}',
                        'Content-Range': f'bytes {start}-{end-1}/{fsize}'
                        },
                    # timeout=(10,30)
                )
                if response.status_code == 202:
                    print("error accur: OneDrive分片上传错误")
                    break
                
            json_resp = json.loads(response.content)
            json_resp_list.append(json_resp)
            current_chunk = current_chunk + 1
            #test
            # print(json_resp)
            # print("\n")
    else:
        response = requests.put(
                    uploadurl,
                    data=open(file,'rb').read(),
                    headers={
                        'Content-Length': f'{fsize}',
                        'Content-Range': f'bytes 0-{fsize - 1}/{fsize}'
                        },
                    # timeout=(10,30)
                )
        json_resp = json.loads(response.content)
        json_resp_list.append(json_resp)    

    # print(json_resp_list)
    return json_resp_list

#第一次获得access—token的内容并保存到本地文件夹的fsave.ini文件中
def Onedrive_First_Access_Token():
    

    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"))
    
    client_id = config.get("config_oneDrive","client_id")
    client_secret = config.get("config_oneDrive","client_secret")

    params_code = {
    'response_type': 'code',
    'client_id':  client_id,
    'client_secret':  client_secret,
    'redirect_uri': 'http://localhost/',
    'scope': 'files.readwrite.all offline_access'
    }

    code_url = Onedrive_authorize_api + urlencode(params_code)

    if(config.getint("config_oneDrive","isfirsttime")):
        print("请浏览出现的网址，完成OneDrive的授权，并将获得的code值输入:\n")
        
        print(code_url)

        code = input("请输入你得到的code值\n")
        
        url = Onedrive_access_token_api
        response = requests.post(
            url,
            headers={},
            data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id':  client_id,
            'client_secret':  client_secret,
            'redirect_uri': 'http://localhost/' 
            },
            timeout=(10,30)
        )

        # response = requests.request("post", url=url, headers=headers, data = payload,timeout=(10,30))
        # print(response.text.encode('utf8'))
        # time.sleep(1)
        json_resp = json.loads(response.content)
        # print(json_resp)

        config.set("config_oneDrive","access_token",json_resp['access_token'])
        config.set("config_oneDrive","refresh_token",json_resp['refresh_token'])
        config.set("config_oneDrive","lastkeytime",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        config.set("config_oneDrive","isfirsttime","0")
        config.set("config_oneDrive","expires_in",str(json_resp['expires_in']))
        
        o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
        config.write(o)
        o.close()

            #获得Onedrive of business的资源url并保存
        Onedrive_serviceResourceId_access_token()

        return json_resp
        
    time_str = config.get("config_oneDrive","lastkeytime")
    # expires_in = config.getint("config_oneDrive","expires_in")
    lastkeytime = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    nowkeytime = datetime.datetime.now()
    time_after_lastkeytime = lastkeytime + datetime.timedelta(days=60)
    if ((time_after_lastkeytime)<nowkeytime):
        print("距离上次授权已经超过太长时间，需要重新授权。请浏览出现的网址，并将获得的code值输入:")
        print(code_url)
        code = input("请输入你得到的code值(注意code值从地址栏中获得)\n")

        url = Onedrive_access_token_api 
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id':  client_id,
            'client_secret':  client_secret,
            'redirect_uri': 'http://localhost/'
        }
        headers = {}

        response = requests.request("post", url = url, headers=headers, data = payload,timeout=(10,30))
        # if response.status_code == 200:#检查响应状态
        json_resp = json.loads(response.content)
        # test
        # print(json_resp)

        config.set("config_oneDrive","access_token",json_resp['access_token'])
        config.set("config_oneDrive","refresh_token",json_resp['refresh_token'])
        config.set("config_oneDrive","lastkeytime",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        config.set("config_oneDrive","expires_in",str(json_resp['expires_in']))
    
        o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
        config.write(o)
        o.close()

    return 

#发现 OneDrive for Business 资源 URI
def Onedrive_serviceResourceId_access_token():
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    # refresh_token = json_param["refresh_token"]
    access_token = config.get("config_oneDrive","access_token")
    
    payload = {}

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json'
    }

    url = Onedrive_serviceResourceId_api

    response = requests.get(url, data=payload, headers=headers,timeout=(10,30))
    json_resp = json.loads(response.content)
    
    # test
    # print(json_resp)

    webUrl = json_resp['webUrl']
    path_useless = "personal/learning_dreamingday_onmicrosoft_com/Documents"
    resource_id = webUrl.split(path_useless)[0]
    
    config.set("config_oneDrive","resource_id",resource_id)
    config.set('config_oneDrive','driveType',json_resp['driveType'])

    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
    config.write(o)
    o.close()
    return resource_id

#可以进行修改，错误理解expires_in的意思了,expires_in的意思是该时间内令牌是有效的，超过就要用refresh_token
#有没有只有超过expires_in时间才能更新
#刷新获得的Access Token更新并保存到本地文件夹的fsave.ini文件中
def Onedrive_Refresh_Access_Token():
    config = configparser.ConfigParser()
    config.read('fsave.ini')
    # refresh_token = json_param["refresh_token"]
    refresh_token = config.get("config_oneDrive","refresh_token")
    client_id = config.get("config_oneDrive","client_id")
    client_secret = config.get("config_oneDrive","client_secret")
    driveType = config.get("config_oneDrive","driveType")
    resource_id = config.get("config_oneDrive","resource_id")

    if driveType == "business":
        response = requests.post(
            url = Oofbusiness_refresh_token_api,
            data = {
                'grant_type': 'refresh_token',
                'client_id':  client_id,
                'client_secret':  client_secret,
                'refresh_token': refresh_token,
                'redirect_uri': 'http://localhost/',
                'resource_id': resource_id,
                'scope': 'files.readwrite.all offline_access'
            },
            headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }
        )
    else:
                response = requests.post(
            url = Onedrive_refresh_token_api,
            data = {
                'grant_type': 'refresh_token',
                'client_id':  client_id,
                'client_secret':  client_secret,
                'refresh_token': refresh_token,
                'redirect_uri': 'http://localhost/',
                'scope': 'files.readwrite.all offline_access'
            },
            headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }
        )

    json_resp = json.loads(response.content)
    # print(json_resp)
    
    config.set("config_oneDrive","access_token",json_resp['access_token'])
    config.set("config_oneDrive","refresh_token",json_resp['refresh_token'])
    config.set("config_oneDrive","expires_in",str(json_resp['expires_in']))
    config.set("config_oneDrive","lastkeytime",datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    o = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"fsave.ini"), 'w')
    config.write(o)
    o.close()
    return

    # def Onedrive_upload_one_file():
        

    #     return

if __name__ == '__main__':
    # Panbaidu_file_upload()

    Onedrive_file_upload()
    # Onedrive_Refresh_Access_Token()




#部分内容学习参考自如下网站:
# https://www.cnblogs.com/zhuosanxun/p/15100588.html
# https://blog.csdn.net/moshlwx/article/details/52694397
# https://blog.csdn.net/a2824256/article/details/119887954
# https://blog.csdn.net/weixin_44495599/article/details/129766396?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-2-129766396-blog-119505202.235%5Ev36%5Epc_relevant_default_base3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EYuanLiJiHua%7EPosition-2-129766396-blog-119505202.235%5Ev36%5Epc_relevant_default_base3&utm_relevant_index=3
# https://blog.csdn.net/MoLeft/article/details/130613761