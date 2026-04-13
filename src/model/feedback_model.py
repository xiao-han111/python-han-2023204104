"""反馈环节模型模块"""
import random
from config import SAMPLE_TIME, FILTER_TC

class FeedbackModel:
    """反馈环节模型类（一阶低通滤波器）"""
    
    def __init__(self, time_constant: float = FILTER_TC):
        """
        初始化反馈环节模型
        
        Args:
            time_constant: 滤波器时间常数
        """
        self.T = time_constant
        self.output = 0.0
        self.last_input = 0.0
    
    def reset(self):
        """重置环节状态"""
        self.output = 0.0
        self.last_input = 0.0
    
    def set_parameters(self, time_constant: float):
        """
        设置环节参数
        
        Args:
            time_constant: 滤波器时间常数
        """
        self.T = time_constant
    
    def update(self, input_value: float) -> float:
        """
        更新环节状态并计算输出
        
        Args:
            input_value: 输入值
        
        Returns:
            float: 输出值
        """
        # 一阶低通滤波器的离散化实现（欧拉法）
        dt = SAMPLE_TIME
        alpha = dt / (self.T + dt)
        self.output = (1 - alpha) * self.output + alpha * input_value
        self.last_input = input_value
        return self.output

class SensorWithNoise:
    """带噪声的传感器模型类"""
    
    def __init__(self, time_constant: float = FILTER_TC, noise_std: float = 0.1):
        """
        初始化带噪声的传感器模型
        
        Args:
            time_constant: 滤波器时间常数
            noise_std: 噪声标准差
        """
        self.feedback_model = FeedbackModel(time_constant=time_constant)
        self.noise_std = noise_std
    
    def reset(self):
        """重置传感器状态"""
        self.feedback_model.reset()
    
    def set_parameters(self, time_constant: float, noise_std: float):
        """
        设置传感器参数
        
        Args:
            time_constant: 滤波器时间常数
            noise_std: 噪声标准差
        """
        self.feedback_model.set_parameters(time_constant)
        self.noise_std = noise_std
    
    def update(self, input_value: float) -> float:
        """
        更新传感器状态并计算输出
        
        Args:
            input_value: 输入值
        
        Returns:
            float: 输出值（带噪声）
        """
        # 先通过低通滤波器
        filtered_value = self.feedback_model.update(input_value)
        # 添加高斯噪声
        noise = random.normalvariate(0, self.noise_std)
        return filtered_value + noise
