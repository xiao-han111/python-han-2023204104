"""用户管理窗口模块"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from user.user_manager import user_manager
from exception import FileOperationError
from utils.exception_handler import show_info_dialog, show_error_dialog

class UserManagerWindow(QMainWindow):
    """用户管理窗口类"""
    
    def __init__(self, parent=None):
        """
        初始化用户管理窗口
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.setWindowTitle("用户管理")
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 控制面板
        control_layout = QHBoxLayout()
        
        # 用户ID
        control_layout.addWidget(QLabel("用户ID:"))
        self.user_id_edit = QLineEdit()
        control_layout.addWidget(self.user_id_edit)
        
        # 密码
        control_layout.addWidget(QLabel("密码:"))
        self.password_edit = QLineEdit()
        control_layout.addWidget(self.password_edit)
        
        # 角色
        control_layout.addWidget(QLabel("角色:"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'user'])
        control_layout.addWidget(self.role_combo)
        
        layout.addLayout(control_layout)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("添加")
        self.add_btn.clicked.connect(self.add_user)
        self.update_btn = QPushButton("修改")
        self.update_btn.clicked.connect(self.update_user)
        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self.delete_user)
        self.clear_btn = QPushButton("清空")
        self.clear_btn.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)
        
        # 用户表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["用户ID", "密码", "角色"])
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.cellClicked.connect(self.on_cell_clicked)
        layout.addWidget(self.table_widget)
    
    def load_users(self):
        """加载用户列表"""
        users = user_manager.get_all_users()
        self.table_widget.setRowCount(len(users))
        
        for i, user in enumerate(users):
            self.table_widget.setItem(i, 0, QTableWidgetItem(user['id']))
            self.table_widget.setItem(i, 1, QTableWidgetItem(user['password']))
            self.table_widget.setItem(i, 2, QTableWidgetItem(user['role']))
        
        # 自动调整列宽
        self.table_widget.resizeColumnsToContents()
    
    def on_cell_clicked(self, row, column):
        """点击表格单元格"""
        user_id = self.table_widget.item(row, 0).text()
        password = self.table_widget.item(row, 1).text()
        role = self.table_widget.item(row, 2).text()
        
        # 填充到输入框
        self.user_id_edit.setText(user_id)
        self.password_edit.setText(password)
        self.role_combo.setCurrentText(role)
    
    def add_user(self):
        """添加用户"""
        user_id = self.user_id_edit.text().strip()
        password = self.password_edit.text()
        role = self.role_combo.currentText()
        
        if not user_id:
            show_error_dialog("错误", "请输入用户ID")
            return
        
        if not password:
            show_error_dialog("错误", "请输入密码")
            return
        
        try:
            user_manager.add_user(user_id, password, role)
            show_info_dialog("成功", "用户添加成功")
            self.load_users()
            self.clear_fields()
        except FileOperationError as e:
            show_error_dialog("错误", str(e))
        except Exception as e:
            show_error_dialog("错误", f"添加用户失败：{str(e)}")
    
    def update_user(self):
        """修改用户"""
        user_id = self.user_id_edit.text().strip()
        password = self.password_edit.text()
        role = self.role_combo.currentText()
        
        if not user_id:
            show_error_dialog("错误", "请选择要修改的用户")
            return
        
        try:
            user_manager.update_user(user_id, password, role)
            show_info_dialog("成功", "用户修改成功")
            self.load_users()
            self.clear_fields()
        except FileOperationError as e:
            show_error_dialog("错误", str(e))
        except Exception as e:
            show_error_dialog("错误", f"修改用户失败：{str(e)}")
    
    def delete_user(self):
        """删除用户"""
        user_id = self.user_id_edit.text().strip()
        
        if not user_id:
            show_error_dialog("错误", "请选择要删除的用户")
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self, "确认", f"确定要删除用户 {user_id} 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                user_manager.delete_user(user_id)
                show_info_dialog("成功", "用户删除成功")
                self.load_users()
                self.clear_fields()
            except FileOperationError as e:
                show_error_dialog("错误", str(e))
            except Exception as e:
                show_error_dialog("错误", f"删除用户失败：{str(e)}")
    
    def clear_fields(self):
        """清空输入字段"""
        self.user_id_edit.clear()
        self.password_edit.clear()
        self.role_combo.setCurrentIndex(0)
