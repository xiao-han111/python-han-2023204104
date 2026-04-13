#!/usr/bin/env python3
"""
详细测试前馈+反馈控制策略的效果
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.abspath('./src'))

from control.control_strategy import ControlStrategyManager
from model.two_inertia_model import TwoInertiaModel
from model.feedback_model import FeedbackModel
from model.disturbance import SquareWaveDisturbance
from config import SAMPLE_TIME, FF_GAIN

def test_feedforward_feedback():
    """测试前馈+反馈控制策略"""
    print("=== 测试前馈+反馈控制策略 ===")
    print(f"前馈增益: {FF_GAIN}")
    
    # 初始化模型
    plant_model = TwoInertiaModel()
    feedback_model = FeedbackModel()
    
    # 初始化控制策略管理器
    control_strategy_manager = ControlStrategyManager()
    control_strategy_manager.set_strategy('前馈+反馈')
    control_strategy_manager.set_mode('自动')
    
    # 设定值
    setpoint = 20.0
    
    # 仿真时间
    simulation_time = 0.0
    max_time = 30.0
    
    # 干扰信号
    disturbance_generator = SquareWaveDisturbance(amplitude=5.0, duration=5.0)
    disturbance_generator.start()
    
    print("时间\t设定值\t过程值\t控制量\t前馈值\t干扰")
    print("=" * 80)
    
    # 保存前馈控制器引用
    ff_controller = control_strategy_manager.current_controller.feedforward_controller
    
    while simulation_time < max_time:
        # 更新干扰
        disturbance = disturbance_generator.update()
        
        # 计算前馈值
        ff_value = ff_controller.calculate(disturbance)
        
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
            print(f"{simulation_time:.1f}\t{setpoint:.2f}\t{feedback_output:.2f}\t{control_output:.2f}\t{ff_value:.2f}\t{disturbance:.2f}")
        
        # 更新时间
        simulation_time += SAMPLE_TIME
    
    # 计算稳态误差
    final_pv = feedback_output
    steady_state_error = abs(setpoint - final_pv)
    print(f"\n稳态误差: {steady_state_error:.2f}")

def main():
    """主函数"""
    test_feedforward_feedback()

if __name__ == "__main__":
    main()
