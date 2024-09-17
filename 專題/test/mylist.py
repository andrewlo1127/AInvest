from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import requests

class Ui_StrategyList(object):
    def setupUi(self, StrategyList):
        StrategyList.setObjectName("StrategyList")
        StrategyList.resize(960, 500)  # 修改主窗口的大小
        self.centralwidget = QtWidgets.QWidget(StrategyList)
        self.centralwidget.setObjectName("centralwidget")

        self.MyStrategy = QtWidgets.QTableWidget(self.centralwidget)
        self.MyStrategy.setGeometry(QtCore.QRect(20, 20, 920, 350))  # 修改表格的大小
        self.MyStrategy.setObjectName("MyStrategy")
        self.MyStrategy.setColumnCount(3)
        self.MyStrategy.setHorizontalHeaderLabels(["Strategy", "Description", ""])
        self.MyStrategy.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        # 設置列寬度
        header = self.MyStrategy.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        StrategyList.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StrategyList)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 25))  # 修改菜單欄的大小
        self.menubar.setObjectName("menubar")
        StrategyList.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StrategyList)
        self.statusbar.setObjectName("statusbar")
        StrategyList.setStatusBar(self.statusbar)

        self.retranslateUi(StrategyList)
        QtCore.QMetaObject.connectSlotsByName(StrategyList)

        self.fetchData()

    def retranslateUi(self, StrategyList):
        _translate = QtCore.QCoreApplication.translate
        StrategyList.setWindowTitle(_translate("StrategyList", "我的策略"))

    def fetchData(self):
        try:
            response = requests.get("http://127.0.0.1:5000/list?public=0")
            data = response.json()
            self.MyStrategy.setRowCount(len(data))
            for row, item in enumerate(data):
                strategy_item = QtWidgets.QTableWidgetItem(item['strategy_name'])
                strategy_item.setFlags(strategy_item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.MyStrategy.setItem(row, 0, strategy_item)

                description_item = QtWidgets.QTableWidgetItem(item['description'])
                description_item.setFlags(description_item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.MyStrategy.setItem(row, 1, description_item)

                btn = QtWidgets.QPushButton('編輯')
                btn.clicked.connect(partial(self.viewDetail, row))
                self.MyStrategy.setCellWidget(row, 2, btn)

                # Store hidden data in table (as userData in QTableWidgetItem)
                strategy_item.setData(QtCore.Qt.UserRole, (item['member_id'], item['file_name']))

        except Exception as e:
            print(f"Error fetching data: {e}")
    
    def viewDetail(self, row):
        item = self.MyStrategy.item(row, 0)
        member_id, file_name = item.data(QtCore.Qt.UserRole)

        try:
            response = requests.get(f"http://127.0.0.1:5000/edit?filename={file_name}&member_id={member_id}")
            if response.status_code == 200:
                data = response.json()
                dialog = EditStrategyDialog(data)
                dialog.exec_()
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', f"Error: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, 'Error', f"Error: {str(e)}")

class EditStrategyDialog(QtWidgets.QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("編輯策略")
        self.resize(890, 480)  # 修改編輯對話框的大小
        self.data = data

        self.pushButton = QtWidgets.QPushButton("保存", self)
        self.pushButton.setGeometry(QtCore.QRect(790, 430, 93, 28))  # 修改保存按鈕的位置
        self.pushButton.clicked.connect(self.saveForm)

        self.description = QtWidgets.QPlainTextEdit(self)
        self.description.setGeometry(QtCore.QRect(330, 50, 361, 71))
        self.description.setObjectName("description")
        self.description.setPlainText(data['description'])

        self.strategyName = QtWidgets.QLineEdit(self)
        self.strategyName.setGeometry(QtCore.QRect(110, 50, 113, 22))
        self.strategyName.setObjectName("strategyName")
        self.strategyName.setText(data['strategyName'])

        self.code = QtWidgets.QPlainTextEdit(self)
        self.code.setGeometry(QtCore.QRect(50, 150, 790, 250))  # 修改代碼區域的大小
        self.code.setObjectName("code")
        self.code.setPlainText(data['code'])

        self.label_description = QtWidgets.QLabel("描述", self)
        self.label_description.setGeometry(QtCore.QRect(250, 50, 71, 21))
        self.label_description.setObjectName("label_description")

        self.label_strategyName = QtWidgets.QLabel("策略名稱", self)
        self.label_strategyName.setGeometry(QtCore.QRect(30, 40, 91, 41))
        self.label_strategyName.setObjectName("label_strategyName")

        self.public_2 = QtWidgets.QComboBox(self)
        self.public_2.setGeometry(QtCore.QRect(730, 50, 80, 22))
        self.public_2.setObjectName("public_2")
        self.public_2.addItem("不公開", 0)
        self.public_2.addItem("公開", 1)
        self.public_2.setCurrentIndex(data['public'])

        # 隱藏欄位
        self.memberID = QtWidgets.QLineEdit(self)
        self.memberID.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.memberID.setObjectName("memberID")
        self.memberID.setHidden(True)
        self.memberID.setText(data['memberID'])

        self.filename = QtWidgets.QLineEdit(self)
        self.filename.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.filename.setObjectName("filename")
        self.filename.setHidden(True)
        self.filename.setText(data['filename'])

    def saveForm(self):
        data = {
            'memberID': self.memberID.text(),
            'strategyName': self.strategyName.text(),
            'filename': self.filename.text(),
            'public': self.public_2.currentIndex(),
            'description': self.description.toPlainText(),
            'code': self.code.toPlainText()
        }

        try:
            response = requests.post('http://127.0.0.1:5000/save', json=data)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, '成功', '保存成功！')
            else:
                QtWidgets.QMessageBox.critical(self, '錯誤', '保存失敗！')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, '錯誤', f"保存過程中出現錯誤: {str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StrategyList = QtWidgets.QMainWindow()
    ui = Ui_StrategyList()
    ui.setupUi(StrategyList)
    StrategyList.show()
    sys.exit(app.exec_())
