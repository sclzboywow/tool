"""
皮带轮连续运动选型计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class BeltContinuousCalculator:
    """皮带轮连续运动选型计算器"""
    
    SCENARIO_NAMES = {
        "belt_continuous": "皮带轮连续运动选型计算",
        "motor_speed": "电机转速计算",
        "load_torque": "负载转矩计算",
        "inertia_conversion": "计算折算到电机轴的惯量",
        "required_torque": "必须转矩计算",
        "inertia_ratio": "负荷与电机惯量比计算"
    }
    
    # 常数
    G = 9.8  # 重力加速度 m/s²
    PI = math.pi  # 圆周率
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算皮带轮连续运动选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "belt_continuous":
            return self._calculate_belt_continuous(params)
        elif scenario == "motor_speed":
            return self._calculate_motor_speed(params)
        elif scenario == "load_torque":
            return self._calculate_load_torque(params)
        elif scenario == "inertia_conversion":
            return self._calculate_inertia_conversion(params)
        elif scenario == "required_torque":
            return self._calculate_required_torque(params)
        elif scenario == "inertia_ratio":
            return self._calculate_inertia_ratio(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_motor_speed(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机转速计算（连续运动）"""
        V = params.get("V")  # 线速度 m/min
        D = params.get("D")  # 滚筒直径 m
        i = params.get("i", 1)  # 减速比
        
        if V is None or V <= 0:
            raise ValueError("线速度V必须大于0")
        if D is None or D <= 0:
            raise ValueError("滚筒直径D必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # 减速机输出轴转速 N = V / (π × D)
        # 按照Excel表格公式：F17 = (F5/(K7*F8))，其中F5是V，K7是π，F8是D
        # Excel中使用的是3.1416作为π值
        PI_EXCEL = 3.1416  # Excel中使用的π值
        N = V / (PI_EXCEL * D)
        
        # 电机输出轴转速 NM = N × i
        NM = N * i
        
        formula = f"减速机输出轴转速: N = V / (π × D)<br>"
        formula += f"  = {V} / (π × {D})<br>"
        formula += f"  = {N:.6f} rpm<br>"
        formula += f"电机输出轴转速: N<sub>M</sub> = N × i<br>"
        formula += f"  = {N:.2f} × {i}<br>"
        formula += f"  = {NM:.2f} rpm"
        
        return CurrentCalcResponse(
            result=round(NM, 2),
            unit="rpm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_speed"],
            extra={'N': N}
        )
    
    def _calculate_load_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负载转矩计算"""
        FA = params.get("FA", 0)
        mL = params.get("mL")
        a = params.get("a", 0)
        mu = params.get("mu", 0.3)
        D = params.get("D")
        eta = params.get("eta", 0.9)
        i = params.get("i", 1)
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
        # Excel公式：F25 = F13+F6*K6*(SIN((F14/360)*2*K7)+F7*COS((F14/360)*2*K7))
        # Excel中使用 (a/360)*2*π 作为角度转换，而不是 math.radians(a)
        PI_EXCEL = 3.1416  # Excel中使用的π值
        a_rad_excel = (a / 360) * 2 * PI_EXCEL
        F = FA + mL * self.G * (math.sin(a_rad_excel) + mu * math.cos(a_rad_excel))
        
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
    
    def _calculate_inertia_conversion(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算折算到电机轴的惯量"""
        mL = params.get("mL")
        D = params.get("D")
        m2 = params.get("m2")
        
        if mL is None or mL <= 0:
            raise ValueError("皮带与工作物总质量mL必须大于0")
        if D is None or D <= 0:
            raise ValueError("滚筒直径D必须大于0")
        if m2 is None or m2 <= 0:
            raise ValueError("滚筒质量m2必须大于0")
        
        # 皮带和工作物的惯量 JM1 = mL × (D/2)²
        JM1 = mL * ((D / 2) ** 2)
        
        # 滚筒的惯量 JM2 = (m2 × D²) / 8
        JM2 = (m2 * (D ** 2)) / 8
        
        # 折算到减速机轴的负载惯量 JL = JM1 + 2×JM2
        JL = JM1 + 2 * JM2
        
        formula = f"皮带和工作物的惯量: J<sub>M1</sub> = m<sub>L</sub> × (D/2)<sup>2</sup><br>"
        formula += f"  = {mL} × ({D}/2)<sup>2</sup><br>"
        formula += f"  = {JM1:.6f} kg·m²<br>"
        formula += f"滚筒的惯量: J<sub>M2</sub> = (m<sub>2</sub> × D<sup>2</sup>) / 8<br>"
        formula += f"  = ({m2} × {D}<sup>2</sup>) / 8<br>"
        formula += f"  = {JM2:.6f} kg·m²<br>"
        formula += f"折算到减速机轴的负载惯量: J<sub>L</sub> = J<sub>M1</sub> + 2×J<sub>M2</sub><br>"
        formula += f"  = {JM1:.6f} + 2×{JM2:.6f}<br>"
        formula += f"  = {JL:.6f} kg·m²"
        
        return CurrentCalcResponse(
            result=round(JL, 6),
            unit="kg·m²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["inertia_conversion"],
            extra={
                'JM1': JM1,
                'JM2': JM2,
                'JL': JL
            }
        )
    
    def _calculate_required_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """必须转矩计算（连续运动，无加速转矩）"""
        TLM = params.get("TLM")
        S = params.get("S", 1.5)
        
        if TLM is None or TLM < 0:
            raise ValueError("电机轴负载转矩TLM必须大于等于0")
        if S is None or S <= 0:
            raise ValueError("安全系数S必须大于0")
        
        # 连续运动：必须转矩 = 负载转矩 × 安全系数（无加速转矩）
        TM = TLM * S
        
        formula = f"T<sub>M</sub> = T<sub>LM</sub> × S<br>"
        formula += f"  = {TLM:.6f} × {S}<br>"
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
        
        formula = f"N<sub>1</sub> = (J<sub>L</sub>/(i<sup>2</sup>)) / J<sub>M</sub><br>"
        formula += f"  = ({JL}/({i}<sup>2</sup>)) / {JM}<br>"
        formula += f"  = ({JL} / {i_squared}) / {JM}<br>"
        formula += f"  = {JL_converted:.6f} / {JM}<br>"
        formula += f"  = {N1:.2f}"
        
        return CurrentCalcResponse(
            result=round(N1, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["inertia_ratio"]
        )
    
    def _calculate_belt_continuous(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """皮带轮连续运动选型计算（完整计算）"""
        # 输入参数
        V = params.get("V")  # 线速度 m/min
        mL = params.get("mL")
        mu = params.get("mu", 0.3)
        D = params.get("D")
        m2 = params.get("m2")
        eta = params.get("eta", 0.9)
        etaG = params.get("etaG", 0.7)
        i = params.get("i", 1)
        FA = params.get("FA", 0)
        a = params.get("a", 0)
        S = params.get("S", 1.5)
        JM = params.get("JM", 0.00027)
        
        # 验证必需参数
        required_params = ["V", "mL", "D", "m2"]
        missing = [p for p in required_params if params.get(p) is None]
        if missing:
            raise ValueError(f"缺少必需参数: {', '.join(missing)}")
        
        # 1) 电机转速（按照Excel公式）
        PI_EXCEL = 3.1416  # Excel中使用的π值
        N = V / (PI_EXCEL * D)
        NM = N * i
        
        # 2) 负载转矩（按照Excel公式）
        PI_EXCEL = 3.1416  # Excel中使用的π值
        a_rad_excel = (a / 360) * 2 * PI_EXCEL
        F = FA + mL * self.G * (math.sin(a_rad_excel) + mu * math.cos(a_rad_excel))
        TL = (F * D) / (2 * eta)
        TLM = TL / (i * etaG)
        
        # 3) 计算折算到电机轴的惯量
        JM1 = mL * ((D / 2) ** 2)
        JM2 = (m2 * (D ** 2)) / 8
        JL = JM1 + 2 * JM2
        
        # 4) 必须转矩（连续运动无加速转矩）
        TM = TLM * S
        
        # 5) 惯量比
        N1 = (JL / (i ** 2)) / JM
        
        # 构建详细公式字符串（按照Excel表格顺序）
        formula = f"计算步骤：<br>"
        formula += f"1) 减速机输出轴转速: N = V / (π × D) = {V} / (π × {D}) = {N:.6f} rpm<br>"
        formula += f"   电机输出轴转速: N<sub>M</sub> = N × i = {N:.6f} × {i} = {NM:.6f} rpm<br>"
        formula += f"2) 减速机轴向负载: F = F<sub>A</sub> + m<sub>L</sub>×g×(sin a + μ×cos a) = {FA} + {mL}×{self.G}×(sin({a}°) + {mu}×cos({a}°)) = {F:.4f} N<br>"
        formula += f"   减速机轴负载转矩: T<sub>L</sub> = (F×D)/(2×η) = ({F:.4f}×{D})/(2×{eta}) = {TL:.6f} Nm<br>"
        formula += f"   电机轴负载转矩: T<sub>LM</sub> = T<sub>L</sub>/(i×η<sub>G</sub>) = {TL:.6f}/({i}×{etaG}) = {TLM:.6f} Nm<br>"
        formula += f"3) 皮带和工作物的惯量: J<sub>M1</sub> = m<sub>L</sub>×(D/2)<sup>2</sup> = {mL}×({D}/2)<sup>2</sup> = {JM1:.6f} kg·m²<br>"
        formula += f"   滚筒的惯量: J<sub>M2</sub> = (m<sub>2</sub>×D<sup>2</sup>)/8 = ({m2}×{D}<sup>2</sup>)/8 = {JM2:.6f} kg·m²<br>"
        formula += f"   折算到减速机轴的负载惯量: J<sub>L</sub> = J<sub>M1</sub> + 2×J<sub>M2</sub> = {JM1:.6f} + 2×{JM2:.6f} = {JL:.6f} kg·m²<br>"
        formula += f"4) 必须转矩: T<sub>M</sub> = T<sub>LM</sub> × S = {TLM:.6f} × {S} = {TM:.6f} Nm<br>"
        formula += f"5) 惯量比: N<sub>1</sub> = (J<sub>L</sub>/(i<sup>2</sup>))/J<sub>M</sub> = ({JL:.6f}/({i}<sup>2</sup>))/{JM} = {N1:.5f}"
        
        return CurrentCalcResponse(
            result=round(TM, 4),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["belt_continuous"],
        )

