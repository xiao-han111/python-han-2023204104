"""控制策略管理器模块"""
from control.pid_controller import PIDController
from control.cascade_control import CascadeController
from control.feedforward_control import FeedforwardFeedbackController
from config import DEFAULT_PID_PARAMS, CONTROL_LIMITS

class ControlStrategyManager:
    """控制策略管理器类"""
    
    def __init__(self):
        """初始化控制策略管理器"""
        # 控制策略列表
        self.strategies = {
            '普通PID(无限幅)': self._create_simple_pid,
            '单回路PID': self._create_single_loop_pid,
            '前馈+反馈': self._create_ff_feedback,
            '串级PID': self._create_cascade,
            '串级+前馈': self._create_cascade_ff
        }
        
        # 当前策略
        self.current_strategy = None
        self.current_controller = None
        
        # 手动/自动模式
        self.mode = '自动'  # '自动' 或 '手动'
        self.manual_output = 0.0
        
        # 控制器实例
        self.controllers = {
            '普通PID(无限幅)': None,
            '单回路PID': None,
            '前馈+反馈': None,
            '串级PID': None,
            '串级+前馈': None
        }
    
    def _create_simple_pid(self):
        """创建普通PID控制器（无限幅）"""
        return PIDController(
            Kp=DEFAULT_PID_PARAMS['single']['Kp'],
            Ti=DEFAULT_PID_PARAMS['single']['Ti'],
            Td=DEFAULT_PID_PARAMS['single']['Td'],
            anti_windup=False,
            limits=(float('-inf'), float('inf'))
        )
    
    def _create_single_loop_pid(self):
        """创建单回路PID控制器（带抗饱和）"""
        return PIDController(
            Kp=DEFAULT_PID_PARAMS['single']['Kp'],
            Ti=DEFAULT_PID_PARAMS['single']['Ti'],
            Td=DEFAULT_PID_PARAMS['single']['Td'],
            anti_windup=True,
            limits=(CONTROL_LIMITS['min'], CONTROL_LIMITS['max'])
        )
    
    def _create_ff_feedback(self):
        """创建前馈+反馈控制器"""
        return FeedforwardFeedbackController(
            Kp=DEFAULT_PID_PARAMS['single']['Kp'],
            Ti=DEFAULT_PID_PARAMS['single']['Ti'],
            Td=DEFAULT_PID_PARAMS['single']['Td']
        )
    
    def _create_cascade(self):
        """创建串级PID控制器"""
        return CascadeController(
            outer_kp=DEFAULT_PID_PARAMS['cascade_outer']['Kp'],
            outer_ti=DEFAULT_PID_PARAMS['cascade_outer']['Ti'],
            outer_td=DEFAULT_PID_PARAMS['cascade_outer']['Td'],
            inner_kp=DEFAULT_PID_PARAMS['cascade_inner']['Kp'],
            inner_ti=DEFAULT_PID_PARAMS['cascade_inner']['Ti'],
            inner_td=DEFAULT_PID_PARAMS['cascade_inner']['Td']
        )
    
    def _create_cascade_ff(self):
        """创建串级+前馈控制器"""
        # 串级控制器基础上添加前馈功能
        from control.feedforward_control import FeedforwardController
        controller = CascadeController(
            outer_kp=DEFAULT_PID_PARAMS['cascade_outer']['Kp'],
            outer_ti=DEFAULT_PID_PARAMS['cascade_outer']['Ti'],
            outer_td=DEFAULT_PID_PARAMS['cascade_outer']['Td'],
            inner_kp=DEFAULT_PID_PARAMS['cascade_inner']['Kp'],
            inner_ti=DEFAULT_PID_PARAMS['cascade_inner']['Ti'],
            inner_td=DEFAULT_PID_PARAMS['cascade_inner']['Td']
        )
        # 添加前馈控制器
        controller.feedforward_controller = FeedforwardController()
        return controller
    
    def set_strategy(self, strategy_name: str):
        """
        设置控制策略
        
        Args:
            strategy_name: 策略名称
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"未知的控制策略: {strategy_name}")
        
        # 保存当前输出值，用于无扰动切换
        current_output = self.get_output()
        
        # 创建或获取控制器
        if self.controllers[strategy_name] is None:
            self.controllers[strategy_name] = self.strategies[strategy_name]()
        
        # 切换到新策略
        self.current_strategy = strategy_name
        self.current_controller = self.controllers[strategy_name]
        
        # 无扰动切换
        if current_output is not None:
            self.current_controller.set_output(current_output)
    
    def set_mode(self, mode: str, manual_output: float = None):
        """
        设置控制模式
        
        Args:
            mode: 控制模式，'自动'或'手动'
            manual_output: 手动输出值
        """
        if mode not in ['自动', '手动']:
            raise ValueError("控制模式必须是'自动'或'手动'")
        
        # 从自动切换到手动时，保存当前输出值
        if self.mode == '自动' and mode == '手动':
            if manual_output is None:
                # 使用当前自动输出作为手动输出
                manual_output = self.get_output() or 0.0
            self.manual_output = manual_output
        
        # 从手动切换到自动时，设置控制器输出为当前手动输出
        elif self.mode == '手动' and mode == '自动' and self.current_controller:
            self.current_controller.set_output(self.manual_output)
        
        self.mode = mode
    
    def set_manual_output(self, output: float):
        """
        设置手动输出值
        
        Args:
            output: 手动输出值
        """
        self.manual_output = output
    
    def set_pid_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        if self.current_controller:
            if hasattr(self.current_controller, 'set_parameters'):
                self.current_controller.set_parameters(Kp, Ti, Td)
    
    def set_cascade_outer_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置串级控制器外环PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        if self.current_controller and hasattr(self.current_controller, 'set_outer_parameters'):
            self.current_controller.set_outer_parameters(Kp, Ti, Td)
    
    def set_cascade_inner_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置串级控制器内环PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        if self.current_controller and hasattr(self.current_controller, 'set_inner_parameters'):
            self.current_controller.set_inner_parameters(Kp, Ti, Td)
    
    def calculate(self, setpoint: float, process_value: float, inner_process_value: float = None, disturbance: float = 0.0) -> float:
        """
        计算控制输出
        
        Args:
            setpoint: 设定值
            process_value: 过程值
            inner_process_value: 内环过程值（串级控制用）
            disturbance: 干扰信号（前馈控制用）
        
        Returns:
            float: 控制输出
        """
        if self.mode == '手动':
            return self.manual_output
        
        if not self.current_controller:
            return 0.0
        
        # 根据不同策略调用不同的计算方法
        if self.current_strategy in ['普通PID(无限幅)', '单回路PID']:
            return self.current_controller.calculate(setpoint, process_value)
        elif self.current_strategy == '前馈+反馈':
            return self.current_controller.calculate(setpoint, process_value, disturbance)
        elif self.current_strategy == '串级PID':
            return self.current_controller.calculate(setpoint, process_value, inner_process_value)
        elif self.current_strategy == '串级+前馈':
            # 串级+前馈：先计算串级输出，再加上前馈补偿
            cascade_output = self.current_controller.calculate(setpoint, process_value, inner_process_value)
            ff_output = self.current_controller.feedforward_controller.calculate(disturbance)
            output = cascade_output + ff_output
            # 限幅
            return max(CONTROL_LIMITS['min'], min(CONTROL_LIMITS['max'], output))
        
        return 0.0
    
    def get_output(self) -> float:
        """
        获取当前控制输出
        
        Returns:
            float: 控制输出
        """
        if self.mode == '手动':
            return self.manual_output
        
        if self.current_controller:
            if hasattr(self.current_controller, 'last_output'):
                return self.current_controller.last_output
            elif hasattr(self.current_controller, 'inner_controller'):
                return self.current_controller.inner_controller.last_output
        
        return 0.0
    
    def reset(self):
        """重置所有控制器状态"""
        for strategy in self.controllers:
            if self.controllers[strategy]:
                if hasattr(self.controllers[strategy], 'reset'):
                    self.controllers[strategy].reset()
        
        self.manual_output = 0.0
    
    def set_pid_parameters(self, Kp: float, Ti: float, Td: float, controller_type: str = 'single'):
        """
        设置PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
            controller_type: 控制器类型，'single'或'cascade_outer'或'cascade_inner'
        """
        if self.current_controller:
            if controller_type == 'single' or self.current_strategy in ['普通PID(无限幅)', '单回路PID', '前馈+反馈']:
                if hasattr(self.current_controller, 'set_parameters'):
                    self.current_controller.set_parameters(Kp, Ti, Td)
            elif controller_type == 'cascade_outer' and hasattr(self.current_controller, 'set_outer_parameters'):
                self.current_controller.set_outer_parameters(Kp, Ti, Td)
            elif controller_type == 'cascade_inner' and hasattr(self.current_controller, 'set_inner_parameters'):
                self.current_controller.set_inner_parameters(Kp, Ti, Td)
    
    def get_strategy_names(self) -> list:
        """
        获取所有策略名称
        
        Returns:
            list: 策略名称列表
        """
        return list(self.strategies.keys())
