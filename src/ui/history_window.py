"""历史数据窗口模块"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFileDialog
from PyQt5.QtCore import Qt
from utils.data_logger import data_logger
from utils.excel_exporter import export_to_excel, export_to_csv
from ui.plot_widget import HistoryPlotWidget
from utils.exception_handler import show_info_dialog, show_error_dialog

class HistoryWindow(QMainWindow):
    """历史数据窗口类"""
    
    def __init__(self, parent=None):
        """
        初始化历史数据窗口
        
        Args:
            parent: 父控件
        """
        super().__init__(parent)
        self.setWindowTitle("历史曲线")
        self.setMinimumSize(1000, 600)
        self.init_ui()
        self.load_history_files()
    
    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # 控制面板
        control_layout = QHBoxLayout()
        
        # 文件选择
        control_layout.addWidget(QLabel("历史文件:"))
        self.file_combo = QComboBox()
        self.file_combo.currentIndexChanged.connect(self.on_file_selected)
        control_layout.addWidget(self.file_combo)
        
        # 导出按钮
        self.export_excel_btn = QPushButton("导出Excel")
        self.export_excel_btn.clicked.connect(self.export_to_excel)
        control_layout.addWidget(self.export_excel_btn)
        
        self.export_csv_btn = QPushButton("导出CSV")
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        control_layout.addWidget(self.export_csv_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # 波形显示
        self.history_plot = HistoryPlotWidget()
        layout.addWidget(self.history_plot)
        
        # 数据表格
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["时间", "设定值", "过程值", "控制量", "干扰"])
        self.table_widget.setAlternatingRowColors(True)
        layout.addWidget(self.table_widget)
    
    def load_history_files(self):
        """加载历史文件列表"""
        files = data_logger.get_history_files()
        self.file_combo.clear()
        self.file_combo.addItems(files)
        
        if files:
            self.on_file_selected(0)
    
    def on_file_selected(self, index):
        """选择历史文件"""
        if index < 0 or index >= self.file_combo.count():
            return
        
        file_path = self.file_combo.itemText(index)
        self.load_history_data(file_path)
    
    def load_history_data(self, file_path):
        """加载历史数据"""
        data = data_logger.load_history_data(file_path)
        
        if not data:
            show_error_dialog("错误", "加载历史数据失败")
            return
        
        # 准备数据
        time_data = []
        sv_data = []
        pv_data = []
        u_data = []
        disturbance_data = []
        
        for item in data:
            time_data.append(item['time'])
            sv_data.append(item['sv'])
            pv_data.append(item['pv'])
            u_data.append(item['u'])
            disturbance_data.append(item['disturbance'])
        
        # 更新波形
        self.history_plot.set_data(time_data, sv_data, pv_data, u_data, disturbance_data)
        
        # 更新表格
        self.table_widget.setRowCount(len(data))
        for i, item in enumerate(data):
            self.table_widget.setItem(i, 0, QTableWidgetItem(f"{item['time']:.1f}"))
            self.table_widget.setItem(i, 1, QTableWidgetItem(f"{item['sv']:.2f}"))
            self.table_widget.setItem(i, 2, QTableWidgetItem(f"{item['pv']:.2f}"))
            self.table_widget.setItem(i, 3, QTableWidgetItem(f"{item['u']:.2f}"))
            self.table_widget.setItem(i, 4, QTableWidgetItem(f"{item['disturbance']:.2f}"))
        
        # 自动调整列宽
        self.table_widget.resizeColumnsToContents()
        
        # 保存当前数据
        self.current_data = data
    
    def export_to_excel(self):
        """导出到Excel"""
        if not hasattr(self, 'current_data') or not self.current_data:
            show_error_dialog("错误", "没有数据可导出")
            return
        
        try:
            file_path = export_to_excel(self.current_data)
            show_info_dialog("成功", f"数据导出成功：{file_path}")
        except Exception as e:
            show_error_dialog("错误", f"导出失败：{str(e)}")
    
    def export_to_csv(self):
        """导出到CSV"""
        if not hasattr(self, 'current_data') or not self.current_data:
            show_error_dialog("错误", "没有数据可导出")
            return
        
        try:
            file_path = export_to_csv(self.current_data)
            show_info_dialog("成功", f"数据导出成功：{file_path}")
        except Exception as e:
            show_error_dialog("错误", f"导出失败：{str(e)}")
