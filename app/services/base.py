"""基础计算器基类，提供统一的参数验证方法。"""
from typing import Dict, Any, Optional


class CalculatorError(ValueError):
    """计算器业务逻辑错误，继承自 ValueError。"""
    pass


class BaseCalculator:
    """基础计算器类，提供统一的参数验证方法。"""
    
    @staticmethod
    def require_positive(params: Dict[str, Any], key: str, error_msg: Optional[str] = None) -> float:
        """
        要求参数为正数
        
        Args:
            params: 参数字典
            key: 参数键
            error_msg: 自定义错误消息，如果为None则使用默认消息
            
        Returns:
            float: 参数值
            
        Raises:
            CalculatorError: 如果参数不存在或小于等于0
        """
        value = params.get(key)
        if value is None or value <= 0:
            if error_msg is None:
                error_msg = f"{key}必须大于0"
            raise CalculatorError(error_msg)
        return float(value)
    
    @staticmethod
    def require_non_negative(params: Dict[str, Any], key: str, error_msg: Optional[str] = None) -> float:
        """
        要求参数为非负数
        
        Args:
            params: 参数字典
            key: 参数键
            error_msg: 自定义错误消息，如果为None则使用默认消息
            
        Returns:
            float: 参数值
            
        Raises:
            CalculatorError: 如果参数不存在或小于0
        """
        value = params.get(key)
        if value is None or value < 0:
            if error_msg is None:
                error_msg = f"{key}必须大于等于0"
            raise CalculatorError(error_msg)
        return float(value)
    
    @staticmethod
    def require_between(
        params: Dict[str, Any], 
        key: str, 
        error_msg: Optional[str] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        inclusive_min: bool = True,
        inclusive_max: bool = False
    ) -> float:
        """
        要求参数在指定范围内
        
        Args:
            params: 参数字典
            key: 参数键
            error_msg: 自定义错误消息，如果为None则使用默认消息
            min_value: 最小值
            max_value: 最大值
            inclusive_min: 是否包含最小值（默认True）
            inclusive_max: 是否包含最大值（默认False）
            
        Returns:
            float: 参数值
            
        Raises:
            CalculatorError: 如果参数不在指定范围内
        """
        value = params.get(key)
        if value is None:
            if error_msg is None:
                error_msg = f"{key}不能为空"
            raise CalculatorError(error_msg)
        
        value = float(value)
        
        if min_value is not None:
            if inclusive_min:
                if value < min_value:
                    if error_msg is None:
                        error_msg = f"{key}必须大于等于{min_value}"
                    raise CalculatorError(error_msg)
            else:
                if value <= min_value:
                    if error_msg is None:
                        error_msg = f"{key}必须大于{min_value}"
                    raise CalculatorError(error_msg)
        
        if max_value is not None:
            if inclusive_max:
                if value > max_value:
                    if error_msg is None:
                        error_msg = f"{key}必须小于等于{max_value}"
                    raise CalculatorError(error_msg)
            else:
                if value >= max_value:
                    if error_msg is None:
                        error_msg = f"{key}必须小于{max_value}"
                    raise CalculatorError(error_msg)
        
        return value
    
    @staticmethod
    def require_all(params: Dict[str, Any], keys: list[str], error_msg: Optional[str] = None) -> Dict[str, Any]:
        """
        要求所有指定的参数都存在且不为None
        
        Args:
            params: 参数字典
            keys: 必需的参数键列表
            error_msg: 自定义错误消息，如果为None则使用默认消息
            
        Returns:
            Dict[str, Any]: 包含所有必需参数的字典
            
        Raises:
            CalculatorError: 如果任何必需参数缺失
        """
        missing = [key for key in keys if params.get(key) is None]
        if missing:
            if error_msg is None:
                error_msg = f"缺少必需参数: {', '.join(missing)}"
            raise CalculatorError(error_msg)
        return {key: params[key] for key in keys}

