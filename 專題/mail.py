import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
import random
import string

# 生成隨機驗證碼
def generate_secure_code(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def send_verifacation_email(input_email,verification_code):
        html = f'''
        <h1></h1>
        <div style="color:red">驗證碼: {verification_code}</div>
        '''

        # 準備郵件內容
        msg = MIMEMultipart()                         # 使用多種格式所組成的內容
        msg.attach(MIMEText(html, 'html', 'utf-8'))   # 加入 HTML 內容

        msg['Subject'] = Header('忘記密碼', 'utf-8')
        msg['From'] = formataddr((Header('愛投資', 'utf-8').encode(), 'AInvestor110@gmail.com'))

        # 连接到 Gmail 的 SMTP 服务器
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        try:
            smtp.login('AInvestor110@gmail.com', 'bmuwqhmuxqphdbpo')
            smtp.sendmail('AInvestor110@gmail.com', input_email, msg.as_string())
            print('郵件傳送成功！')
        except Exception as e:
            print('郵件傳送失敗！', e)
        finally:
            smtp.quit()
