"""自定义控件模块"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDoubleSpinBox, QGroupBox, QGridLayout, QComboBox, QStatusBar, QButtonGroup
from PyQt5.QtCore import Qt
from config import DEFAULT_PID_PARAMS, CONTROL_STRATEGIES, TEMP_RANGE, CONTROL_LIMITS

class PIDParamGroup(QGroupBox):
    """PID参数面板类"""
    
    def __init__(self, title: str, parent=None):
        """
        初始化PID参数面板
        
        Args:
            title: 面板标题
            parent: 父控件
        """
        super().__init__(title, parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QGridLayout(self)
        
        # Kp
        layout.addWidget(QLabel("Kp:"), 0, 0)
        self.kp_spin = QDoubleSpinBox()
        self.kp_spin.setRange(0, 100)
        self.kp_spin.setSingleStep(0.1)
        self.kp_spin.setValue(DEFAULT_PID_PARAMS['single']['Kp'])
        layout.addWidget(self.kp_spin, 0, 1)
        
        # Ti
        layout.addWidget(QLabel("Ti:"), 1, 0)
        self.ti_spin = QDoubleSpinBox()
        self.ti_spin.setRange(0.1, 100)
        self.ti_spin.setSingleStep(0.1)
        self.ti_spin.setValue(DEFAULT_PID_PARAMS['single']['Ti'])
        layout.addWidget(self.ti_spin, 1, 1)
        
        # Td
        layout.addWidget(QLabel("Td:"), 2, 0)
        self.td_spin = QDoubleSpinBox()
        self.td_spin.setRange(0, 100)
        self.td_spin.setSingleStep(0.1)
        self.td_spin.setValue(DEFAULT_PID_PARAMS['single']['Td'])
        layout.addWidget(self.td_spin, 2, 1)
    
    def get_parameters(self) -> dict:
        """
        获取PID参数
        
        Returns:
            dict: PID参数
        """
        return {
            'Kp': self.kp_spin.value(),
            'Ti': self.ti_spin.value(),
            'Td': self.td_spin.value()
        }
    
    def set_parameters(self, Kp: float, Ti: float, Td: float):
        """
        设置PID参数
        
        Args:
            Kp: 比例增益
            Ti: 积分时间常数
            Td: 微分时间常数
        """
        self.kp_spin.setValue(Kp)
        self.ti_spin.setValue(Ti)
        self.td_spin.setValue(Td)

class ControlStrategyWidget(QWidget):
    """控制策略选择控件类"""
    
    def __init__(self, parent=None):
        """
        初始化控制策略选择控件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        
        layout.addWidget(QLabel("控制策略:"))
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(CONTROL_STRATEGIES)
        layout.addWidget(self.strategy_combo)
        layout.addStretch()
    
    def get_strategy(self) -> str:
        """
        获取当前选择的控制策略
        
        Returns:
            str: 控制策略名称
        """
        return self.strategy_combo.currentText()
    
    def set_strategy(self, strategy: str):
        """
        设置控制策略
        
        Args:
            strategy: 控制策略名称
        """
        index = self.strategy_combo.findText(strategy)
        if index >= 0:
            self.strategy_combo.setCurrentIndex(index)

