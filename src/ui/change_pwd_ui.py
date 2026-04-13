"""修改密码对话框模块"""
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from user.user_manager import user_manager
from exception import AuthenticationError
from utils.exception_handler import show_info_dialog, show_error_dialog

class ChangePasswordDialog(QDialog):
    """修改密码对话框类"""
    
    def __init__(self, user_id, parent=None):
        """
        初始化修改密码对话框
        
        Args:
            user_id: 用户ID
            parent: 父控件
        """
        super().__init__(parent)
        self.setWindowTitle("修改密码")
        self.setFixedSize(400, 200)
        self.user_id = user_id
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 旧密码
        old_pwd_layout = QHBoxLayout()
        old_pwd_label = QLabel("旧密码:")
        self.old_pwd_edit = QLineEdit()
        self.old_pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        old_pwd_layout.addWidget(old_pwd_label)
        old_pwd_layout.addWidget(self.old_pwd_edit)
        layout.addLayout(old_pwd_layout)
        
        # 新密码
        new_pwd_layout = QHBoxLayout()
        new_pwd_label = QLabel("新密码:")
        self.new_pwd_edit = QLineEdit()
        self.new_pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        new_pwd_layout.addWidget(new_pwd_label)
        new_pwd_layout.addWidget(self.new_pwd_edit)
        layout.addLayout(new_pwd_layout)
        
        # 确认新密码
        confirm_pwd_layout = QHBoxLayout()
        confirm_pwd_label = QLabel("确认新密码:")
        self.confirm_pwd_edit = QLineEdit()
        self.confirm_pwd_edit.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_pwd_layout.addWidget(confirm_pwd_label)
        confirm_pwd_layout.addWidget(self.confirm_pwd_edit)
        layout.addLayout(confirm_pwd_layout)
        
        # 按钮
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("确定")
        self.ok_btn.clicked.connect(self.on_ok)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
    
    def on_ok(self):
        """确定按钮点击事件"""
        old_password = self.old_pwd_edit.text()
        new_password = self.new_pwd_edit.text()
        confirm_password = self.confirm_pwd_edit.text()
        
        # 验证输入
        if not old_password:
            show_error_dialog("错误", "请输入旧密码")
            return
        
        if not new_password:
            show_error_dialog("错误", "请输入新密码")
            return
        
        if new_password != confirm_password:
            show_error_dialog("错误", "两次输入的新密码不一致")
            return
        
        try:
            # 修改密码
            user_manager.change_password(self.user_id, old_password, new_password)
            show_info_dialog("成功", "密码修改成功")
            self.accept()
        except AuthenticationError as e:
            show_error_dialog("错误", str(e))
        except Exception as e:
            show_error_dialog("错误", f"修改密码失败：{str(e)}")
