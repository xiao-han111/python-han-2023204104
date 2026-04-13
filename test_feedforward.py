#!/usr/bin/env python3
"""
测试前馈+反馈控制策略的效果
"""

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

def test_control_strategy(strategy_name):
    """测试指定的控制策略"""
    print(f"\n=== 测试 {strategy_name} 控制策略 ===")
    
    # 初始化模型
    plant_model = TwoInertiaModel()
    feedback_model = FeedbackModel()
    
    # 初始化控制策略管理器
    control_strategy_manager = ControlStrategyManager()
    control_strategy_manager.set_strategy(strategy_name)
    control_strategy_manager.set_mode('自动')
    
    # 设定值
    setpoint = 20.0
    
    # 仿真时间
    simulation_time = 0.0
    max_time = 30.0
    
    # 数据记录
    data = []
    
    # 干扰信号
    from model.disturbance import SquareWaveDisturbance
    disturbance_generator = SquareWaveDisturbance(amplitude=5.0, duration=5.0)
    disturbance_generator.start()
    
    print("时间\t设定值\t过程值\t控制量\t干扰")
    print("=" * 60)
    
    while simulation_time < max_time:
        # 更新干扰
        disturbance = disturbance_generator.update()
        
        # 获取当前反馈输出
        feedback_output = feedback_model.update(plant_model.inertia2.output)
        
        # 计算控制输出
        control_output = control_strategy_manager.calculate(
            setpoint=setpoint,
            process_value=feedback_output,
            inner_process_value=plant_model.inertia1.output,
            disturbance=disturbance
        )
        
        # 更新被控对象
        intermediate, plant_output = plant_model.update(
            input_value=control_output,
            disturbance=disturbance
        )
        
        # 记录数据
        data.append([simulation_time, setpoint, feedback_output, control_output, disturbance])
        
        # 打印数据（每1秒打印一次）
        if int(simulation_time) != int(simulation_time - SAMPLE_TIME):
            print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{disturbance:.2f}")
        
        # 更新时间
        simulation_time += SAMPLE_TIME
    
    # 计算稳态误差
    final_pv = data[-1][2]
    steady_state_error = abs(setpoint - final_pv)
    print(f"\n稳态误差: {steady_state_error:.2f}")
    
    return data

def main():
    """主函数"""
    # 测试不同控制策略
    strategies = [
        '单回路PID',
        '前馈+反馈',
        '串级PID',
        '串级+前馈'
    ]
    
    for strategy in strategies:
        test_control_strategy(strategy)

if __name__ == "__main__":
    main()
