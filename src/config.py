"""全局配置文件"""
import os
import sys

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据目录
DATA_DIR = os.path.join(BASE_DIR, 'data')
HISTORY_DATA_DIR = os.path.join(DATA_DIR, 'history_data')
USERS_DIR = os.path.join(DATA_DIR, 'users')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')

# 确保数据目录存在
for dir_path in [DATA_DIR, HISTORY_DATA_DIR, USERS_DIR, LOGS_DIR]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

# 日志文件路径
LOG_FILE = os.path.join(LOGS_DIR, 'error.log')

# 用户数据文件
USER_DATA_FILE = os.path.join(USERS_DIR, 'users.json')

# 历史数据文件模板
HISTORY_DATA_TEMPLATE = os.path.join(HISTORY_DATA_DIR, 'history_{}.json')

# 默认用户
DEFAULT_USERS = [
    {
        'id': 'admin',
        'password': 'admin123',
        'role': 'admin'
    },
    {
        'id': 'user',
        'password': 'user123',
        'role': 'user'
    }
]

# 被控对象默认参数
DEFAULT_PLANT_PARAMS = {
    'T1': 1.0,  # 第一惯性环节时间常数
    'T2': 2.0,  # 第二惯性环节时间常数
    'gain': 1.0  # 被控对象总增益
}

# PID默认参数
DEFAULT_PID_PARAMS = {
    'single': {
        'Kp': 2.0,
        'Ti': 2.0,
        'Td': 0.5
    },
    'cascade_outer': {
        'Kp': 2.0,
        'Ti': 2.0,
        'Td': 0.5
    },
    'cascade_inner': {
        'Kp': 1.0,
        'Ti': 2.0,
        'Td': 0.0
    }
}

# 控制量限制
CONTROL_LIMITS = {
    'min': -30,
    'max': 30
}

# 温度范围
TEMP_RANGE = {
    'min': 0,
    'max': 30
}

# 采样时间 (秒)
SAMPLE_TIME = 0.1

# 显示点数
DEFAULT_DISPLAY_POINTS = 1000

# 滤波器时间常数
FILTER_TC = 0.1

# 前馈增益
FF_GAIN = -0.5

# 控制策略列表
CONTROL_STRATEGIES = [
    '普通PID(无限幅)',
    '单回路PID',
    '前馈+反馈',
    '串级PID',
    '串级+前馈'
]

# 角色权限
ROLE_PERMISSIONS = {
    'admin': {
        'change_password': True,
        'manage_users': True,
        'run_simulation': True,
        'export_data': True
    },
    'user': {
        'change_password': True,
        'manage_users': False,
        'run_simulation': True,
        'export_data': True
    }
}
