import pymysql

# 数据库连接设置
db_config = {
    'host': '127.0.0.1',  # 或者 'localhost'
    'user': 'root',
    'password': '',
    'database': '專題'
}

try:
    # 连接到数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    
    # 查询电子邮件地址
    cursor.execute("SELECT email FROM members WHERE m_id = 3")
    bcc_recipients = [row[0] for row in cursor.fetchall()]
    
    print("收件人：", bcc_recipients)
    
except pymysql.MySQLError as err:
    print("数据库错误：", err)
finally:
    # 关闭数据库连接
    if 'conn' in locals() and conn.open:
        cursor.close()
        conn.close()


import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

html = '''
<h1>hello</h1>
<div>這是 HTML 的內容</div>
<div style="color:red">紅色的字</div>
<p><a href="https://www.ncnu.edu.tw/">ncnu</a></p>
'''

msg = MIMEMultipart()                         # 使用多種格式所組成的內容
msg.attach(MIMEText(html, 'html', 'utf-8'))   # 加入 HTML 內容
# 使用 python 內建的 open 方法開啟指定目錄下的檔案
with open(r"C:\Users\z0901\OneDrive\桌面\175925.jpg", 'rb') as file:
    img = file.read()
attach_file = MIMEApplication(img, Name='175925.jpg')    # 設定附加檔案圖片
msg.attach(attach_file)                       # 加入附加檔案圖片

# 创建邮件内容
#msg = MIMEText('早安', 'plain', 'utf-8')
msg['Subject'] = Header('test測試', 'utf-8')
msg['From'] = formataddr((Header('愛投資', 'utf-8').encode(), 'AInvestor110@gmail.com'))


# 连接到 Gmail 的 SMTP 服务器
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()

try:
    smtp.login('AInvestor110@gmail.com', 'bmuwqhmuxqphdbpo')
    smtp.sendmail('AInvestor110@gmail.com', bcc_recipients, msg.as_string())
    print('邮件传送成功！')
except Exception as e:
    print('邮件传送失败！', e)
finally:
    smtp.quit()
