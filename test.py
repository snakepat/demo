#!/usr/bin/python3
# -*- coding: utf-8 -*- #考虑到python3默认的编译格式本来就是utf-8,这条多余了

#该程序比较适用于移动本程序所在文件目录的文件，
#因为会把该文件的绝对路径的上层路径删除来提取类似与相对路径的内容
#可以做一个调整，自动添加上层路径方便删除

import json
import requests
import base64

url_1 = "http://23.234.200.170:1314/api/get_panbaidu_access_token"  # 根据实际的 API 地址进行替换
url_2 = "http://23.234.200.170:1314/api/change_panbaidu_access_token"
# fsave.lipj7.top
# 23.234.200.170:1314
# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("Error:", response.status_code)


# 设置用户名和密码
username = "test"
password = "0315lcgj"
access_token = "121.214ec7e3ddb0e65d5ab2d90079b4eb4a.Ya4j0S0Vh4MhWoVOmgSR77NYUonnHjLsNPtKNT5.jlya1w"
refresh_token = "122.f9636777daeabb3248abf1f900cc3283.YBuls7airk2MFuLWL2z9Yw_1ERNnRbS76x_TaaS.-9x6IA"

# 创建一个请求头，将用户名和密码进行 Base64 编码
auth_header = "Basic " + base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

# 发送 API 请求，并在请求头中包含身份验证信息
headers = {
    "Authorization": auth_header,
    "Content-Type": "application/json"
    }

data = {
    'panbaidu_access_token':  access_token,
    'panbaidu_refresh_token':  refresh_token
}

response_1 = requests.post(url_2, headers=headers,data=json.dumps(data))
res_json_1 = json.loads(response_1.content)

headers = {
    "Authorization": auth_header
    }
response = requests.post(url_1, headers=headers)
res_json = json.loads(response.content)

print(res_json)
print(res_json["access_token"])