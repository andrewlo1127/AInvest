from flask import Flask, request, jsonify
import random
import string
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# 生成随机验证码
def generate_secure_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    specific_email = data.get('email')
    verification_code = generate_secure_code()

    # 数据库连接设置
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': '專題'
    }

    try:
        # 连接到数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 查询电子邮件地址
        cursor.execute("SELECT email FROM members WHERE email=%s", (specific_email,))
        bcc_recipients = [row[0] for row in cursor.fetchall()]

        if not bcc_recipients:
            return jsonify({"status": "error", "message": "没有找到该电子邮件地址。"}), 400

        # 插入验证码到 HTML 模板中
        html = f'''
        <h1></h1>
        <div style="color:white">验证码: {verification_code}</div>
        '''

        msg = MIMEMultipart()
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        msg['Subject'] = Header('忘记密码', 'utf-8')
        msg['From'] = formataddr((Header('爱投资', 'utf-8').encode(), 'AInvestor110@gmail.com'))

        # 连接到 Gmail 的 SMTP 服务器
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        try:
            smtp.login('AInvestor110@gmail.com', 'bmuwqhmuxqphdbpo')
            smtp.sendmail('AInvestor110@gmail.com', bcc_recipients, msg.as_string())
            return jsonify({"status": "success", "message": "邮件发送成功！"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"邮件发送失败！{e}"}), 500
        finally:
            smtp.quit()

    except pymysql.MySQLError as err:
        return jsonify({"status": "error", "message": f"数据库连接失败：{err}"}), 500
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
