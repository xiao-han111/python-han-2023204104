"""异常处理工具类模块"""
import traceback
from PyQt5.QtWidgets import QMessageBox
from utils.logger import get_logger

logger = get_logger()


def show_error_dialog(title: str, message: str):
    """
    显示错误对话框
    
    Args:
        title: 对话框标题
        message: 错误信息
    """
    QMessageBox.critical(None, title, message)


def show_warning_dialog(title: str, message: str):
    """
    显示警告对话框
    
    Args:
        title: 对话框标题
        message: 警告信息
    """
    QMessageBox.warning(None, title, message)


def show_info_dialog(title: str, message: str):
    """
    显示信息对话框
    
    Args:
        title: 对话框标题
        message: 信息内容
    """
    QMessageBox.information(None, title, message)


def handle_exception(func):
    """
    异常处理装饰器
    
    Args:
        func: 被装饰的函数
    
    Returns:
        function: 装饰后的函数
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 记录异常信息
            logger.error(f"Exception in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # 显示错误信息
            error_msg = f"发生错误: {str(e)}"
            show_error_dialog("错误", error_msg)
            return None
    return wrapper


def log_exception(exception: Exception, context: str = ""):
    """
    记录异常信息
    
    Args:
        exception: 异常对象
        context: 上下文信息
    """
    logger.error(f"{context}Exception: {str(exception)}")
    logger.error(traceback.format_exc())
