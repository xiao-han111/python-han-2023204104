"""Excel导出功能模块"""
import pandas as pd
import os
from datetime import datetime
from exception import FileOperationError
from utils.logger import get_logger

logger = get_logger()

def export_to_excel(data: list, filename: str = None) -> str:
    """
    导出数据到Excel文件
    
    Args:
        data: 数据列表，每个元素是包含时间、SV、PV、控制量u、干扰的字典
        filename: 导出文件名，默认使用当前时间
    
    Returns:
        str: 导出文件路径
    """
    try:
        if not data:
            raise FileOperationError("没有数据可导出")
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'history_{timestamp}.xlsx'
        
        # 确保文件路径存在
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'history_data')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 导出到Excel
        output_path = os.path.join(output_dir, filename)
        df.to_excel(output_path, index=False)
        
        logger.info(f"数据导出成功: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"导出数据失败: {str(e)}")
        raise FileOperationError(f"导出数据失败: {str(e)}")

def export_to_csv(data: list, filename: str = None) -> str:
    """
    导出数据到CSV文件
    
    Args:
        data: 数据列表，每个元素是包含时间、SV、PV、控制量u、干扰的字典
        filename: 导出文件名，默认使用当前时间
    
    Returns:
        str: 导出文件路径
    """
    try:
        if not data:
            raise FileOperationError("没有数据可导出")
        
        # 创建DataFrame
        df = pd.DataFrame(data)
        
        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'history_{timestamp}.csv'
        
        # 确保文件路径存在
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'history_data')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 导出到CSV
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        logger.info(f"数据导出成功: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"导出数据失败: {str(e)}")
        raise FileOperationError(f"导出数据失败: {str(e)}")
