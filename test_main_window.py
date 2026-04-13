"""简化版主窗口测试脚本"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class TestMainWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("PID温度控制仿真系统")
        self.setMinimumSize(800, 600)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        
        # 欢迎信息
        welcome_label = QLabel(f"欢迎，{user_info['id']}！")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(welcome_label)
        
        # 状态信息
        status_label = QLabel("系统就绪")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status_label)

if __name__ == '__main__':
    # 模拟用户信息
    user_info = {'id': 'admin', 'role': 'admin'}
    
    print("创建应用程序...")
    app = QApplication(sys.argv)
    
    print("创建主窗口...")
    window = TestMainWindow(user_info)
    
    print("显示主窗口...")
    window.show()
    
    print("进入事件循环...")
    sys.exit(app.exec_())
