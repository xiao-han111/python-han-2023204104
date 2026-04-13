#!/usr/bin/env python3
"""
测试串级PID控制策略的效果和参数调整功能
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from control.control_strategy import ControlStrategyManager
from model.two_inertia_model import TwoInertiaModel
from model.feedback_model import FeedbackModel
from model.disturbance import SquareWaveDisturbance
from config import SAMPLE_TIME

def test_cascade_pid():
    """测试串级PID控制策略"""
    print("=== 测试串级PID控制策略 ===")
    
    # 初始化模型
    plant_model = TwoInertiaModel()
    feedback_model = FeedbackModel()
    
    # 初始化控制策略管理器
    control_strategy_manager = ControlStrategyManager()
    control_strategy_manager.set_strategy('串级PID')
    control_strategy_manager.set_mode('自动')
    
    # 设定值
    setpoint = 20.0
    
    # 仿真时间
    simulation_time = 0.0
    max_time = 30.0
    
    # 干扰信号
    disturbance_generator = SquareWaveDisturbance(amplitude=5.0, duration=5.0)
    disturbance_generator.start()
    
    print("时间\t设定值\t过程值\t控制量\t干扰")
    print("=" * 60)
    
    # 初始参数测试
    while simulation_time < 10.0:
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
        
        # 打印数据（每1秒打印一次）
        if int(simulation_time) != int(simulation_time - SAMPLE_TIME):
            print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{disturbance:.2f}")
        
        # 更新时间
        simulation_time += SAMPLE_TIME
    
    # 修改串级PID参数
    print("\n=== 修改串级PID参数 ===")
    print("设置外环参数: Kp=5.0, Ti=1.0, Td=0.5")
    print("设置内环参数: Kp=2.0, Ti=1.0, Td=0.0")
    control_strategy_manager.set_cascade_outer_parameters(5.0, 1.0, 0.5)
    control_strategy_manager.set_cascade_inner_parameters(2.0, 1.0, 0.0)
    
    # 继续仿真
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
        
        # 打印数据（每1秒打印一次）
        if int(simulation_time) != int(simulation_time - SAMPLE_TIME):
            print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{disturbance:.2f}")
        
        # 更新时间
        simulation_time += SAMPLE_TIME
    
    # 计算稳态误差
    final_pv = feedback_output
    steady_state_error = abs(setpoint - final_pv)
    print(f"\n稳态误差: {steady_state_error:.2f}")

def main():
    """主函数"""
    test_cascade_pid()

if __name__ == "__main__":
    main()
