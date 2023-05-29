#!/usr/bin/python3
# Write Python 3 code in this online editor and run it.
import requests
import os

#print("hello, word");

#上传该目录文件下的所有文件到百度网盘/考虑以后还有上传的Onedrive的选项
def panbaidu_upload():
    

    return

#第一次获得access—token的内容并保存到本地文件夹的vps_save.scn文件中
def get_First_Access_Token():


    return

#获得Access Token更新并保存到本地文件夹的vps_save.scn文件中
def refresh_Access_Token():


    return

#遍历当前文件列表并存贮相关信息
def find_dir():


    return

#文件加密处理，可选服务，针对百度网盘的和谐功能
def encrypt_Compression():


    return

#预上传


def pre_upload():
    


    return


url = "http://pan.baidu.com/rest/2.0/xpan/file?method=precreate&access_token=12.a6b7dbd428f731035f771b8d15063f61.86400.1292922000-2346678-124328"

payload = {'path': '/apps/test/test.jpg',
'size': '91037',
'rtype': '1',
'isdir': '0',
'autoinit': '1',
'block_list': '["e08b8e863d2fffce685530608305598c"]'}
files = [

]

headers = {
  'Cookie': 'BAIDUID=56BE0870011A115CFA43E19EA4CE92C2:FG=1; BIDUPSID=56BE0870011A115CFA43E19EA4CE92C2; PSTM=1535714267'
}

response = requests.request("POST", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))