"""数据记录器模块"""
import json
import os
from datetime import datetime
from config import HISTORY_DATA_TEMPLATE
from utils.logger import get_logger

logger = get_logger()

class DataLogger:
    """数据记录器类"""
    
    def __init__(self):
        """初始化数据记录器"""
        self.current_data = []
        self.current_session_id = None
    
    def start_session(self):
        """
        开始一个新的数据记录会话
        """
        # 生成会话ID（使用时间戳）
        self.current_session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_data = []
        logger.info(f"开始新的数据记录会话: {self.current_session_id}")
    
    def add_data_point(self, time: float, sv: float, pv: float, u: float, disturbance: float):
        """
        添加数据点
        
        Args:
            time: 时间
            sv: 设定值
            pv: 过程值
            u: 控制量
            disturbance: 干扰
        """
        data_point = {
            'time': time,
            'sv': sv,
            'pv': pv,
            'u': u,
            'disturbance': disturbance,
            'timestamp': datetime.now().isoformat()
        }
        self.current_data.append(data_point)
    
    def save_session(self):
        """
        保存当前会话数据
        """
        if not self.current_session_id or not self.current_data:
            return
        
        try:
            # 生成文件名
            file_path = HISTORY_DATA_TEMPLATE.format(self.current_session_id)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存数据
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"数据会话保存成功: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"保存数据失败: {str(e)}")
            return None
    
    def get_history_files(self) -> list:
        """
        获取所有历史数据文件
        
        Returns:
            list: 历史数据文件路径列表
        """
        history_dir = os.path.dirname(HISTORY_DATA_TEMPLATE.format(''))
        if not os.path.exists(history_dir):
            return []
        
        files = []
        for file in os.listdir(history_dir):
            if file.startswith('history_') and file.endswith('.json'):
                files.append(os.path.join(history_dir, file))
        
        # 按时间排序（最新的在前）
        files.sort(key=os.path.getmtime, reverse=True)
        return files
    
    def load_history_data(self, file_path: str) -> list:
        """
        加载历史数据
        
        Args:
            file_path: 历史数据文件路径
        
        Returns:
            list: 历史数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"加载历史数据失败: {str(e)}")
            return []
    
    def clear_current_data(self):
        """
        清空当前数据
        """
        self.current_data = []
    
    def get_current_data(self) -> list:
        """
        获取当前数据
        
        Returns:
            list: 当前数据
        """
        return self.current_data

# 创建全局数据记录器实例
data_logger = DataLogger()
