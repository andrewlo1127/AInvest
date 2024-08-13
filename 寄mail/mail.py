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

# 生成隨機驗證碼
def generate_secure_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 数据库连接设置
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': '專題'
}

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'success': False, 'message': '沒有提供 email 地址'})
    
    try:
        # 连接到数据库
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # 查询数据库中是否存在该 email
        cursor.execute("SELECT email FROM members WHERE email = %s", (email,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'success': False, 'message': '此 email 尚未註冊'})

        # 如果 email 存在，则生成验证码
        verification_code = generate_secure_code()
        cursor.execute("UPDATE members SET verification_code = %s WHERE email = %s", (verification_code, email))
        conn.commit()

    except pymysql.MySQLError as err:
        return jsonify({'success': False, 'message': '資料庫連接失敗'})
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

    # 插入驗證碼到 HTML 模板中
    html = f'''
    <h1></h1>
    <div style="color:red">驗證碼: {verification_code}</div>
    '''

    msg = MIMEMultipart()
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    msg['Subject'] = Header('忘記密碼', 'utf-8')
    msg['From'] = formataddr((Header('愛投資', 'utf-8').encode(), 'AInvestor110@gmail.com'))

    # 连接到 Gmail 的 SMTP 服务器
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()

    try:
        smtp.login('AInvestor110@gmail.com', 'bmuwqhmuxqphdbpo')
        smtp.sendmail('AInvestor110@gmail.com', [email], msg.as_string())
        return jsonify({'success': True, 'message': '郵件傳送成功！'})
    except Exception as e:
        return jsonify({'success': False, 'message': '郵件傳送失敗！', 'error': str(e)})
    finally:
        smtp.quit()

if __name__ == '__main__':
    app.run(debug=True)
