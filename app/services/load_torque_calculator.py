"""
不同驱动机构下负载转矩计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class LoadTorqueCalculator:
    """不同驱动机构下负载转矩计算器"""
    
    SCENARIO_NAMES = {
        "ball_screw": "滚珠丝杠驱动下负载转矩计算",
        "pulley": "滑轮驱动下负载转矩计算",
        "belt_gear_rack": "金属线、皮带齿轮、齿条驱动下负载转矩计算",
        "test_method": "实际测试计算方法"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算负载转矩
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "ball_screw":
            return self._calculate_ball_screw(params)
        elif scenario == "pulley":
            return self._calculate_pulley(params)
        elif scenario == "belt_gear_rack":
            return self._calculate_belt_gear_rack(params)
        elif scenario == "test_method":
            return self._calculate_test_method(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_ball_screw(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """滚珠丝杠驱动下负载转矩计算"""
        # 获取参数
        FA = params.get("FA")  # 外力 (N)
        m = params.get("m")  # 工作物与工作台的总质量 (kg)
        g = params.get("g", 9.807)  # 重力加速度 (m/s²)
        alpha = params.get("alpha")  # 倾斜角度 (°)
        mu = params.get("mu")  # 滑动面的摩擦系数
        PB = params.get("PB")  # 滚珠螺杆螺距 (m/rev)
        eta = params.get("eta")  # 机械效率
        mu0 = params.get("mu0")  # 预压螺帽的内部摩擦系数
        F0 = params.get("F0")  # 预负载 (N)
        i = params.get("i")  # 减速比
        
        # 验证参数
        if FA is None:
            raise ValueError("外力FA必须提供")
        if m is None or m <= 0:
            raise ValueError("工作物与工作台的总质量m必须大于0")
        if alpha is None:
            raise ValueError("倾斜角度alpha必须提供")
        if mu is None or mu < 0:
            raise ValueError("滑动面的摩擦系数μ必须大于等于0")
        if PB is None or PB <= 0:
            raise ValueError("滚珠螺杆螺距PB必须大于0")
        if eta is None or eta <= 0 or eta > 1:
            raise ValueError("机械效率η应在0-1之间")
        if mu0 is None or mu0 < 0:
            raise ValueError("预压螺帽的内部摩擦系数μ0必须大于等于0")
        if F0 is None or F0 < 0:
            raise ValueError("预负载F0必须大于等于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # 1. 计算轴方向负载 F = FA + mg(sinα + μcosα)
        alpha_rad = math.radians(alpha)
        F = FA + m * g * (math.sin(alpha_rad) + mu * math.cos(alpha_rad))
        
        # 2. 计算负载转矩 TL = (F×PB/(2×π×η) + μ0×F0×PB/(2×π)) × (1/i)
        TL = (F * PB / (2 * math.pi * eta) + mu0 * F0 * PB / (2 * math.pi)) * (1 / i)
        
        formula = f"轴方向负载: F = F<sub>A</sub> + mg(sinα + μcosα)<br>"
        formula += f"  = {FA} + {m}×{g}×(sin{alpha}° + {mu}×cos{alpha}°)<br>"
        formula += f"  = {FA} + {m}×{g}×({math.sin(alpha_rad):.6f} + {mu}×{math.cos(alpha_rad):.6f})<br>"
        formula += f"  = {F:.10f} N<br>"
        formula += f"负载转矩: T<sub>L</sub> = (F×P<sub>B</sub>/(2×π×η) + μ<sub>0</sub>×F<sub>0</sub>×P<sub>B</sub>/(2×π)) × (1/i)<br>"
        formula += f"  = ({F:.10f}×{PB}/(2×π×{eta}) + {mu0}×{F0}×{PB}/(2×π)) × (1/{i})<br>"
        formula += f"  = {TL:.10f} Nm"
        
        return CurrentCalcResponse(
            result=round(TL, 10),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["ball_screw"],
            extra={'F': F}
        )
    
    def _calculate_pulley(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """滑轮驱动下负载转矩计算"""
        FA = params.get("FA")  # 外力 (N)
        m = params.get("m")  # 工作物与工作台的总质量 (kg)
        g = params.get("g", 9.807)  # 重力加速度 (m/s²)
        mu = params.get("mu")  # 滑动面的摩擦系数
        D = params.get("D")  # 终段滑轮直径 (m)
        i = params.get("i")  # 减速比
        
        # 验证参数
        if FA is None:
            raise ValueError("外力FA必须提供")
        if m is None or m <= 0:
            raise ValueError("工作物与工作台的总质量m必须大于0")
        if mu is None or mu < 0:
            raise ValueError("滑动面的摩擦系数μ必须大于等于0")
        if D is None or D <= 0:
            raise ValueError("终段滑轮直径D必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # TL = (μ×FA + m×g) × D / (2×i)
        TL = (mu * FA + m * g) * D / (2 * i)
        
        formula = f"负载转矩: T<sub>L</sub> = (μ×F<sub>A</sub> + m×g) × D / (2×i)<br>"
        formula += f"  = ({mu}×{FA} + {m}×{g}) × {D} / (2×{i})<br>"
        formula += f"  = {TL:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TL, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["pulley"]
        )
    
    def _calculate_belt_gear_rack(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """金属线、皮带齿轮、齿条驱动下负载转矩计算"""
        FA = params.get("FA")  # 外力 (N)
        m = params.get("m")  # 工作物与工作台的总质量 (kg)
        g = params.get("g", 9.807)  # 重力加速度 (m/s²)
        alpha = params.get("alpha")  # 倾斜角度 (°)
        mu = params.get("mu")  # 滑动面的摩擦系数
        D = params.get("D")  # 小齿轮/链轮直径 (m)
        eta = params.get("eta")  # 机械效率
        i = params.get("i")  # 减速比
        
        # 验证参数
        if FA is None:
            raise ValueError("外力FA必须提供")
        if m is None or m <= 0:
            raise ValueError("工作物与工作台的总质量m必须大于0")
        if alpha is None:
            raise ValueError("倾斜角度alpha必须提供")
        if mu is None or mu < 0:
            raise ValueError("滑动面的摩擦系数μ必须大于等于0")
        if D is None or D <= 0:
            raise ValueError("小齿轮/链轮直径D必须大于0")
        if eta is None or eta <= 0 or eta > 1:
            raise ValueError("机械效率η应在0-1之间")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # 1. 计算力 F = FA + mg(sinα + μcosα)
        alpha_rad = math.radians(alpha)
        F = FA + m * g * (math.sin(alpha_rad) + mu * math.cos(alpha_rad))
        
        # 2. 计算负载转矩 TL = F × D / (2×η×i)
        TL = F * D / (2 * eta * i)
        
        formula = f"力: F = F<sub>A</sub> + mg(sinα + μcosα)<br>"
        formula += f"  = {FA} + {m}×{g}×(sin{alpha}° + {mu}×cos{alpha}°)<br>"
        formula += f"  = {FA} + {m}×{g}×({math.sin(alpha_rad):.6f} + {mu}×{math.cos(alpha_rad):.6f})<br>"
        formula += f"  = {F:.10f} N<br>"
        formula += f"负载转矩: T<sub>L</sub> = F × D / (2×η×i)<br>"
        formula += f"  = {F:.10f} × {D} / (2×{eta}×{i})<br>"
        formula += f"  = {TL:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TL, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["belt_gear_rack"],
            extra={'F': F}
        )
    
    def _calculate_test_method(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """实际测试计算方法"""
        FB = params.get("FB")  # 主轴开始运动时的力 (N)
        D = params.get("D")  # 终段滑轮直径 (m)
        
        # 验证参数
        if FB is None or FB <= 0:
            raise ValueError("主轴开始运动时的力FB必须大于0")
        if D is None or D <= 0:
            raise ValueError("终段滑轮直径D必须大于0")
        
        # TL = FB × (D / 2)
        TL = FB * (D / 2)
        
        formula = f"负载转矩: T<sub>L</sub> = F<sub>B</sub> × (D / 2)<br>"
        formula += f"  = {FB} × ({D} / 2)<br>"
        formula += f"  = {TL:.6f} Nm<br>"
        formula += f"<small>注: F<sub>B</sub> = 弹簧秤值 (kg×g [m/s²])</small>"
        
        return CurrentCalcResponse(
            result=round(TL, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["test_method"]
        )

