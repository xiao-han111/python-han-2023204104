"""时间格式化工具模块"""
from datetime import datetime


def get_current_time_str() -> str:
    """
    获取当前时间的字符串表示
    
    Returns:
        str: 当前时间字符串，格式为"YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_current_timestamp() -> str:
    """
    获取当前时间戳字符串
    
    Returns:
        str: 当前时间戳，格式为"YYYYMMDD_HHMMSS"
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def format_time(seconds: float) -> str:
    """
    格式化时间（秒）为可读字符串
    
    Args:
        seconds: 时间（秒）
    
    Returns:
        str: 格式化后的时间字符串
    """
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:.1f}"


def parse_time_str(time_str: str) -> datetime:
    """
    解析时间字符串为datetime对象
    
    Args:
        time_str: 时间字符串，格式为"YYYY-MM-DD HH:MM:SS"
    
    Returns:
        datetime: 解析后的datetime对象
    """
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
