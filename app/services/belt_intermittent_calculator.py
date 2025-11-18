"""
皮带轮间歇运动选型计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class BeltIntermittentCalculator:
    """皮带轮间歇运动选型计算器"""
    
    SCENARIO_NAMES = {
        "belt_intermittent": "皮带轮间歇运动选型计算",
        "speed_curve": "速度曲线 - 加速时间计算",
        "motor_speed": "电机转速计算",
        "load_torque": "负载转矩计算",
        "acceleration_torque": "加速转矩计算",
        "required_torque": "必须转矩计算",
        "inertia_ratio": "负荷与电机惯量比计算"
    }
    
    # 常数
    G = 9.8  # 重力加速度 m/s²
    PI = math.pi  # 圆周率
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算皮带轮间歇运动选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "belt_intermittent":
            return self._calculate_belt_intermittent(params)
        elif scenario == "speed_curve":
            return self._calculate_speed_curve(params)
        elif scenario == "motor_speed":
            return self._calculate_motor_speed(params)
        elif scenario == "load_torque":
            return self._calculate_load_torque(params)
        elif scenario == "acceleration_torque":
            return self._calculate_acceleration_torque(params)
        elif scenario == "required_torque":
            return self._calculate_required_torque(params)
        elif scenario == "inertia_ratio":
            return self._calculate_inertia_ratio(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_speed_curve(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """速度曲线 - 加速时间计算"""
        t = params.get("t")
        A = params.get("A")
        
        if t is None or t <= 0:
            raise ValueError("定位时间t必须大于0")
        if A is None or A < 0 or A > 1:
            raise ValueError("加减速时间比A应在0-1之间")
        
        t0 = t * A
        formula = f"t₀ = t × A<br>"
        formula += f"  = {t} × {A}<br>"
        formula += f"  = {t0:.4f} s"
        
        return CurrentCalcResponse(
            result=round(t0, 4),
            unit="s",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["speed_curve"]
        )
    
    def _calculate_motor_speed(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机转速计算"""
        L = params.get("L")
        D = params.get("D")
        t = params.get("t")
        t0 = params.get("t0")
        i = params.get("i")
        
        if L is None or L <= 0:
            raise ValueError("运动距离L必须大于0")
        if D is None or D <= 0:
            raise ValueError("滚筒直径D必须大于0")
        if t is None or t <= 0:
            raise ValueError("定位时间t必须大于0")
        if t0 is None or t0 <= 0:
            raise ValueError("加速时间t0必须大于0")
        if t0 >= t:
            raise ValueError("加速时间t0必须小于定位时间t")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # 减速机输出轴角加速度 β = 2*(L/D)/(t0*(t-t0))
        beta = 2 * (L / D) / (t0 * (t - t0))
        
        # 减速机输出轴转速 N = (β*t0/(2π))*60
        N = (beta * t0 / (2 * self.PI)) * 60
        
        # 电机输出轴角加速度 βM = i*β
        betaM = i * beta
        
        # 电机输出轴转速 NM = N*i
        NM = N * i
        
        formula = f"减速机输出轴角加速度: β = 2×(L/D)/(t₀×(t-t₀))<br>"
        formula += f"  = 2×({L}/{D})/({t0}×({t}-{t0}))<br>"
        formula += f"  = {beta:.4f} rad/s²<br>"
        formula += f"减速机输出轴转速: N = (β×t₀/(2π))×60<br>"
        formula += f"  = ({beta:.4f}×{t0}/(2π))×60<br>"
        formula += f"  = {N:.2f} rpm<br>"
        formula += f"电机输出轴角加速度: β<sub>M</sub> = i×β<br>"
        formula += f"  = {i}×{beta:.4f}<br>"
        formula += f"  = {betaM:.4f} rad/s²<br>"
        formula += f"电机输出轴转速: N<sub>M</sub> = N×i<br>"
        formula += f"  = {N:.2f}×{i}<br>"
        formula += f"  = {NM:.2f} rpm"
        
        return CurrentCalcResponse(
            result=round(NM, 2),
            unit="rpm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_speed"],
            extra={'beta': beta, 'N': N, 'betaM': betaM}
        )
    
    def _calculate_load_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负载转矩计算"""
        FA = params.get("FA", 0)
        mL = params.get("mL")
        a = params.get("a", 0)
        mu = params.get("mu", 0.3)
        D = params.get("D")
        eta = params.get("eta", 0.9)
        i = params.get("i")
        etaG = params.get("etaG", 0.7)
        
        if mL is None or mL <= 0:
            raise ValueError("皮带与工作物总质量mL必须大于0")
        if a < -90 or a > 90:
            raise ValueError("移动方向与水平轴夹角a应在-90°到90°之间")
        if mu < 0:
            raise ValueError("摩擦系数μ不能为负数")
        if D is None or D <= 0:
            raise ValueError("滚筒直径D必须大于0")
        if eta <= 0 or eta > 1:
            raise ValueError("传送带和滚筒的机械效率η应在0-1之间")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if etaG <= 0 or etaG > 1:
            raise ValueError("减速机机械效率ηG应在0-1之间")
        
        # 减速机轴向负载 F = FA + mL×g×(sin(a) + μ×cos(a))
        a_rad = math.radians(a)
        F = FA + mL * self.G * (math.sin(a_rad) + mu * math.cos(a_rad))
        
        # 减速机轴负载转矩 TL = (F × D) / (2 × η)
        TL = (F * D) / (2 * eta)
        
        # 电机轴负载转矩 TLM = TL / (i × ηG)
        TLM = TL / (i * etaG)
        
        formula = f"减速机轴向负载: F = F<sub>A</sub> + m<sub>L</sub>×g×(sin a + μ×cos a)<br>"
        formula += f"  = {FA} + {mL}×{self.G}×(sin({a}°) + {mu}×cos({a}°))<br>"
        formula += f"  = {F:.4f} N<br>"
        formula += f"减速机轴负载转矩: T<sub>L</sub> = (F × D) / (2 × η)<br>"
        formula += f"  = ({F:.4f} × {D}) / (2 × {eta})<br>"
        formula += f"  = {TL:.6f} Nm<br>"
        formula += f"电机轴负载转矩: T<sub>LM</sub> = T<sub>L</sub> / (i × η<sub>G</sub>)<br>"
        formula += f"  = {TL:.6f} / ({i} × {etaG})<br>"
        formula += f"  = {TLM:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TLM, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["load_torque"],
            extra={'F': F, 'TL': TL}
        )
    
    def _calculate_acceleration_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机轴加速转矩计算"""
        mL = params.get("mL")
        D = params.get("D")
        m2 = params.get("m2")
        i = params.get("i")
        JM = params.get("JM", 0.00027)
        betaM = params.get("betaM")
        etaG = params.get("etaG", 0.7)
        
        if mL is None or mL <= 0:
            raise ValueError("皮带与工作物总质量mL必须大于0")
        if D is None or D <= 0:
            raise ValueError("滚筒直径D必须大于0")
        if m2 is None or m2 <= 0:
            raise ValueError("滚筒质量m2必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        if betaM is None or betaM <= 0:
            raise ValueError("电机输出轴角加速度βM必须大于0")
        if etaG <= 0 or etaG > 1:
            raise ValueError("减速机机械效率ηG应在0-1之间")
        
        # 皮带和工作物的惯量 JM1 = mL × (D/2)²
        JM1 = mL * ((D / 2) ** 2)
        
        # 滚筒的惯量 JM2 = (m2 × D²) / 8
        JM2 = (m2 * (D ** 2)) / 8
        
        # 折算到减速机轴的负载惯量 JL = JM1 + 2×JM2
        JL = JM1 + 2 * JM2
        
        # 全负载惯量 J = JL/(i²) + JM
        J = JL / (i ** 2) + JM
        
        # 电机轴加速转矩 TS = J × βM / ηG
        TS = J * betaM / etaG
        
        formula = f"皮带和工作物的惯量: J<sub>M1</sub> = m<sub>L</sub> × (D/2)²<br>"
        formula += f"  = {mL} × ({D}/2)²<br>"
        formula += f"  = {JM1:.6f} kg·m²<br>"
        formula += f"滚筒的惯量: J<sub>M2</sub> = (m<sub>2</sub> × D²) / 8<br>"
        formula += f"  = ({m2} × {D}²) / 8<br>"
        formula += f"  = {JM2:.6f} kg·m²<br>"
        formula += f"折算到减速机轴的负载惯量: J<sub>L</sub> = J<sub>M1</sub> + 2×J<sub>M2</sub><br>"
        formula += f"  = {JM1:.6f} + 2×{JM2:.6f}<br>"
        formula += f"  = {JL:.6f} kg·m²<br>"
        formula += f"全负载惯量: J = J<sub>L</sub>/(i²) + J<sub>M</sub><br>"
        formula += f"  = {JL:.6f}/({i}²) + {JM}<br>"
        formula += f"  = {J:.6f} kg·m²<br>"
        formula += f"电机轴加速转矩: T<sub>S</sub> = J × β<sub>M</sub> / η<sub>G</sub><br>"
        formula += f"  = {J:.6f} × {betaM:.4f} / {etaG}<br>"
        formula += f"  = {TS:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TS, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["acceleration_torque"],
            extra={
                'JM1': JM1,
                'JM2': JM2,
                'JL': JL,
                'J': J
            }
        )
    
    def _calculate_required_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """必须转矩计算"""
        TLM = params.get("TLM")
        TS = params.get("TS")
        S = params.get("S", 2)
        
        if TLM is None or TLM < 0:
            raise ValueError("电机轴负载转矩TLM必须大于等于0")
        if TS is None or TS < 0:
            raise ValueError("电机轴加速转矩TS必须大于等于0")
        if S is None or S <= 0:
            raise ValueError("安全系数S必须大于0")
        
        TM = (TLM + TS) * S
        formula = f"T<sub>M</sub> = (T<sub>LM</sub> + T<sub>S</sub>) × S<br>"
        formula += f"  = ({TLM} + {TS}) × {S}<br>"
        formula += f"  = {TM:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TM, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["required_torque"]
        )
    
    def _calculate_inertia_ratio(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负荷与电机惯量比计算"""
        JL = params.get("JL")
        i = params.get("i")
        JM = params.get("JM")
        
        if JL is None or JL <= 0:
            raise ValueError("折算到减速机轴的负载惯量JL必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        
        # 惯量比 N1 = (JL/(i²)) / JM
        N1 = (JL / (i ** 2)) / JM
        i_squared = i ** 2
        JL_converted = JL / i_squared
        
        formula = f"N<sub>1</sub> = (J<sub>L</sub>/(i²)) / J<sub>M</sub><br>"
        formula += f"  = ({JL}/({i}²)) / {JM}<br>"
        formula += f"  = ({JL} / {i_squared}) / {JM}<br>"
        formula += f"  = {JL_converted:.6f} / {JM}<br>"
        formula += f"  = {N1:.2f}"
        
        return CurrentCalcResponse(
            result=round(N1, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["inertia_ratio"]
        )
    
    def _calculate_belt_intermittent(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """皮带轮间歇运动选型计算（完整计算）"""
        # 输入参数
        mL = params.get("mL")
        mu = params.get("mu", 0.3)
        D = params.get("D")
        m2 = params.get("m2")
        eta = params.get("eta", 0.9)
        etaG = params.get("etaG", 0.7)
        i = params.get("i", 1)
        t = params.get("t")
        L = params.get("L")
        A = params.get("A", 0.5)
        FA = params.get("FA", 0)
        a = params.get("a", 0)
        S = params.get("S", 2)
        JM = params.get("JM", 0.00027)
        
        # 验证必需参数
        required_params = ["mL", "D", "m2", "t", "L"]
        missing = [p for p in required_params if params.get(p) is None]
        if missing:
            raise ValueError(f"缺少必需参数: {', '.join(missing)}")
        
        # 1) 速度曲线：加速时间
        t0 = t * A
        
        # 2) 电机转速
        beta = 2 * (L / D) / (t0 * (t - t0))
        N = (beta * t0 / (2 * self.PI)) * 60
        betaM = i * beta
        NM = N * i
        
        # 3) 负载转矩
        a_rad = math.radians(a)
        F = FA + mL * self.G * (math.sin(a_rad) + mu * math.cos(a_rad))
        TL = (F * D) / (2 * eta)
        TLM = TL / (i * etaG)
        
        # 4) 加速转矩
        JM1 = mL * ((D / 2) ** 2)
        JM2 = (m2 * (D ** 2)) / 8
        JL = JM1 + 2 * JM2
        J = JL / (i ** 2) + JM
        TS = J * betaM / etaG
        
        # 5) 必须转矩
        TM = (TLM + TS) * S
        
        # 6) 惯量比
        N1 = (JL / (i ** 2)) / JM
        
        # 构建详细公式字符串
        formula = f"计算步骤：<br>"
        formula += f"1) 加速时间: t0 = t × A = {t} × {A} = {t0:.4f} s<br>"
        formula += f"2) 减速机输出轴角加速度: β = 2×(L/D)/(t₀×(t-t₀)) = 2×({L}/{D})/({t0:.4f}×({t}-{t0:.4f})) = {beta:.4f} rad/s²<br>"
        formula += f"   减速机输出轴转速: N = (β×t₀/(2π))×60 = {N:.2f} rpm<br>"
        formula += f"   电机输出轴角加速度: βM = i×β = {i}×{beta:.4f} = {betaM:.4f} rad/s²<br>"
        formula += f"   电机输出轴转速: NM = N×i = {N:.2f}×{i} = {NM:.2f} rpm<br>"
        formula += f"3) 减速机轴向负载: F = FA + mL×g×(sin a + μ×cos a) = {FA} + {mL}×{self.G}×(sin({a}°) + {mu}×cos({a}°)) = {F:.4f} N<br>"
        formula += f"   减速机轴负载转矩: TL = (F×D)/(2×η) = ({F:.4f}×{D})/(2×{eta}) = {TL:.4f} Nm<br>"
        formula += f"   电机轴负载转矩: TLM = TL/(i×ηG) = {TL:.4f}/({i}×{etaG}) = {TLM:.4f} Nm<br>"
        formula += f"4) 皮带和工作物的惯量: JM1 = mL×(D/2)² = {mL}×({D}/2)² = {JM1:.6f} kg·m²<br>"
        formula += f"   滚筒的惯量: JM2 = (m2×D²)/8 = ({m2}×{D}²)/8 = {JM2:.6f} kg·m²<br>"
        formula += f"   折算到减速机轴的负载惯量: JL = JM1 + 2×JM2 = {JM1:.6f} + 2×{JM2:.6f} = {JL:.6f} kg·m²<br>"
        formula += f"   全负载惯量: J = JL/(i²) + JM = {JL:.6f}/({i}²) + {JM} = {J:.6f} kg·m²<br>"
        formula += f"   电机轴加速转矩: TS = J×βM/ηG = {J:.6f}×{betaM:.4f}/{etaG} = {TS:.4f} Nm<br>"
        formula += f"5) 必须转矩: TM = (TLM + TS)×S = ({TLM:.4f} + {TS:.4f})×{S} = {TM:.4f} Nm<br>"
        formula += f"6) 惯量比: N1 = (JL/(i²))/JM = ({JL:.6f}/({i}²))/{JM} = {N1:.2f}"
        
        return CurrentCalcResponse(
            result=round(TM, 4),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["belt_intermittent"],
        )

