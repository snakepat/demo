import mysql.connector

# 创建数据库连接
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
query = "SELECT panbaidu_access_token FROM account where username = 'veronica'"
cursor.execute(query)
result = cursor.fetchall()
access_token = result[0][0]
print(result)

# # 修改数据
# update_query = "UPDATE users SET age = 30 WHERE id = 1"
# cursor.execute(update_query)
# conn.commit()

# 关闭游标和连接
cursor.close()
conn.close()