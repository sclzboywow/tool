"""
角加速度计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class AngularAccelerationCalculator:
    """角加速度计算器"""
    
    SCENARIO_NAMES = {
        "acceleration_time": "加速时间计算",
        "motor_speed": "电机转速计算",
        "torque": "扭矩计算",
        "angular_acceleration": "角加速度计算"  # 保留完整计算
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算角加速度
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "acceleration_time":
            return self._calculate_acceleration_time(params)
        elif scenario == "motor_speed":
            return self._calculate_motor_speed(params)
        elif scenario == "torque":
            return self._calculate_torque(params)
        elif scenario == "angular_acceleration":
            return self._calculate_angular_acceleration(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_acceleration_time(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """加速时间计算"""
        t = params.get("t")  # 每次定位时间 (s)
        A = params.get("A")  # 加减速时间比
        
        if t is None or t <= 0:
            raise ValueError("每次定位时间t必须大于0")
        if A is None or A <= 0 or A >= 1:
            raise ValueError("加减速时间比A必须在0和1之间")
        
        # 加速时间: t0 = t × A
        t0 = t * A
        
        formula = f"加速时间: t<sub>0</sub> = t × A<br>"
        formula += f"  = {t} × {A}<br>"
        formula += f"  = {t0:.4f} s"
        
        return CurrentCalcResponse(
            result=round(t0, 4),
            unit="s",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["acceleration_time"],
            extra={'t0': t0}
        )
    
    def _calculate_motor_speed(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机转速计算"""
        i = params.get("i")  # 减速比
        t = params.get("t")  # 每次定位时间 (s)
        L = params.get("L")  # 每次运动角度 (°)
        A = params.get("A")  # 加减速时间比
        
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if t is None or t <= 0:
            raise ValueError("每次定位时间t必须大于0")
        if L is None or L <= 0:
            raise ValueError("每次运动角度L必须大于0")
        if A is None or A <= 0 or A >= 1:
            raise ValueError("加减速时间比A必须在0和1之间")
        
        # 1. 加速时间
        t0 = t * A
        
        # 2. 减速机输出轴角加速度
        beta = (L * math.pi) / (180 * (t0 * (t - t0)))
        
        # 3. 减速机输出轴转速
        Nmax = (beta * t0 / (2 * math.pi)) * 60
        
        # 4. 电机输出轴角加速度
        betaM = i * beta
        
        # 5. 电机输出轴转速
        NM = Nmax * i
        
        formula = f"加速时间: t<sub>0</sub> = t × A<br>"
        formula += f"  = {t} × {A}<br>"
        formula += f"  = {t0:.4f} s<br>"
        formula += f"减速机输出轴角加速度: β = (L×π)/(180×(t<sub>0</sub>×(t-t<sub>0</sub>)))<br>"
        formula += f"  = ({L}×π)/(180×({t0:.4f}×({t}-{t0:.4f})))<br>"
        formula += f"  = {beta:.6f} rad/s²<br>"
        formula += f"减速机输出轴转速: N<sub>max</sub> = (β×t<sub>0</sub>/(2×π))×60<br>"
        formula += f"  = ({beta:.6f}×{t0:.4f}/(2×π))×60<br>"
        formula += f"  = {Nmax:.4f} rpm<br>"
        formula += f"电机输出轴角加速度: β<sub>M</sub> = i × β<br>"
        formula += f"  = {i} × {beta:.6f}<br>"
        formula += f"  = {betaM:.6f} rad/s²<br>"
        formula += f"电机输出轴转速: N<sub>M</sub> = N<sub>max</sub> × i<br>"
        formula += f"  = {Nmax:.4f} × {i}<br>"
        formula += f"  = {NM:.4f} rpm"
        
        return CurrentCalcResponse(
            result=round(NM, 4),
            unit="rpm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_speed"],
            extra={
                't0': t0,
                'beta': beta,
                'Nmax': Nmax,
                'betaM': betaM
            }
        )
    
    def _calculate_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """扭矩计算"""
        J = params.get("J")  # 负载惯量 (Kg.m²)
        betaM = params.get("betaM")  # 电机输出轴角加速度 (rad/s²)
        
        if J is None or J <= 0:
            raise ValueError("负载惯量J必须大于0")
        if betaM is None or betaM <= 0:
            raise ValueError("电机输出轴角加速度βM必须大于0")
        
        # 电机输出扭矩
        T = J * betaM
        
        # 启动扭矩
        Ts = 2 * T
        
        formula = f"电机输出扭矩: T = J × β<sub>M</sub><br>"
        formula += f"  = {J} × {betaM:.6f}<br>"
        formula += f"  = {T:.6f} Nm<br>"
        formula += f"启动扭矩: T<sub>s</sub> = 2 × T<br>"
        formula += f"  = 2 × {T:.6f}<br>"
        formula += f"  = {Ts:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(Ts, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["torque"],
            extra={'T': T}
        )
    
    def _calculate_angular_acceleration(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """角加速度计算"""
        # 获取参数
        i = params.get("i")  # 减速比
        t = params.get("t")  # 每次定位时间 (s)
        L = params.get("L")  # 每次运动角度 (°)
        A = params.get("A")  # 加减速时间比
        J = params.get("J")  # 负载惯量 (Kg.m²)
        
        # 验证参数
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if t is None or t <= 0:
            raise ValueError("每次定位时间t必须大于0")
        if L is None or L <= 0:
            raise ValueError("每次运动角度L必须大于0")
        if A is None or A <= 0 or A >= 1:
            raise ValueError("加减速时间比A必须在0和1之间")
        if J is None or J <= 0:
            raise ValueError("负载惯量J必须大于0")
        
        # 1. 加速时间: t0 = t × A
        # Excel公式：F12 = F5*F7
        t0 = t * A
        
        # 2. 减速机输出轴角加速度: β = (L×π)/(180×(t0×(t-t0)))
        # Excel公式：F16 = (F6*K5)/(180*(F12*(F5-F12)))，K5=3.1416
        beta = (L * math.pi) / (180 * (t0 * (t - t0)))
        
        # 3. 减速机输出轴转速: Nmax = (β×t0/(2×π))×60
        # Excel公式：F20 = (F16*F12/(2*K5))*60
        Nmax = (beta * t0 / (2 * math.pi)) * 60
        
        # 4. 电机输出轴角加速度: βM = i × β
        # Excel公式：F23 = F4*F16
        betaM = i * beta
        
        # 5. 电机输出轴转速: NM = Nmax × i
        # Excel公式：F26 = F20*F4
        NM = Nmax * i
        
        # 6. 电机输出扭矩: T = J × βM
        # Excel公式：F29 = F8*F23
        T = J * betaM
        
        # 7. 启动扭矩: Ts = 2 × T
        # Excel公式：F32 = 2*F29
        Ts = 2 * T
        
        # 构建公式字符串
        formula = f"加速时间: t<sub>0</sub> = t × A<br>"
        formula += f"  = {t} × {A}<br>"
        formula += f"  = {t0:.4f} s<br>"
        formula += f"减速机输出轴角加速度: β = (L×π)/(180×(t<sub>0</sub>×(t-t<sub>0</sub>)))<br>"
        formula += f"  = ({L}×π)/(180×({t0:.4f}×({t}-{t0:.4f})))<br>"
        formula += f"  = {beta:.6f} rad/s²<br>"
        formula += f"减速机输出轴转速: N<sub>max</sub> = (β×t<sub>0</sub>/(2×π))×60<br>"
        formula += f"  = ({beta:.6f}×{t0:.4f}/(2×π))×60<br>"
        formula += f"  = {Nmax:.4f} rpm<br>"
        formula += f"电机输出轴角加速度: β<sub>M</sub> = i × β<br>"
        formula += f"  = {i} × {beta:.6f}<br>"
        formula += f"  = {betaM:.6f} rad/s²<br>"
        formula += f"电机输出轴转速: N<sub>M</sub> = N<sub>max</sub> × i<br>"
        formula += f"  = {Nmax:.4f} × {i}<br>"
        formula += f"  = {NM:.4f} rpm<br>"
        formula += f"电机输出扭矩: T = J × β<sub>M</sub><br>"
        formula += f"  = {J} × {betaM:.6f}<br>"
        formula += f"  = {T:.6f} Nm<br>"
        formula += f"启动扭矩: T<sub>s</sub> = 2 × T<br>"
        formula += f"  = 2 × {T:.6f}<br>"
        formula += f"  = {Ts:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(Ts, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["angular_acceleration"],
            extra={
                't0': t0,
                'beta': beta,
                'Nmax': Nmax,
                'betaM': betaM,
                'NM': NM,
                'T': T
            }
        )

