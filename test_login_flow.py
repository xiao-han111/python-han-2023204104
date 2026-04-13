"""登录流程测试脚本"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("登录")
        self.setFixedSize(400, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 用户名
        user_layout = QVBoxLayout()
        user_label = QLabel("用户名:")
        self.user_edit = QLineEdit()
        self.user_edit.setText("admin")
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_edit)
        layout.addLayout(user_layout)
        
        # 密码
        pwd_layout = QVBoxLayout()
        pwd_label = QLabel("密码:")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_edit.setText("admin123")
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_edit)
        layout.addLayout(pwd_layout)
        
        # 登录按钮
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.on_login)
        layout.addWidget(self.login_btn)
        
        # 回调函数
        self.login_success_callback = None
    
    def on_login(self):
        """登录按钮点击事件"""
        user_id = self.user_edit.text().strip()
        password = self.pwd_edit.text()
        
        print(f"登录尝试: {user_id}")
        
        # 模拟登录成功
        user_info = {'id': user_id, 'role': 'admin'}
        
        if self.login_success_callback:
            print("调用登录成功回调...")
            self.login_success_callback(user_info)
        
        print("关闭登录窗口...")
        self.close()
    
    def set_login_success_callback(self, callback):
        """设置登录成功回调函数"""
        self.login_success_callback = callback

class TestMainWindow(QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
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
        
        print("主窗口创建成功")

if __name__ == '__main__':
    print("创建应用程序...")
    app = QApplication(sys.argv)
    print("应用程序创建成功")
    
    print("创建登录窗口...")
    login_window = LoginWindow()
    print("登录窗口创建成功")
    
    def on_login_success(user_info):
        """登录成功回调"""
        print(f"登录成功，用户信息: {user_info}")
        print("创建主窗口...")
        main_window = TestMainWindow(user_info)
        print("显示主窗口...")
        main_window.show()
        print("主窗口显示成功")
    
    login_window.set_login_success_callback(on_login_success)
    print("显示登录窗口...")
    login_window.show()
    print("登录窗口显示成功")
    
    print("进入事件循环...")
    sys.exit(app.exec_())
