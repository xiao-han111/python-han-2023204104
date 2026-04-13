"""PID控制器模块"""
from config import SAMPLE_TIME, CONTROL_LIMITS

class PIDController:
    """PID控制器类"""
    
    def __init__(self, Kp: float = 2.0, Ti: float = 2.0, Td: float = 0.5, 
                 anti_windup: bool = False, limits: tuple = None):
        """
        初始化PID控制器
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
            anti_windup: 是否启用抗积分饱和
            limits: 输出限制 (min, max)
        """
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
        self.anti_windup = anti_windup
        self.limits = limits if limits else (float('-inf'), float('inf'))
        
        # 内部变量
        self.last_error = 0.0
        self.integral = 0.0
        self.last_output = 0.0
    
    def reset(self):
        """重置控制器状态"""
        self.last_error = 0.0
        self.integral = 0.0
        self.last_output = 0.0
    
    def set_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
    
    def calculate(self, setpoint: float, process_value: float) -> float:
        """
        计算控制输出
        
        Args:
            setpoint: 设定值
            process_value: 过程值
        
        Returns:
            float: 控制输出
        """
        # 计算误差
        error = setpoint - process_value
        
        # 比例项
        proportional = self.Kp * error
        
        # 积分项（带抗积分饱和）
        if self.anti_windup:
            # 条件积分：只有当误差方向有利于退出饱和时才累积积分
            if not ((self.last_output >= self.limits[1] and error > 0) or 
                    (self.last_output <= self.limits[0] and error < 0)):
                if self.Ti > 0:
                    self.integral += (self.Kp / self.Ti) * error * SAMPLE_TIME
        else:
            if self.Ti > 0:
                self.integral += (self.Kp / self.Ti) * error * SAMPLE_TIME
        
        # 微分项
        derivative = 0.0
        if self.Td > 0:
            derivative = self.Kp * self.Td * (error - self.last_error) / SAMPLE_TIME
        
        # 计算总输出
        output = proportional + self.integral + derivative
        
        # 限幅
        output = max(self.limits[0], min(self.limits[1], output))
        
        # 更新状态
        self.last_error = error
        self.last_output = output
        
        return output
    
    def set_output(self, output: float):
        """
        设置输出值（用于手动/自动切换时的无扰动切换）
        
        Args:
            output: 控制输出值
        """
        self.last_output = output
        # 自动调整积分项以实现无扰动切换
        if self.Ti > 0:
            # 假设当前误差为0，计算积分项以匹配输出
            self.integral = output
    
    def get_state(self) -> dict:
        """
        获取控制器状态
        
        Returns:
            dict: 控制器状态
        """
        return {
            'Kp': self.Kp,
            'Ti': self.Ti,
            'Td': self.Td,
            'anti_windup': self.anti_windup,
            'limits': self.limits,
            'last_error': self.last_error,
            'integral': self.integral,
            'last_output': self.last_output
        }
