"""干扰信号模块"""
from config import SAMPLE_TIME

class SquareWaveDisturbance:
    """方波干扰信号类"""
    
    def __init__(self, amplitude: float = 0.0, duration: float = 0.0):
        """
        初始化方波干扰信号
        
        Args:
            amplitude: 干扰振幅
            duration: 干扰持续时间（秒）
        """
        self.amplitude = amplitude
        self.duration = duration
        self.remaining_time = 0.0
        self.active = False
    
    def reset(self):
        """重置干扰状态"""
        self.remaining_time = 0.0
        self.active = False
    
    def set_parameters(self, amplitude: float, duration: float):
        """
        设置干扰参数
        
        Args:
            amplitude: 干扰振幅
            duration: 干扰持续时间（秒）
        """
        self.amplitude = amplitude
        self.duration = duration
    
    def start(self):
        """
        开始施加干扰
        """
        self.remaining_time = self.duration
        self.active = True
    
    def update(self) -> float:
        """
        更新干扰状态并计算当前干扰值
        
        Returns:
            float: 当前干扰值
        """
        if not self.active:
            return 0.0
        
        # 计算当前干扰值
        current_disturbance = self.amplitude
        
        # 减少剩余时间
        self.remaining_time -= SAMPLE_TIME
        
        # 检查是否结束
        if self.remaining_time <= 0:
            self.active = False
            self.remaining_time = 0.0
            return 0.0
        
        return current_disturbance
    
    def is_active(self) -> bool:
        """
        检查干扰是否活跃
        
        Returns:
            bool: 干扰是否活跃
        """
        return self.active
    
    def get_remaining_time(self) -> float:
        """
        获取剩余干扰时间
        
        Returns:
            float: 剩余干扰时间（秒）
        """
        return self.remaining_time

class DisturbanceGenerator:
    """干扰信号管理器类"""
    
    def __init__(self):
        """
        初始化干扰信号管理器
        """
        self.square_wave = SquareWaveDisturbance()
        self.current_disturbance = 0.0
    
    def reset(self):
        """
        重置所有干扰
        """
        self.square_wave.reset()
        self.current_disturbance = 0.0
    
    def set_square_wave_parameters(self, amplitude: float, duration: float):
        """
        设置方波干扰参数
        
        Args:
            amplitude: 干扰振幅
            duration: 干扰持续时间（秒）
        """
        self.square_wave.set_parameters(amplitude, duration)
    
    def start_square_wave(self):
        """
        开始施加方波干扰
        """
        self.square_wave.start()
    
    def update(self) -> float:
        """
        更新所有干扰并计算总干扰值
        
        Returns:
            float: 总干扰值
        """
        # 更新方波干扰
        square_wave_disturbance = self.square_wave.update()
        
        # 计算总干扰
        self.current_disturbance = square_wave_disturbance
        
        return self.current_disturbance
    
    def is_active(self) -> bool:
        """
        检查是否有活跃的干扰
        
        Returns:
            bool: 是否有活跃的干扰
        """
        return self.square_wave.is_active()
    
    def get_remaining_time(self) -> float:
        """
        获取剩余干扰时间
        
        Returns:
            float: 剩余干扰时间（秒）
        """
        return self.square_wave.get_remaining_time()
