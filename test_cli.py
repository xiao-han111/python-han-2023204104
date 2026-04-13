"""命令行测试脚本"""
import sys
import os
import time

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from control.control_strategy import ControlStrategyManager
from model.two_inertia_model import TwoInertiaModel
from model.feedback_model import FeedbackModel
from model.disturbance import DisturbanceGenerator
from config import SAMPLE_TIME

print("=== PID温度控制仿真系统 - 命令行测试 ===")

# 初始化模型
plant_model = TwoInertiaModel()
feedback_model = FeedbackModel()
disturbance_generator = DisturbanceGenerator()

# 初始化控制器
control_strategy_manager = ControlStrategyManager()
control_strategy_manager.set_strategy('单回路PID')

# 仿真参数
setpoint = 20.0
simulation_time = 0.0
simulation_duration = 10.0  # 10秒

print("开始仿真...")
print("时间\t设定值\t过程值\t控制量\t干扰")
print("-" * 50)

while simulation_time < simulation_duration:
    # 更新干扰
    disturbance = disturbance_generator.update()
    
    # 更新被控对象
    intermediate, plant_output = plant_model.update(
        input_value=control_strategy_manager.get_output(),
        disturbance=disturbance
    )
    
    # 更新反馈环节
    feedback_output = feedback_model.update(plant_output)
    
    # 计算控制输出
    control_output = control_strategy_manager.calculate(
        setpoint=setpoint,
        process_value=feedback_output,
        inner_process_value=intermediate,
        disturbance=disturbance
    )
    
    # 打印数据
    print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{disturbance:.2f}")
    
    # 更新时间
    simulation_time += SAMPLE_TIME
    time.sleep(SAMPLE_TIME)

print("-" * 50)
print("仿真结束！")