class ModeControlWidget(QWidget):
    """控制模式选择控件类"""
    
    def __init__(self, parent=None):
        """
        初始化控制模式选择控件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        
        layout.addWidget(QLabel("控制模式:"))
        self.auto_btn = QPushButton("自动")
        self.auto_btn.setCheckable(True)
        self.auto_btn.setChecked(True)
        self.manual_btn = QPushButton("手动")
        self.manual_btn.setCheckable(True)
        
        # 按钮组
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.auto_btn)
        self.button_group.addButton(self.manual_btn)
        
        layout.addWidget(self.auto_btn)
        layout.addWidget(self.manual_btn)
        
        # 手动输出设置
        self.manual_output_label = QLabel("手动输出:")
        self.manual_output_spin = QDoubleSpinBox()
        self.manual_output_spin.setRange(CONTROL_LIMITS['min'], CONTROL_LIMITS['max'])
        self.manual_output_spin.setSingleStep(0.1)
        self.manual_output_spin.setValue(0)
        
        layout.addWidget(self.manual_output_label)
        layout.addWidget(self.manual_output_spin)
        layout.addStretch()
    
    def is_auto_mode(self) -> bool:
        """
        检查是否为自动模式
        
        Returns:
            bool: 是否为自动模式
        """
        return self.auto_btn.isChecked()
    
    def get_manual_output(self) -> float:
        """
        获取手动输出值
        
        Returns:
            float: 手动输出值
        """
        return self.manual_output_spin.value()
    
    def set_manual_output(self, value: float):
        """
        设置手动输出值
        
        Args:
            value: 手动输出值
        """
        self.manual_output_spin.setValue(value)

class SetpointWidget(QWidget):
    """设定值控件类"""
    
    def __init__(self, parent=None):
        """
        初始化设定值控件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        
        layout.addWidget(QLabel("设定温度 (°C):"))
        self.setpoint_spin = QDoubleSpinBox()
        self.setpoint_spin.setRange(TEMP_RANGE['min'], TEMP_RANGE['max'])
        self.setpoint_spin.setSingleStep(0.1)
        self.setpoint_spin.setValue(20)
        layout.addWidget(self.setpoint_spin)
        layout.addStretch()
    
    def get_setpoint(self) -> float:
        """
        获取设定值
        
        Returns:
            float: 设定值
        """
        return self.setpoint_spin.value()
    
    def set_setpoint(self, value: float):
        """
        设置设定值
        
        Args:
            value: 设定值
        """
        self.setpoint_spin.setValue(value)

class DisturbanceWidget(QWidget):
    """干扰信号控件类"""
    
    def __init__(self, parent=None):
        """
        初始化干扰信号控件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        
        # 干扰振幅
        layout.addWidget(QLabel("干扰振幅:"))
        self.amplitude_spin = QDoubleSpinBox()
        self.amplitude_spin.setRange(0, 10)
        self.amplitude_spin.setSingleStep(0.1)
        self.amplitude_spin.setValue(0)
        layout.addWidget(self.amplitude_spin)
        
        # 干扰持续时间
        layout.addWidget(QLabel("持续时间 (s):"))
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 60)
        self.duration_spin.setSingleStep(0.1)
        self.duration_spin.setValue(5)
        layout.addWidget(self.duration_spin)
        
        # 施加干扰按钮
        self.apply_btn = QPushButton("施加方波干扰")
        layout.addWidget(self.apply_btn)
        layout.addStretch()
    
    def get_parameters(self) -> dict:
        """
        获取干扰参数
        
        Returns:
            dict: 干扰参数
        """
        return {
            'amplitude': self.amplitude_spin.value(),
            'duration': self.duration_spin.value()
        }
    
    def set_apply_button_enabled(self, enabled: bool):
        """
        设置施加干扰按钮状态
        
        Args:
            enabled: 是否启用
        """
        self.apply_btn.setEnabled(enabled)
    
    def set_apply_button_text(self, text: str):
        """
        设置施加干扰按钮文本
        
        Args:
            text: 按钮文本
        """
        self.apply_btn.setText(text)

class StatusBar(QStatusBar):
    """自定义状态栏类"""
    
    def __init__(self, parent=None):
        """
        初始化状态栏
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 状态信息
        self.status_label = QLabel("就绪")
        self.addWidget(self.status_label)
        
        # 分隔符
        self.addPermanentWidget(QLabel(" | "))
        
        # 当前用户
        self.user_label = QLabel("用户: 未登录")
        self.addPermanentWidget(self.user_label)
    
    def set_status(self, text: str):
        """
        设置状态信息
        
        Args:
            text: 状态文本
        """
        self.status_label.setText(text)
    
    def set_user(self, username: str):
        """
        设置当前用户
        
        Args:
            username: 用户名
        """
        self.user_label.setText(f"用户: {username}")
