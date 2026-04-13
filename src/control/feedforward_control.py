"""前馈控制器模块"""
from control.pid_controller import PIDController
from config import CONTROL_LIMITS, FF_GAIN

class FeedforwardController:
    """前馈控制器类"""
    
    def __init__(self, gain: float = FF_GAIN):
        """
        初始化前馈控制器
        
        Args:
            gain: 前馈增益
        """
        self.gain = gain
    
    def calculate(self, disturbance: float) -> float:
        """
        计算前馈补偿输出
        
        Args:
            disturbance: 干扰信号
        
        Returns:
            float: 前馈补偿输出
        """
        return self.gain * disturbance
    
    def set_gain(self, gain: float):
        """
        设置前馈增益
        
        Args:
            gain: 前馈增益
        """
        self.gain = gain

class FeedforwardFeedbackController:
    """前馈+反馈复合控制器类"""
    
    def __init__(self, 
                 Kp: float = 2.0, Ti: float = 2.0, Td: float = 0.5, 
                 ff_gain: float = FF_GAIN):
        """
        初始化前馈+反馈控制器
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
            ff_gain: 前馈增益
        """
        # 反馈控制器
        self.feedback_controller = PIDController(
            Kp=Kp,
            Ti=Ti,
            Td=Td,
            anti_windup=True,
            limits=(CONTROL_LIMITS['min'], CONTROL_LIMITS['max'])
        )
        
        # 前馈控制器
        self.feedforward_controller = FeedforwardController(gain=ff_gain)
    
    def reset(self):
        """重置控制器状态"""
        self.feedback_controller.reset()
    
    def set_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        self.feedback_controller.set_parameters(Kp, Ti, Td)
    
    def set_ff_gain(self, gain: float):
        """
        设置前馈增益
        
        Args:
            gain: 前馈增益
        """
        self.feedforward_controller.set_gain(gain)
    
    def calculate(self, setpoint: float, process_value: float, disturbance: float) -> float:
        """
        计算控制输出
        
        Args:
            setpoint: 设定值
            process_value: 过程值
            disturbance: 干扰信号
        
        Returns:
            float: 控制输出
        """
        # 反馈控制输出
        feedback_output = self.feedback_controller.calculate(setpoint, process_value)
        
        # 前馈补偿输出
        ff_output = self.feedforward_controller.calculate(disturbance)
        
        # 总输出
        output = feedback_output + ff_output
        
        # 限幅
        output = max(CONTROL_LIMITS['min'], min(CONTROL_LIMITS['max'], output))
        
        # 更新反馈控制器的输出状态
        self.feedback_controller.last_output = output - ff_output
        
        return output
    
    def set_output(self, output: float):
        """
        设置输出值（用于手动/自动切换时的无扰动切换）
        
        Args:
            output: 控制输出值
        """
        self.feedback_controller.set_output(output)
    
    def get_state(self) -> dict:
        """
        获取控制器状态
        
        Returns:
            dict: 控制器状态
        """
        return {
            'feedback_controller': self.feedback_controller.get_state(),
            'feedforward_gain': self.feedforward_controller.gain
        }
