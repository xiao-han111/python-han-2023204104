"""串级控制器模块"""
from control.pid_controller import PIDController
from config import CONTROL_LIMITS

class CascadeController:
    """串级控制器类"""
    
    def __init__(self, 
                 outer_kp: float = 2.0, outer_ti: float = 2.0, outer_td: float = 0.5, 
                 inner_kp: float = 1.0, inner_ti: float = 2.0, inner_td: float = 0.0):
        """
        初始化串级控制器
        
        Args:
            outer_kp: 外环比例增益
            outer_ti: 外环积分时间常数
            outer_td: 外环微分时间常数
            inner_kp: 内环比例增益
            inner_ti: 内环积分时间常数
            inner_td: 内环微分时间常数
        """
        # 外环控制器（控制最终输出）
        self.outer_controller = PIDController(
            Kp=outer_kp,
            Ti=outer_ti,
            Td=outer_td,
            anti_windup=True,
            limits=(CONTROL_LIMITS['min'], CONTROL_LIMITS['max'])  # 使用与内环相同的范围
        )
        
        # 内环控制器（控制中间变量）
        self.inner_controller = PIDController(
            Kp=inner_kp,
            Ti=inner_ti,
            Td=inner_td,
            anti_windup=True,
            limits=(CONTROL_LIMITS['min'], CONTROL_LIMITS['max'])
        )
    
    def reset(self):
        """重置控制器状态"""
        self.outer_controller.reset()
        self.inner_controller.reset()
    
    def set_outer_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置外环PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        self.outer_controller.set_parameters(Kp, Ti, Td)
    
    def set_inner_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置内环PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        self.inner_controller.set_parameters(Kp, Ti, Td)
    
    def calculate(self, setpoint: float, process_value: float, inner_process_value: float) -> float:
        """
        计算控制输出
        
        Args:
            setpoint: 外环设定值
            process_value: 外环过程值（最终输出）
            inner_process_value: 内环过程值（中间变量）
        
        Returns:
            float: 控制输出
        """
        # 外环计算（得到内环设定值）
        inner_setpoint = self.outer_controller.calculate(setpoint, process_value)
        
        # 内环计算（得到最终控制输出）
        output = self.inner_controller.calculate(inner_setpoint, inner_process_value)
        
        return output
    
    def set_output(self, output: float):
        """
        设置输出值（用于手动/自动切换时的无扰动切换）
        
        Args:
            output: 控制输出值
        """
        self.inner_controller.set_output(output)
    
    def get_state(self) -> dict:
        """
        获取控制器状态
        
        Returns:
            dict: 控制器状态
        """
        return {
            'outer_controller': self.outer_controller.get_state(),
            'inner_controller': self.inner_controller.get_state()
        }
