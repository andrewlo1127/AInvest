import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import *

class ChatbotWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Botpress Webchat")
        self.setGeometry(1567, 106, 351, 504)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 创建 QWebEngineView
        self.browser = QWebEngineView()
        self.browser.setZoomFactor(1.0)

        # 设置 HTML 内容
        html_content = """
        <html>
        <head>
            <script src="https://cdn.botpress.cloud/webchat/v2/inject.js"></script>
            <script src="https://mediafiles.botpress.cloud/26a83f89-ace1-4045-92ba-95b836f75669/webchat/v2/config.js"></script>
        </head>
        <body>
            <button id="openBotpress" style="display: none;">Open Botpress</button>
            <script defer>
                async function openBotpress() {
                    window.botpress.open();
                }
            </script>
        </body>
        </html>
        """
        self.browser.setHtml(html_content)

        # 创建按钮

        # 使用布局管理器
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # 将布局应用到 QDialog
        self.setLayout(layout)

    def open_botpress_chat(self):
        # 执行 JavaScript 来触发 Botpress Webchat 窗口
        self.browser.page().runJavaScript("openBotpress();")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec_())
