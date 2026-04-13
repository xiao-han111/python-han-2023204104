"""登录界面模块"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from user.user_manager import user_manager
from exception import AuthenticationError

class LoginWindow(QMainWindow):
    """登录界面类"""
    
    def __init__(self, parent=None):
        """
        初始化登录界面
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.setWindowTitle("PID温度控制仿真系统 - 登录")
        self.setFixedSize(400, 200)
        self.init_ui()
        
        # 登录成功回调
        self.login_success_callback = None
    
    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 标题
        title_label = QLabel("PID温度控制仿真系统")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 用户名
        user_layout = QHBoxLayout()
        user_label = QLabel("用户名:")
        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("请输入用户名")
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_edit)
        layout.addLayout(user_layout)
        
        # 密码
        pwd_layout = QHBoxLayout()
        pwd_label = QLabel("密码:")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd_edit.setPlaceholderText("请输入密码")
        pwd_layout.addWidget(pwd_label)
        pwd_layout.addWidget(self.pwd_edit)
        layout.addLayout(pwd_layout)
        
        # 按钮
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("登录")
        self.login_btn.clicked.connect(self.on_login)
        self.exit_btn = QPushButton("退出")
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.exit_btn)
        layout.addLayout(btn_layout)
        
        # 默认值
        self.user_edit.setText("admin")
        self.pwd_edit.setText("admin123")
    
    def on_login(self):
        """登录按钮点击事件"""
        user_id = self.user_edit.text().strip()
        password = self.pwd_edit.text()
        
        if not user_id:
            QMessageBox.warning(self, "警告", "请输入用户名")
            return
        
        if not password:
            QMessageBox.warning(self, "警告", "请输入密码")
            return
        
        try:
            # 验证用户
            user_info = user_manager.authenticate(user_id, password)
            
            # 登录成功
            if self.login_success_callback:
                self.login_success_callback(user_info)
            
            self.close()
        except AuthenticationError as e:
            QMessageBox.warning(self, "登录失败", str(e))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"登录过程中发生错误: {str(e)}")
    
    def set_login_success_callback(self, callback):
        """
        设置登录成功回调函数
        
        Args:
            callback: 回调函数，接收用户信息作为参数
        """
        self.login_success_callback = callback
