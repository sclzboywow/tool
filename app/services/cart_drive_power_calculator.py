"""
小车驱动电机功率计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class CartDrivePowerCalculator:
    """小车驱动电机功率计算器"""
    
    SCENARIO_NAMES = {
        "cart_drive_power": "小车驱动电机功率计算",
        "traction_force": "牵引力计算",
        "motor_power": "电机功率计算",
        "power_boost": "功率提升版本计算"
    }
    
    # 常数
    G = 10  # 重力加速度 m/s² (Excel中使用10)
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算小车驱动电机功率
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "cart_drive_power":
            return self._calculate_cart_drive_power(params)
        elif scenario == "traction_force":
            return self._calculate_traction_force(params)
        elif scenario == "motor_power":
            return self._calculate_motor_power(params)
        elif scenario == "power_boost":
            return self._calculate_power_boost(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_traction_force(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """牵引力计算"""
        u = params.get("u")  # 摩擦系数
        m = params.get("m")  # 质量 (t)
        
        if u is None or u < 0:
            raise ValueError("摩擦系数u必须大于等于0")
        if m is None or m <= 0:
            raise ValueError("质量m必须大于0")
        
        # F = u×m×g
        # Excel公式：C6 = C5*C3*10
        F = u * m * self.G
        
        formula = f"F = u × m × g<br>"
        formula += f"  = {u} × {m} × {self.G}<br>"
        formula += f"  = {F:.2f} kN"
        
        return CurrentCalcResponse(
            result=round(F, 2),
            unit="kN",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["traction_force"]
        )
    
    def _calculate_motor_power(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机功率计算"""
        F = params.get("F")  # 牵引力 (kN)
        v = params.get("v")  # 小车速度 (m/min)
        K = params.get("K", 1.25)  # 功率系数
        eta = params.get("eta", 0.8)  # 传动效率
        
        if F is None or F <= 0:
            raise ValueError("牵引力F必须大于0")
        if v is None or v <= 0:
            raise ValueError("小车速度v必须大于0")
        if K is None or K <= 0:
            raise ValueError("功率系数K必须大于0")
        if eta is None or eta <= 0 or eta > 1:
            raise ValueError("传动效率η应在0-1之间")
        
        # P = F×v×K/(60×η)
        # Excel公式：C9 = C6*C4*C7/60/C8
        P = F * v * K / (60 * eta)
        
        formula = f"P = F × v × K / (60 × η)<br>"
        formula += f"  = {F} × {v} × {K} / (60 × {eta})<br>"
        formula += f"  = {P:.4f} kW"
        
        return CurrentCalcResponse(
            result=round(P, 4),
            unit="kW",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_power"]
        )
    
    def _calculate_power_boost(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """功率提升版本计算"""
        P = params.get("P")  # 电机功率 (kW)
        
        if P is None or P <= 0:
            raise ValueError("电机功率P必须大于0")
        
        # P1 = P/1.732
        # Excel公式：C25 = C24/1.732
        P1 = P / 1.732
        
        formula = f"P<sub>1</sub> = P / 1.732<br>"
        formula += f"  = {P} / 1.732<br>"
        formula += f"  = {P1:.4f} kW"
        
        return CurrentCalcResponse(
            result=round(P1, 4),
            unit="kW",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["power_boost"]
        )
    
    def _calculate_cart_drive_power(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """小车驱动电机功率计算（完整计算）"""
        u = params.get("u", 0.1)  # 摩擦系数
        m = params.get("m")  # 质量 (t)
        v = params.get("v")  # 小车速度 (m/min)
        K = params.get("K", 1.25)  # 功率系数
        eta = params.get("eta", 0.8)  # 传动效率
        
        # 验证必需参数
        if m is None or m <= 0:
            raise ValueError("质量m必须大于0")
        if v is None or v <= 0:
            raise ValueError("小车速度v必须大于0")
        
        # 1) 牵引力
        F = u * m * self.G
        
        # 2) 电机功率
        P = F * v * K / (60 * eta)
        
        # 3) 功率提升版本
        P1 = P / 1.732
        
        # 构建详细公式字符串
        formula = f"计算步骤：<br>"
        formula += f"1) 牵引力: F = u × m × g = {u} × {m} × {self.G} = {F:.2f} kN<br>"
        formula += f"2) 电机功率: P = F × v × K / (60 × η) = {F:.2f} × {v} × {K} / (60 × {eta}) = {P:.4f} kW<br>"
        formula += f"3) 功率提升版本: P<sub>1</sub> = P / 1.732 = {P:.4f} / 1.732 = {P1:.4f} kW"
        
        return CurrentCalcResponse(
            result=round(P, 4),
            unit="kW",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["cart_drive_power"],
            extra={'F': F, 'P1': P1}
        )

