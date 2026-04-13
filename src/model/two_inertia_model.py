"""双惯性环节串联模型模块"""
from config import SAMPLE_TIME

class FirstOrderLag:
    """一阶惯性环节类"""
    
    def __init__(self, time_constant: float, gain: float = 1.0):
        """
        初始化一阶惯性环节
        
        Args:
            time_constant: 时间常数
            gain: 增益
        """
        self.T = time_constant
        self.K = gain
        self.output = 0.0
        self.last_input = 0.0
    
    def reset(self):
        """重置环节状态"""
        self.output = 0.0
        self.last_input = 0.0
    
    def set_parameters(self, time_constant: float, gain: float):
        """
        设置环节参数
        
        Args:
            time_constant: 时间常数
            gain: 增益
        """
        self.T = time_constant
        self.K = gain
    
    def update(self, input_value: float) -> float:
        """
        更新环节状态并计算输出
        
        Args:
            input_value: 输入值
        
        Returns:
            float: 输出值
        """
        # 一阶惯性环节的离散化实现（欧拉法）
        dt = SAMPLE_TIME
        alpha = dt / (self.T + dt)
        self.output = (1 - alpha) * self.output + alpha * self.K * input_value
        self.last_input = input_value
        return self.output

class TwoInertiaModel:
    """双惯性环节串联模型类"""
    
    def __init__(self, T1: float = 1.0, T2: float = 2.0, gain: float = 1.0):
        """
        初始化双惯性环节串联模型
        
        Args:
            T1: 第一惯性环节时间常数
            T2: 第二惯性环节时间常数
            gain: 总增益
        """
        # 第一惯性环节
        self.inertia1 = FirstOrderLag(time_constant=T1, gain=1.0)
        # 第二惯性环节
        self.inertia2 = FirstOrderLag(time_constant=T2, gain=gain)
    
    def reset(self):
        """重置模型状态"""
        self.inertia1.reset()
        self.inertia2.reset()
    
    def set_parameters(self, T1: float, T2: float, gain: float):
        """
        设置模型参数
        
        Args:
            T1: 第一惯性环节时间常数
            T2: 第二惯性环节时间常数
            gain: 总增益
        """
        self.inertia1.set_parameters(time_constant=T1, gain=1.0)
        self.inertia2.set_parameters(time_constant=T2, gain=gain)
    
    def update(self, input_value: float, disturbance: float = 0.0) -> tuple:
        """
        更新模型状态并计算输出
        
        Args:
            input_value: 控制输入值
            disturbance: 干扰信号
        
        Returns:
            tuple: (中间变量, 最终输出)
        """
        # 第一惯性环节输出（中间变量）
        intermediate = self.inertia1.update(input_value)
        # 第二惯性环节输入 = 第一惯性环节输出
        # 第二惯性环节输出 = 最终输出 + 干扰
        output = self.inertia2.update(intermediate) + disturbance
        return intermediate, output
    
    def get_state(self) -> dict:
        """
        获取模型状态
        
        Returns:
            dict: 模型状态
        """
        return {
            'inertia1_output': self.inertia1.output,
            'inertia2_output': self.inertia2.output
        }
