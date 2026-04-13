"""实时波形显示组件模块"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
import numpy as np
from config import DEFAULT_DISPLAY_POINTS, SAMPLE_TIME

class PlotWidget(QWidget):
    """实时波形显示组件类"""
    
    def __init__(self, parent=None):
        """
        初始化波形显示组件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
        self.init_data()
    
    def init_ui(self):
        """初始化UI"""
        # 主布局
        layout = QVBoxLayout(self)
        
        # 标题
        title_layout = QHBoxLayout()
        title_label = QLabel("实时波形")
        title_layout.addWidget(title_label)
        
        # 显示点数设置
        points_layout = QHBoxLayout()
        points_label = QLabel("显示点数:")
        self.points_spin = QSpinBox()
        self.points_spin.setRange(100, 5000)
        self.points_spin.setValue(DEFAULT_DISPLAY_POINTS)
        self.points_spin.valueChanged.connect(self.set_display_points)
        points_layout.addWidget(points_label)
        points_layout.addWidget(self.points_spin)
        points_layout.addStretch()
        
        title_layout.addLayout(points_layout)
        layout.addLayout(title_layout)
        
        # 波形图
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setAxisItems({'left': pg.AxisItem(orientation='left', pen='k')})
        self.plot_widget.setAxisItems({'bottom': pg.AxisItem(orientation='bottom', pen='k')})
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        
        # 添加图例
        self.plot_widget.addLegend()
        
        # 创建曲线
        self.curves = {
            'SV': self.plot_widget.plot(pen=pg.mkPen('r', width=2), name='设定值'),  # 红色：设定值
            'PV': self.plot_widget.plot(pen=pg.mkPen('g', width=2), name='过程值'),  # 绿色：过程值
            'u': self.plot_widget.plot(pen=pg.mkPen('b', width=2), name='控制量'),   # 蓝色：控制量
            'disturbance': self.plot_widget.plot(pen=pg.mkPen('purple', width=2, style=Qt.PenStyle.DashLine), name='干扰'),  # 紫色虚线：干扰
            'error': self.plot_widget.plot(pen=pg.mkPen('cyan', width=2, style=Qt.PenStyle.DotLine), name='误差')  # 青色点划线：误差
        }
        
        layout.addWidget(self.plot_widget)
    
    def init_data(self):
        """初始化数据"""
        self.display_points = DEFAULT_DISPLAY_POINTS
        self.time_data = np.zeros(self.display_points)
        self.data = {
            'SV': np.zeros(self.display_points),
            'PV': np.zeros(self.display_points),
            'u': np.zeros(self.display_points),
            'disturbance': np.zeros(self.display_points),
            'error': np.zeros(self.display_points)
        }
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(int(SAMPLE_TIME * 1000))
    
    def set_display_points(self, points: int):
        """
        设置显示点数
        
        Args:
            points: 显示点数
        """
        self.display_points = points
        self.time_data = np.zeros(self.display_points)
        for key in self.data:
            self.data[key] = np.zeros(self.display_points)
    
    def add_data(self, time: float, sv: float, pv: float, u: float, disturbance: float):
        """
        添加数据点
        
        Args:
            time: 时间
            sv: 设定值
            pv: 过程值
            u: 控制量
            disturbance: 干扰
        """
        # 计算误差
        error = sv - pv
        
        # 数据滚动
        self.time_data = np.roll(self.time_data, -1)
        self.time_data[-1] = time
        
        self.data['SV'] = np.roll(self.data['SV'], -1)
        self.data['SV'][-1] = sv
        
        self.data['PV'] = np.roll(self.data['PV'], -1)
        self.data['PV'][-1] = pv
        
        self.data['u'] = np.roll(self.data['u'], -1)
        self.data['u'][-1] = u
        
        self.data['disturbance'] = np.roll(self.data['disturbance'], -1)
        self.data['disturbance'][-1] = disturbance
        
        self.data['error'] = np.roll(self.data['error'], -1)
        self.data['error'][-1] = error
    
    def update_plot(self):
        """更新波形显示"""
        for key, curve in self.curves.items():
            curve.setData(self.time_data, self.data[key])
        
        # 自动调整Y轴范围
        all_data = np.concatenate([self.data[key] for key in self.data])
        if len(all_data) > 0:
            min_val = np.min(all_data)
            max_val = np.max(all_data)
            padding = (max_val - min_val) * 0.1
            if padding < 1:
                padding = 1
            self.plot_widget.setYRange(min_val - padding, max_val + padding)
    
    def clear(self):
        """清空数据"""
        self.time_data = np.zeros(self.display_points)
        for key in self.data:
            self.data[key] = np.zeros(self.display_points)
        self.update_plot()

class HistoryPlotWidget(QWidget):
    """历史曲线显示组件类"""
    
    def __init__(self, parent=None):
        """
        初始化历史曲线显示组件
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 主布局
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("历史曲线")
        layout.addWidget(title_label)
        
        # 波形图
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setAxisItems({'left': pg.AxisItem(orientation='left', pen='k')})
        self.plot_widget.setAxisItems({'bottom': pg.AxisItem(orientation='bottom', pen='k')})
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setMouseEnabled(x=True, y=True)
        self.plot_widget.setMenuEnabled(True)
        
        # 添加图例
        self.plot_widget.addLegend()
        
        # 创建曲线
        self.curves = {
            'SV': self.plot_widget.plot(pen=pg.mkPen('r', width=2), name='设定值'),  # 红色：设定值
            'PV': self.plot_widget.plot(pen=pg.mkPen('g', width=2), name='过程值'),  # 绿色：过程值
            'u': self.plot_widget.plot(pen=pg.mkPen('b', width=2), name='控制量'),   # 蓝色：控制量
            'disturbance': self.plot_widget.plot(pen=pg.mkPen('purple', width=2, style=Qt.PenStyle.DashLine), name='干扰')  # 紫色虚线：干扰
        }
        
        layout.addWidget(self.plot_widget)
    
    def set_data(self, time_data: list, sv_data: list, pv_data: list, u_data: list, disturbance_data: list):
        """
        设置历史数据
        
        Args:
            time_data: 时间数据
            sv_data: 设定值数据
            pv_data: 过程值数据
            u_data: 控制量数据
            disturbance_data: 干扰数据
        """
        self.curves['SV'].setData(time_data, sv_data)
        self.curves['PV'].setData(time_data, pv_data)
        self.curves['u'].setData(time_data, u_data)
        self.curves['disturbance'].setData(time_data, disturbance_data)
        
        # 自动调整Y轴范围
        all_data = sv_data + pv_data + u_data + disturbance_data
        if all_data:
            min_val = min(all_data)
            max_val = max(all_data)
            padding = (max_val - min_val) * 0.1
            if padding < 1:
                padding = 1
            self.plot_widget.setYRange(min_val - padding, max_val + padding)
    
    def clear(self):
        """清空数据"""
        for curve in self.curves.values():
            curve.setData([], [])
