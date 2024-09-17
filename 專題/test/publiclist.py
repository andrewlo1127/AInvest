from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import requests

class Ui_StrategyList2(object):
    def setupUi(self, StrategyList2):
        StrategyList2.setObjectName("StrategyList2")
        StrategyList2.resize(960, 500)  #窗口大小
        self.centralwidget = QtWidgets.QWidget(StrategyList2)
        self.centralwidget.setObjectName("centralwidget")

        self.PublicStrategy = QtWidgets.QTableWidget(self.centralwidget)
        self.PublicStrategy.setGeometry(QtCore.QRect(20, 20, 920, 400))  #表格大小
        self.PublicStrategy.setObjectName("PublicStrategy")
        self.PublicStrategy.setColumnCount(3)
        self.PublicStrategy.setHorizontalHeaderLabels(["Strategy", "Description", ""])
        self.PublicStrategy.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        
        # 設置列寬度
        header = self.PublicStrategy.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        StrategyList2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StrategyList2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 960, 25))  # 欄位大小
        self.menubar.setObjectName("menubar")
        StrategyList2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StrategyList2)
        self.statusbar.setObjectName("statusbar")
        StrategyList2.setStatusBar(self.statusbar)

        self.retranslateUi(StrategyList2)
        QtCore.QMetaObject.connectSlotsByName(StrategyList2)

        # Fetch and populate data
        self.fetchData()

    def retranslateUi(self, StrategyList2):
        _translate = QtCore.QCoreApplication.translate
        StrategyList2.setWindowTitle(_translate("StrategyList2", "公開策略"))

    def fetchData(self):
        try:
            response = requests.get("http://127.0.0.1:5000/list?public=1")
            data = response.json()
            self.PublicStrategy.setRowCount(len(data))
            for row, item in enumerate(data):
                strategy_item = QtWidgets.QTableWidgetItem(item['strategy_name'])
                strategy_item.setFlags(strategy_item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.PublicStrategy.setItem(row, 0, strategy_item)

                description_item = QtWidgets.QTableWidgetItem(item['description'])
                description_item.setFlags(description_item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.PublicStrategy.setItem(row, 1, description_item)

                btn = QtWidgets.QPushButton('查看')
                btn.clicked.connect(partial(self.viewDetail, row))
                self.PublicStrategy.setCellWidget(row, 2, btn)

                # Store hidden data in table (as userData in QTableWidgetItem)
                strategy_item.setData(QtCore.Qt.UserRole, (item['strategy_name'], item['member_id']))

        except Exception as e:
            print(f"Error fetching data: {e}")

    def viewDetail(self, row):
        item = self.PublicStrategy.item(row, 0)
        strategy_name, member_id = item.data(QtCore.Qt.UserRole)

        try:
            response = requests.post("http://127.0.0.1:5000/get_file", json={'strategy_name': strategy_name, 'member_id': member_id})
            if response.status_code == 200:
                file_content = response.text
                self.showFileContentDialog(file_content)
            else:
                self.showFileContentDialog(f"Error: {response.json().get('message', 'Unknown error')}")
        except Exception as e:
            self.showFileContentDialog(f"Error: {str(e)}")

    def showFileContentDialog(self, content):
        dialog = FileContentDialog(content)
        dialog.exec_()

class FileContentDialog(QtWidgets.QDialog):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("檔案內容")
        self.resize(600, 400)
        layout = QtWidgets.QVBoxLayout(self)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setPlainText(content)
        self.textEdit.setReadOnly(True)  # ReadOnly
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    StrategyList2 = QtWidgets.QMainWindow()
    ui = Ui_StrategyList2()
    ui.setupUi(StrategyList2)
    StrategyList2.show()
    sys.exit(app.exec_())
