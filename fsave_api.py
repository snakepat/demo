import base64
from flask import Flask, request, jsonify
import logging
import mysql.connector

#可以用来查看该api是否成功运行
#ps -ef | grep python

fsave_test = Flask(__name__)

# 配置日志记录
logging.basicConfig(
    filename='fsave_api.log', 
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

@fsave_test.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, World!"})


@fsave_test.route("/api/get_panbaidu_access_token", methods=["POST"])
def get_panbaidu_access_token():

    # 获取请求头中的身份验证信息
    auth_header = request.headers.get("Authorization")
    # 记录客户id
    client_ip = request.remote_addr
    logging.info(f"API request from IP: {client_ip}")
    # 解析身份验证信息，这里以基本身份验证为例
    if auth_header and auth_header.startswith("Basic"):
        # 提取用户名和密码
        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")

        # logging.info(f'user is {username}')
        # 创造数据库链接

        conn = mysql.connector.connect(
        host="127.0.0.1",
        port= 3306,#默认的接口，但也不全是
        user="root",
        password="your_password",
        database="mysql"
        )
        
        # 创建游标对象
        cursor = conn.cursor()

        # table = "fave_db"
        # 查询数据
        cursor.execute("use fsave_db")

        # 进行相应的身份验证逻辑
        # ...
        query = "SELECT password FROM account where username = '{user}'".format(user = username)
        cursor.execute(query)
        result = cursor.fetchall()
        db_pw = result[0][0]

        if db_pw != password:
            # logging.error(f"the password or the username is error")  
            return jsonify({"message": "Authentication failed, the password or the username is error"}), 401
        else: 
            #传递参数
            query = "SELECT panbaidu_access_token FROM account where username = '{user}'".format(user = username)
            cursor.execute(query)
            result = cursor.fetchall()
            access_token = result[0][0]
            query = "SELECT panbaidu_refresh_token FROM account where username = '{user}'".format(user = username)
            cursor.execute(query)
            result = cursor.fetchall()
            refresh_token = result[0][0]

            # 返回响应
            return jsonify({
                "message": "Authenticated successfully.",
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
    else:
        # 身份验证失败，返回错误响应
        return jsonify({"message": "Authentication failed."}), 401


@fsave_test.route("/api/change_panbaidu_access_token", methods=["POST"])
def change_panbaidu_access_token():
     # 获取请求头中的身份验证信息
    auth_header = request.headers.get("Authorization")
    # 记录客户id
    client_ip = request.remote_addr
    logging.info(f"API request from IP: {client_ip}")
    # 解析身份验证信息，这里以基本身份验证为例
    if auth_header and auth_header.startswith("Basic"):
        # 提取用户名和密码
        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":")

        # 获取 POST 数据
        data = request.json

        # 获取 "panbaidu_access_token" 参数
        panbaidu_access_token = data.get("panbaidu_access_token")
        panbaidu_refresh_token = data.get("panbaidu_refresh_token")

        # 创造数据库链接
        conn = mysql.connector.connect(
        host="127.0.0.1",
        port= 3306,
        user="root",
        password="159852145lcgj",
        database="mysql"
        )
        
        # 创建游标对象
        cursor = conn.cursor()

        # table = "fave_db"
        # 查询数据
        cursor.execute("use fsave_db")

        # 进行相应的身份验证逻辑
        # ...
        query = "SELECT password FROM account where username = '{user}'".format(user = username)
        cursor.execute(query)
        result = cursor.fetchall()
        db_pw = result[0][0]
        #test
        logging.info(f"{panbaidu_access_token}")
        logging.info(f"{panbaidu_refresh_token}")
        if db_pw != password:
            # logging.error(f"the password or the username is error")  
            return jsonify({"message": "Authentication failed, the password or the username is error"}), 401
        else: 
            #传递参数
            query = f"UPDATE account SET panbaidu_access_token = '{panbaidu_access_token}' where username = '{username}'"
            cursor.execute(query)
            conn.commit()
            # updated_rows = cursor.rowcount
            # if updated_rows > 0:
            #     logging.info(f"panbaidu_access_token update successful")
            # else:
            #     logging.error("panbaidu_access_token update fail")

            query = f"UPDATE account SET panbaidu_refresh_token = '{panbaidu_refresh_token}' where username = '{username}'"
            cursor.execute(query)
            conn.commit()
            result = cursor.fetchall()
            logging.info(f"{result}")
            # updated_rows = cursor.rowcount
            # if updated_rows > 0:
            #     logging.info(f"panbaidu_refresh_token update successful")
            # else:
            #     logging.error("panbaidu_refresh_token update fail")

            # 返回响应
            return jsonify({
                "message": "token update successfully.",
            }), 200
        
            cursor.close()
            conn.close()

    else:
        # 身份验证失败，返回错误响应
        return jsonify({"message": "Authentication failed."}), 401

if __name__ == "__main__":
    fsave_test.run(host='0.0.0.0', port=1314)

