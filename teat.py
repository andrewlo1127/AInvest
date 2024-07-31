import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
from PyQt5 import uic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_connection = self.connect_to_db()
        self.first_ui()
    
    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='專題'
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Database Connection Error", f"Error: {err}")
            sys.exit()

    def first_ui(self): #登錄,註冊的UI
        self.ui = uic.loadUi("./first_main_ui.ui")
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.register)
    
    def login(self):#登錄
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM members WHERE m_01 = %s AND m_08 = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.fetchall()  # 把剩下的讀取完 不然sql會報錯
        if result:
            QMessageBox.information(None, "Login Success", "成功登錄")
            self.load_main_ui()
        else:
            QMessageBox.warning(None, "Login Failed", "用戶名或者密碼錯誤")
        cursor.close()

    def register(self):#註冊
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        cursor = self.db_connection.cursor()
        check_query = "SELECT * FROM members WHERE m_01 = %s"
        cursor.execute(check_query, (username,))
        result = cursor.fetchone()
        cursor.fetchall()  # 把剩下的讀取完 不然sql會報錯
        if result:
            QMessageBox.warning(None, "Registration Failed", "已經有人取過這個名字了")
        else:
            query = "INSERT INTO members (m_01, m_08) VALUES (%s, %s)"
            try:
                cursor.execute(query, (username, password))
                self.db_connection.commit()
                QMessageBox.information(None, "Registration Success", "You have successfully registered!")
            except mysql.connector.Error as err:
                QMessageBox.warning(None, "Registration Failed", f"Error: {err}")
            cursor.fetchall()  # 把剩下的讀取完 不然sql會報錯
        cursor.close()
    
    def load_main_ui(self):
        self.main_ui = uic.loadUi("./main_ui.ui")
        self.main_ui.show()
        self.ui.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Form = MainWindow()
    Form.ui.show()
    sys.exit(app.exec_())
