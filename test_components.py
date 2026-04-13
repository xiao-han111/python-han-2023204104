"""组件测试脚本"""
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

print("=== 组件测试开始 ===")

# 测试1: 导入config
print("测试1: 导入config模块...")
try:
    from config import DEFAULT_PID_PARAMS, CONTROL_STRATEGIES
    print("OK: config模块导入成功")
    print(f"  - 控制策略: {CONTROL_STRATEGIES}")
except Exception as e:
    print(f"ERROR: config模块导入失败: {e}")

# 测试2: 导入控制模块
print("\n测试2: 导入控制模块...")
try:
    from control.pid_controller import PIDController
    from control.control_strategy import ControlStrategyManager
    print("OK: 控制模块导入成功")
    # 测试控制器初始化
    controller = PIDController()
    print("OK: PID控制器初始化成功")
    strategy_manager = ControlStrategyManager()
    print("OK: 控制策略管理器初始化成功")
except Exception as e:
    print(f"ERROR: 控制模块导入失败: {e}")

# 测试3: 导入模型模块
print("\n测试3: 导入模型模块...")
try:
    from model.two_inertia_model import TwoInertiaModel
    from model.feedback_model import FeedbackModel
    from model.disturbance import DisturbanceGenerator
    print("OK: 模型模块导入成功")
    # 测试模型初始化
    plant_model = TwoInertiaModel()
    print("OK: 双惯性模型初始化成功")
    feedback_model = FeedbackModel()
    print("OK: 反馈模型初始化成功")
    disturbance_generator = DisturbanceGenerator()
    print("OK: 干扰生成器初始化成功")
except Exception as e:
    print(f"ERROR: 模型模块导入失败: {e}")

# 测试4: 导入工具模块
print("\n测试4: 导入工具模块...")
try:
    from utils.data_logger import data_logger
    from utils.logger import get_logger
    print("OK: 工具模块导入成功")
    # 测试工具初始化
    logger = get_logger()
    print("OK: 日志工具初始化成功")
    data_logger.start_session()
    print("OK: 数据记录器初始化成功")
except Exception as e:
    print(f"ERROR: 工具模块导入失败: {e}")

# 测试5: 导入用户模块
print("\n测试5: 导入用户模块...")
try:
    from user.user_manager import user_manager
    print("OK: 用户模块导入成功")
    # 测试用户管理器
    users = user_manager.get_all_users()
    print(f"OK: 用户管理器初始化成功，用户数: {len(users)}")
except Exception as e:
    print(f"ERROR: 用户模块导入失败: {e}")

# 测试6: 导入UI模块（不含PyQt）
print("\n测试6: 导入UI模块...")
try:
    from ui.widgets import PIDParamGroup
    print("OK: UI模块导入成功")
except Exception as e:
    print(f"ERROR: UI模块导入失败: {e}")

print("\n=== 组件测试结束 ===")
