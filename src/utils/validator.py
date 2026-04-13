"""参数校验工具模块"""
from exception import ParameterError


def validate_pid_params(Kp: float, Ti: float, Td: float) -> bool:
    """
    验证PID参数
    
    Args:
        Kp: 比例增益
        Ti: 积分时间常数
        Td: 微分时间常数
    
    Returns:
        bool: 参数是否有效
    
    Raises:
        ParameterError: 参数无效时抛出异常
    """
    if Kp < 0:
        raise ParameterError("比例增益Kp必须大于等于0")
    
    if Ti <= 0:
        raise ParameterError("积分时间常数Ti必须大于0")
    
    if Td < 0:
        raise ParameterError("微分时间常数Td必须大于等于0")
    
    return True


def validate_plant_params(T1: float, T2: float, gain: float) -> bool:
    """
    验证被控对象参数
    
    Args:
        T1: 第一惯性环节时间常数
        T2: 第二惯性环节时间常数
        gain: 总增益
    
    Returns:
        bool: 参数是否有效
    
    Raises:
        ParameterError: 参数无效时抛出异常
    """
    if T1 <= 0:
        raise ParameterError("第一惯性环节时间常数T1必须大于0")
    
    if T2 <= 0:
        raise ParameterError("第二惯性环节时间常数T2必须大于0")
    
    if gain <= 0:
        raise ParameterError("总增益必须大于0")
    
    return True


def validate_temp_range(value: float, min_val: float, max_val: float) -> bool:
    """
    验证温度值是否在范围内
    
    Args:
        value: 温度值
        min_val: 最小值
        max_val: 最大值
    
    Returns:
        bool: 值是否在范围内
    
    Raises:
        ParameterError: 值不在范围内时抛出异常
    """
    if value < min_val or value > max_val:
        raise ParameterError(f"温度值必须在{min_val}到{max_val}之间")
    
    return True


def validate_control_output(value: float, min_val: float, max_val: float) -> bool:
    """
    验证控制输出值是否在范围内
    
    Args:
        value: 控制输出值
        min_val: 最小值
        max_val: 最大值
    
    Returns:
        bool: 值是否在范围内
    
    Raises:
        ParameterError: 值不在范围内时抛出异常
    """
    if value < min_val or value > max_val:
        raise ParameterError(f"控制输出值必须在{min_val}到{max_val}之间")
    
    return True


def validate_disturbance_params(amplitude: float, duration: float) -> bool:
    """
    验证干扰参数
    
    Args:
        amplitude: 干扰振幅
        duration: 干扰持续时间
    
    Returns:
        bool: 参数是否有效
    
    Raises:
        ParameterError: 参数无效时抛出异常
    """
    if amplitude < 0:
        raise ParameterError("干扰振幅必须大于等于0")
    
    if duration <= 0:
        raise ParameterError("干扰持续时间必须大于0")
    
    return True
