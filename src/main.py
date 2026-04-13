"""程序入口文件"""
import sys
import os
import traceback

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from exception import handle_ui_exception

# 设置全局异常处理器
sys.excepthook = handle_ui_exception


def main():
    """主函数"""
    app = QApplication(sys.argv)
    # ✅ 关键修复：禁止最后一个窗口关闭时自动退出程序
    #app.setQuitOnLastWindowClosed(False)
    main_window = None  # 外部变量，避免被垃圾回收
    # 打开登录窗口
    login_window = LoginWindow()
    
    def on_login_success(user_info):
        """登录成功回调"""
        nonlocal main_window  # 引用外部变量
        print(f"登录成功，用户信息: {user_info}")
        print("创建主窗口...")
        main_window = MainWindow(user_info)
        print("主窗口创建成功，显示窗口...")
        main_window.show()
        print("主窗口显示成功")
    
    login_window.set_login_success_callback(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
