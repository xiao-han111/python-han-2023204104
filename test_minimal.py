"""最小PyQt5测试脚本"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试窗口")
        self.setGeometry(100, 100, 400, 300)
        label = QLabel("PyQt5 测试成功！", self)
        label.setGeometry(150, 100, 100, 50)

if __name__ == '__main__':
    print("开始测试PyQt5...")
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    print("窗口已显示，进入事件循环...")
    sys.exit(app.exec_())
