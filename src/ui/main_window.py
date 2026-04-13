"""主界面模块"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSplitter, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from ui.plot_widget import PlotWidget
from ui.widgets import ControlStrategyWidget, ModeControlWidget, SetpointWidget, DisturbanceWidget, PIDParamGroup, StatusBar
from control.control_strategy import ControlStrategyManager
from model.two_inertia_model import TwoInertiaModel
from model.feedback_model import FeedbackModel
from model.disturbance import DisturbanceGenerator
from utils.data_logger import data_logger
from utils.exception_handler import show_info_dialog, show_error_dialog
from utils.time_format import format_time
from config import SAMPLE_TIME, DEFAULT_PLANT_PARAMS, DEFAULT_PID_PARAMS

class MainWindow(QMainWindow):
    """主界面类"""
    
    def __init__(self, user_info, parent=None):
        """
        初始化主界面
        
        Args:
            user_info: 用户信息
            parent: 父控件
        """
        print("MainWindow: 开始初始化...")
        super().__init__(parent)
        print("MainWindow: 设置窗口属性...")
        self.setWindowTitle("PID温度控制仿真系统")
        self.setMinimumSize(800, 600)
        
        # 用户信息
        self.user_info = user_info
        print(f"MainWindow: 用户信息: {user_info}")
        
        # 初始化组件
        print("MainWindow: 初始化UI...")
        self.init_ui()
        print("MainWindow: 初始化模型...")
        self.init_models()
        print("MainWindow: 初始化控制器...")
        self.init_control()
        
        # 计时器
        print("MainWindow: 初始化计时器...")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.simulation_time = 0.0
        
        # 数据记录
        print("MainWindow: 开始数据记录会话...")
        data_logger.start_session()
        print("MainWindow: 初始化完成")
    
    def init_ui(self):
        """初始化UI"""
        # 状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.set_user(self.user_info['id'])
        self.status_bar.set_status("就绪")
        
        # 菜单栏
        menubar = self.menuBar()
        
        # 系统菜单
        system_menu = menubar.addMenu("系统")
        logout_action = system_menu.addAction("退出登录")
        logout_action.triggered.connect(self.on_logout)
        exit_action = system_menu.addAction("退出程序")
        exit_action.triggered.connect(self.close)
        
        # 功能菜单
        function_menu = menubar.addMenu("功能")
        history_action = function_menu.addAction("历史曲线")
        history_action.triggered.connect(self.open_history_window)
        
        # 用户管理菜单
        user_menu = menubar.addMenu("用户管理")
        change_pwd_action = user_menu.addAction("修改密码")
        change_pwd_action.triggered.connect(self.open_change_password_dialog)
        
        if self.user_info['role'] == 'admin':
            manage_users_action = user_menu.addAction("管理用户")
            manage_users_action.triggered.connect(self.open_user_manager_window)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = help_menu.addAction("关于软件")
        about_action.triggered.connect(self.show_about)
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # 控制策略和模式
        strategy_layout = QHBoxLayout()
        self.control_strategy_widget = ControlStrategyWidget()
        self.mode_control_widget = ModeControlWidget()
        strategy_layout.addWidget(self.control_strategy_widget)
        strategy_layout.addWidget(self.mode_control_widget)
        control_layout.addLayout(strategy_layout)
        
        # 设定值和干扰
        setpoint_layout = QHBoxLayout()
        self.setpoint_widget = SetpointWidget()
        self.disturbance_widget = DisturbanceWidget()
        setpoint_layout.addWidget(self.setpoint_widget)
        setpoint_layout.addWidget(self.disturbance_widget)
        control_layout.addLayout(setpoint_layout)
        
        # PID参数
        pid_layout = QHBoxLayout()
        
        # 单回路PID参数面板
        self.pid_param_group = PIDParamGroup("PID参数")
        
        # 串级PID参数面板
        self.cascade_param_widget = QWidget()
        cascade_layout = QVBoxLayout(self.cascade_param_widget)
        
        # 外环参数
        self.outer_pid_group = PIDParamGroup("外环参数")
        self.outer_pid_group.set_parameters(
            DEFAULT_PID_PARAMS['cascade_outer']['Kp'],
            DEFAULT_PID_PARAMS['cascade_outer']['Ti'],
            DEFAULT_PID_PARAMS['cascade_outer']['Td']
        )
        
        # 内环参数
        self.inner_pid_group = PIDParamGroup("内环参数")
        self.inner_pid_group.set_parameters(
            DEFAULT_PID_PARAMS['cascade_inner']['Kp'],
            DEFAULT_PID_PARAMS['cascade_inner']['Ti'],
            DEFAULT_PID_PARAMS['cascade_inner']['Td']
        )
        
        cascade_layout.addWidget(self.outer_pid_group)
        cascade_layout.addWidget(self.inner_pid_group)
        
        pid_layout.addWidget(self.pid_param_group)
        pid_layout.addWidget(self.cascade_param_widget)
        control_layout.addLayout(pid_layout)
        
        # 初始隐藏串级参数面板
        self.cascade_param_widget.hide()
        
        # 仿真控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始仿真")
        self.start_btn.clicked.connect(self.start_simulation)
        self.stop_btn = QPushButton("停止仿真")
        self.stop_btn.clicked.connect(self.stop_simulation)
        self.stop_btn.setEnabled(False)
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_simulation)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.reset_btn)
        control_layout.addLayout(btn_layout)
        
        # 波形显示
        self.plot_widget = PlotWidget()
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(control_panel)
        splitter.addWidget(self.plot_widget)
        splitter.setSizes([200, 400])
        
        main_layout.addWidget(splitter)
        
        # 信号连接
        self.control_strategy_widget.strategy_combo.currentTextChanged.connect(self.on_strategy_changed)
        self.disturbance_widget.apply_btn.clicked.connect(self.on_apply_disturbance)
    
    def init_models(self):
        """初始化系统模型"""
        # 被控对象模型
        self.plant_model = TwoInertiaModel(
            T1=DEFAULT_PLANT_PARAMS['T1'],
            T2=DEFAULT_PLANT_PARAMS['T2'],
            gain=DEFAULT_PLANT_PARAMS['gain']
        )
        
        # 反馈环节模型
        self.feedback_model = FeedbackModel()
        
        # 干扰信号生成器
        self.disturbance_generator = DisturbanceGenerator()
    
    def init_control(self):
        """初始化控制器"""
        self.control_strategy_manager = ControlStrategyManager()
        # 默认策略
        self.control_strategy_manager.set_strategy('单回路PID')
    
    def start_simulation(self):
        """开始仿真"""
        self.timer.start(int(SAMPLE_TIME * 1000))
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_bar.set_status("仿真中...")
    
    def stop_simulation(self):
        """停止仿真"""
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_bar.set_status("已停止")
        
        # 保存数据
        data_logger.save_session()
    
    def reset_simulation(self):
        """重置仿真"""
        # 停止仿真
        self.stop_simulation()
        
        # 重置模型
        self.plant_model.reset()
        self.feedback_model.reset()
        self.disturbance_generator.reset()
        
        # 重置控制器
        self.control_strategy_manager.reset()
        
        # 重置波形
        self.plot_widget.clear()
        
        # 重置时间
        self.simulation_time = 0.0
        
        # 重置数据记录
        data_logger.start_session()
        
        self.status_bar.set_status("已重置")
    
    def update_simulation(self):
        """更新仿真"""
        # 获取设定值
        setpoint = self.setpoint_widget.get_setpoint()
        
        # 获取控制模式
        if self.mode_control_widget.is_auto_mode():
            self.control_strategy_manager.set_mode('自动')
        else:
            manual_output = self.mode_control_widget.get_manual_output()
            self.control_strategy_manager.set_mode('手动', manual_output)
        
        # 更新PID参数
        strategy = self.control_strategy_widget.get_strategy()
        if strategy in ['串级PID', '串级+前馈']:
            # 更新串级PID内外环参数
            outer_params = self.outer_pid_group.get_parameters()
            inner_params = self.inner_pid_group.get_parameters()
            self.control_strategy_manager.set_cascade_outer_parameters(
                outer_params['Kp'], outer_params['Ti'], outer_params['Td']
            )
            self.control_strategy_manager.set_cascade_inner_parameters(
                inner_params['Kp'], inner_params['Ti'], inner_params['Td']
            )
        else:
            # 更新单回路PID参数
            params = self.pid_param_group.get_parameters()
            self.control_strategy_manager.set_pid_parameters(
                params['Kp'], params['Ti'], params['Td']
            )
        
        # 更新干扰
        disturbance = self.disturbance_generator.update()
        
        # 获取当前被控对象输出
        current_plant_output = self.plant_model.inertia2.output
        
        # 更新反馈环节
        feedback_output = self.feedback_model.update(current_plant_output)
        
        # 计算控制输出
        control_output = self.control_strategy_manager.calculate(
            setpoint=setpoint,
            process_value=feedback_output,
            inner_process_value=self.plant_model.inertia1.output,
            disturbance=disturbance
        )
        
        # 更新被控对象
        intermediate, plant_output = self.plant_model.update(
            input_value=control_output,
            disturbance=disturbance
        )
        
        # 更新反馈环节（使用更新后的被控对象输出）
        updated_feedback_output = self.feedback_model.update(plant_output)
        
        # 记录数据
        data_logger.add_data_point(
            time=self.simulation_time,
            sv=setpoint,
            pv=updated_feedback_output,
            u=control_output,
            disturbance=disturbance
        )
        
        # 更新波形
        self.plot_widget.add_data(
            time=self.simulation_time,
            sv=setpoint,
            pv=updated_feedback_output,
            u=control_output,
            disturbance=disturbance
        )
        
        # 更新时间
        self.simulation_time += SAMPLE_TIME
    
    def on_strategy_changed(self, strategy):
        """控制策略变更"""
        self.control_strategy_manager.set_strategy(strategy)
        
        # 根据策略类型显示不同的参数面板
        if strategy in ['串级PID', '串级+前馈']:
            # 显示串级参数面板
            self.pid_param_group.hide()
            self.cascade_param_widget.show()
        else:
            # 显示单回路PID参数面板
            self.pid_param_group.show()
            self.cascade_param_widget.hide()
    
    def on_apply_disturbance(self):
        """施加干扰"""
        params = self.disturbance_widget.get_parameters()
        amplitude = params['amplitude']
        duration = params['duration']
        
        # 设置干扰参数
        self.disturbance_generator.set_square_wave_parameters(amplitude, duration)
        # 开始干扰
        self.disturbance_generator.start_square_wave()
        
        # 禁用按钮
        self.disturbance_widget.set_apply_button_enabled(False)
        
        # 启动倒计时
        self.disturbance_timer = QTimer(self)
        self.disturbance_timer.timeout.connect(self.update_disturbance_countdown)
        self.disturbance_timer.start(100)
        self.disturbance_remaining = duration
    
    def update_disturbance_countdown(self):
        """更新干扰倒计时"""
        self.disturbance_remaining -= 0.1
        if self.disturbance_remaining <= 0:
            self.disturbance_timer.stop()
            self.disturbance_widget.set_apply_button_enabled(True)
            self.disturbance_widget.set_apply_button_text("施加方波干扰")
        else:
            self.disturbance_widget.set_apply_button_text(f"干扰中... ({self.disturbance_remaining:.1f}s)")
    
    def open_history_window(self):
        """打开历史数据窗口"""
        from ui.history_window import HistoryWindow
        history_window = HistoryWindow(self)
        history_window.show()
    
    def open_change_password_dialog(self):
        """打开修改密码对话框"""
        from ui.change_pwd_ui import ChangePasswordDialog
        dialog = ChangePasswordDialog(self.user_info['id'], self)
        dialog.exec()
    
    def open_user_manager_window(self):
        """打开用户管理窗口"""
        from ui.user_manager_ui import UserManagerWindow
        window = UserManagerWindow(self)
        window.show()
    
    def on_logout(self):
        """退出登录"""
        # 停止仿真
        self.stop_simulation()
        
        # 关闭主窗口
        self.close()
        
        # 打开登录窗口
        from ui.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.set_login_success_callback(self.on_login_success)
        login_window.show()
    
    def on_login_success(self, user_info):
        """登录成功回调"""
        # 更新用户信息
        self.user_info = user_info
        self.status_bar.set_user(user_info['id'])
        
        # 重新显示主窗口
        self.show()
    
    def show_about(self):
        """显示关于对话框"""
        about_text = "PID温度控制仿真系统 v1.0\n\n" \
                    "开发语言: Python 3.10+\n" \
                    "UI框架: PyQt6\n" \
                    "绘图库: pyqtgraph\n\n" \
                    "© 2024 PID温度控制仿真系统"
        show_info_dialog("关于软件", about_text)
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止仿真
        self.stop_simulation()
        event.accept()
