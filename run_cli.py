"""命令行版本的PID温度控制仿真系统"""
import sys
import os
import time

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from control.control_strategy import ControlStrategyManager
from model.two_inertia_model import TwoInertiaModel
from model.feedback_model import FeedbackModel
from model.disturbance import DisturbanceGenerator
from config import SAMPLE_TIME, CONTROL_STRATEGIES
from user.user_manager import user_manager
from utils.data_logger import data_logger

print("=== PID温度控制仿真系统 - 命令行版本 ===")

# 登录功能
def login():
    print("\n=== 登录 ===")
    print("默认账号:")
    print("  - 管理员: admin / admin123")
    print("  - 普通用户: user / user123")
    
    while True:
        user_id = input("请输入用户名: ")
        password = input("请输入密码: ")
        
        try:
            user_info = user_manager.authenticate(user_id, password)
            print(f"登录成功！欢迎，{user_id}（{user_info['role']}）")
            return user_info
        except Exception as e:
            print(f"登录失败: {e}")
            continue

# 控制策略选择
def select_strategy():
    print("\n=== 选择控制策略 ===")
    for i, strategy in enumerate(CONTROL_STRATEGIES):
        print(f"{i+1}. {strategy}")
    
    while True:
        try:
            choice = int(input("请选择控制策略（1-5）: "))
            if 1 <= choice <= len(CONTROL_STRATEGIES):
                return CONTROL_STRATEGIES[choice-1]
            else:
                print("请输入有效的选项")
        except ValueError:
            print("请输入数字")

# 仿真参数设置
def set_simulation_params():
    print("\n=== 仿真参数设置 ===")
    setpoint = float(input("请输入设定温度 (°C): "))
    duration = float(input("请输入仿真时间 (秒): "))
    return setpoint, duration

# 运行仿真
def run_simulation(user_info):
    # 选择控制策略
    strategy = select_strategy()
    
    # 设置仿真参数
    setpoint, duration = set_simulation_params()
    
    # 初始化模型
    plant_model = TwoInertiaModel()
    feedback_model = FeedbackModel()
    disturbance_generator = DisturbanceGenerator()
    
    # 初始化控制器
    control_strategy_manager = ControlStrategyManager()
    control_strategy_manager.set_strategy(strategy)
    
    # 开始数据记录
    data_logger.start_session()
    print(f"开始数据记录会话: {data_logger.current_session_id}")
    
    # 仿真参数
    simulation_time = 0.0
    
    print("\n开始仿真...")
    print("时间\t设定值\t过程值\t控制量\t干扰")
    print("-" * 50)
    
    while simulation_time < duration:
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
        
        # 记录数据
        data_logger.add_data_point(
            time=simulation_time,
            sv=setpoint,
            pv=feedback_output,
            u=control_output,
            disturbance=disturbance
        )
        
        # 打印数据
        print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{disturbance:.2f}")
        
        # 更新时间
        simulation_time += SAMPLE_TIME
        time.sleep(SAMPLE_TIME)
    
    print("-" * 50)
    print("仿真结束！")
    
    # 保存数据
    data_logger.save_session()
    print(f"数据保存成功")

# 主菜单
def main_menu(user_info):
    while True:
        print("\n=== 主菜单 ===")
        print("1. 运行仿真")
        print("2. 查看历史数据")
        print("3. 退出")
        
        try:
            choice = int(input("请选择操作（1-3）: "))
            if choice == 1:
                run_simulation(user_info)
            elif choice == 2:
                print("历史数据功能开发中...")
            elif choice == 3:
                print("退出系统")
                break
            else:
                print("请输入有效的选项")
        except ValueError:
            print("请输入数字")

if __name__ == '__main__':
    # 登录
    user_info = login()
    
    # 显示主菜单
    main_menu(user_info)
