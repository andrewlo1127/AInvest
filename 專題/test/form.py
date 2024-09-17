from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(960, 500)  # 修改主視窗的大小

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setEnabled(True)
        self.pushButton.setGeometry(QtCore.QRect(860, 70, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.description = QtWidgets.QPlainTextEdit(Form)
        self.description.setGeometry(QtCore.QRect(330, 50, 361, 71))
        self.description.setObjectName("description")

        self.strategyName = QtWidgets.QLineEdit(Form)
        self.strategyName.setGeometry(QtCore.QRect(110, 50, 113, 22))
        self.strategyName.setObjectName("strategyName")

        self.code = QtWidgets.QPlainTextEdit(Form)
        self.code.setGeometry(QtCore.QRect(50, 150, 901, 321))  # 高度調整為 321
        self.code.setObjectName("code")

        self.label_description = QtWidgets.QLabel(Form)
        self.label_description.setGeometry(QtCore.QRect(250, 50, 71, 21))
        self.label_description.setObjectName("label_description")

        self.label_strategyName = QtWidgets.QLabel(Form)
        self.label_strategyName.setGeometry(QtCore.QRect(30, 40, 91, 41))
        self.label_strategyName.setObjectName("label_strategyName")

        self.public_2 = QtWidgets.QComboBox(Form)
        self.public_2.setGeometry(QtCore.QRect(730, 50, 80, 22))
        self.public_2.setObjectName("public_2")
        self.public_2.addItem("不公開", 0)  # 设置项和值
        self.public_2.addItem("公開", 1)    # 设置项和值

        # 隱藏欄位
        self.memberID = QtWidgets.QLineEdit(Form)
        self.memberID.setGeometry(QtCore.QRect(0, 0, 0, 0)) # 放到看不見的地方
        self.memberID.setObjectName("memberID")
        self.memberID.setHidden(True)

        self.filename = QtWidgets.QLineEdit(Form)
        self.filename.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.filename.setObjectName("filename")
        self.filename.setHidden(True)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 事件綁定
        self.pushButton.clicked.connect(self.saveForm)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "儲存"))
        self.strategyName.setText(_translate("Form", "未命名策略"))
        self.label_description.setText(_translate("Form", "策略概述"))
        self.label_strategyName.setText(_translate("Form", "策略名稱"))
        self.public_2.setItemText(0, _translate("Form", "不公開"))
        self.public_2.setItemText(1, _translate("Form", "公開"))
        # 載入表單
        self.loadForm()

    def loadForm(self):
        response = requests.get('http://127.0.0.1:5000/edit', params={'filename': 'file.txt'}) # 'filename' 取決於點哪一個策略編輯
        if response.status_code == 200:
            data = response.json()
            self.strategyName.setText(data['strategyName'])
            self.description.setPlainText(data['description'])
            self.code.setPlainText(data['code'])
            self.public_2.setCurrentIndex(data['public'])
            self.memberID.setText(data['memberID'])
            self.filename.setText(data['filename'])

    def saveForm(self):
        data = {
            'memberID': self.memberID.text(),
            'strategyName': self.strategyName.text(),
            'filename': self.filename.text(),
            'public': self.public_2.currentIndex(),
            'description': self.description.toPlainText()
        }

        # 發送表單內容
        response = requests.post('http://127.0.0.1:5000/save', data=data)
        if response.status_code == 200:
            QtWidgets.QMessageBox.information(None, 'OK', '保存成功！')
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', '保存失敗！')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
