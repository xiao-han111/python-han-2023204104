"""全局异常处理模块"""
import traceback
import logging
from PyQt5.QtWidgets import QMessageBox
from config import LOG_FILE

# 配置日志
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class AppException(Exception):
    """应用程序异常基类"""
    pass

class ParameterError(AppException):
    """参数错误异常"""
    pass

class AuthenticationError(AppException):
    """认证错误异常"""
    pass

class FileOperationError(AppException):
    """文件操作异常"""
    pass

class ControlError(AppException):
    """控制算法异常"""
    pass

def handle_exception(func):
    """异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 记录异常信息
            logging.error(f"Exception in {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            
            # 显示错误信息
            error_msg = f"发生错误: {str(e)}"
            QMessageBox.critical(None, "错误", error_msg)
            return None
    return wrapper

def handle_ui_exception(exc_type, exc_value, exc_traceback):
    """全局UI异常处理器"""
    # 记录异常信息
    logging.error(f"UI Exception: {exc_type.__name__}: {exc_value}")
    logging.error(traceback.format_exc())
    
    # 显示错误信息
    error_msg = f"程序发生错误: {exc_value}\n请联系管理员"
    QMessageBox.critical(None, "错误", error_msg)
