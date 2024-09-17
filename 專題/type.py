import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QTabBar, QStylePainter, QStyleOptionTab, QVBoxLayout, QWidget, QStyle
from PyQt5.QtCore import QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor

class CustomTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.line_rect = QRect()  # 用于绘制青色线条的矩形
        self.current_tab_index = 0

    def paintEvent(self, event):
        # 使用 QStylePainter 绘制 Tab
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        # 遍历每个 Tab 进行绘制
        for index in range(self.count()):
            self.initStyleOption(option, index)
            painter.drawControl(QStyle.CE_TabBarTab, option)

        # 绘制自定义的青色线条
        if not self.line_rect.isEmpty():
            painter.setPen(QColor(0, 170, 255))  # 设置青色
            painter.setBrush(QColor(0, 170, 255))
            painter.drawRect(self.line_rect)

    def update_line_position(self, index):
        # 获取当前选中的 tab 的矩形区域
        rect = self.tabRect(index)
        self.line_rect = QRect(rect.left(), rect.bottom() - 2, rect.width(), 2)
        self.update()

    def animate_line(self, current_index, next_index):
        # 动画处理，根据左右切换来设置动画效果
        current_rect = self.tabRect(current_index)
        next_rect = self.tabRect(next_index)

        self.animation = QPropertyAnimation(self, b"line_rect")
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(current_rect.left(), current_rect.bottom() - 2, current_rect.width(), 2))

        if next_index > current_index:
            # 从右侧进入
            self.animation.setEndValue(QRect(next_rect.left(), next_rect.bottom() - 2, next_rect.width(), 2))
            self.animation.setEasingCurve(QEasingCurve.OutCubic)
        else:
            # 从左侧进入
            self.animation.setEndValue(QRect(next_rect.left(), next_rect.bottom() - 2, next_rect.width(), 2))
            self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.animation.start()

    def setCurrentIndex(self, index):
        self.animate_line(self.current_tab_index, index)
        self.current_tab_index = index
        super().setCurrentIndex(index)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建 TabWidget 和自定义 TabBar
        self.tab_widget = QTabWidget(self)
        self.custom_tab_bar = CustomTabBar()

        # 设置自定义 TabBar
        self.tab_widget.setTabBar(self.custom_tab_bar)

        # 添加几个 Tab
        self.tab_widget.addTab(QWidget(), "Tab 1")
        self.tab_widget.addTab(QWidget(), "Tab 2")
        self.tab_widget.addTab(QWidget(), "Tab 3")

        # 初始化线条位置
        self.custom_tab_bar.update_line_position(0)

        # 设置布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

        # 信号槽连接，检测 Tab 切换时更新线条动画
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        # 更新线条位置和动画
        self.custom_tab_bar.setCurrentIndex(index)
        self.custom_tab_bar.update_line_position(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
