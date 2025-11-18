"""
丝杠垂直运动选型计算服务
"""
import math
from typing import Dict, Any, Optional
from app.models.schemas import CurrentCalcResponse


class ScrewVerticalCalculator:
    """丝杠垂直运动选型计算器"""
    
    SCENARIO_NAMES = {
        "screw_vertical": "丝杠垂直运动选型计算",
        "speed_curve": "速度曲线 - 加速时间计算",
        "motor_speed": "电机转速计算",
        "load_torque": "负荷转矩计算",
        "acceleration_torque": "加速转矩计算",
        "required_torque": "必须转矩计算",
        "inertia_ratio_motor": "负荷与电机惯量比计算",
        "inertia_ratio_reducer": "负荷与减速机惯量比计算"
    }
    
    # 常数
    G = 9.8  # 重力加速度 m/s²
    PI = math.pi  # 圆周率
    RHO = 7900  # 丝杠密度 kg/m³
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算丝杠垂直运动选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "screw_vertical":
            return self._calculate_screw_vertical(params)
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
        elif scenario == "inertia_ratio_motor":
            return self._calculate_inertia_ratio_motor(params)
        elif scenario == "inertia_ratio_reducer":
            return self._calculate_inertia_ratio_reducer(params)
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
        Vl = params.get("Vl")
        PB = params.get("PB")
        
        if Vl is None or Vl <= 0:
            raise ValueError("速度Vl必须大于0")
        if PB is None or PB <= 0:
            raise ValueError("丝杠导程PB必须大于0")
        
        NM = Vl / PB
        formula = f"N<sub>M</sub> = V<sub>l</sub> / P<sub>B</sub><br>"
        formula += f"  = {Vl} / {PB}<br>"
        formula += f"  = {NM:.2f} rpm"
        
        return CurrentCalcResponse(
            result=round(NM, 2),
            unit="rpm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_speed"]
        )
    
    def _calculate_load_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负荷转矩计算（垂直运动，a=90°）"""
        FA = params.get("FA", 0)
        M = params.get("M")
        a = params.get("a", 90)  # 垂直运动默认90°
        mu = params.get("mu", 0.1)
        PB = params.get("PB")
        eta = params.get("eta", 0.9)
        
        if M is None or M <= 0:
            raise ValueError("滑动部分质量M必须大于0")
        if a < -90 or a > 90:
            raise ValueError("移动方向与水平轴夹角a应在-90°到90°之间")
        if mu < 0:
            raise ValueError("摩擦系数μ不能为负数")
        if PB is None or PB <= 0:
            raise ValueError("丝杠导程PB必须大于0")
        if eta <= 0 or eta > 1:
            raise ValueError("机械效率η应在0-1之间")
        
        # 轴向负载 F = FA + M×G×(sin(a) + μ×cos(a))
        a_rad = math.radians(a)
        F = FA + M * self.G * (math.sin(a_rad) + mu * math.cos(a_rad))
        
        # 负载转矩 TL = (F × PB) / (2π × η)
        TL = (F * PB) / (2 * self.PI * eta)
        
        formula = f"轴向负载: F = F<sub>A</sub> + M×G×(sin a + μ×cos a)<br>"
        formula += f"  = {FA} + {M}×{self.G}×(sin({a}°) + {mu}×cos({a}°))<br>"
        formula += f"  = {F:.4f} N<br>"
        formula += f"负载转矩: T<sub>L</sub> = (F × P<sub>B</sub>) / (2π × η)<br>"
        formula += f"  = ({F:.4f} × {PB}) / (2π × {eta})<br>"
        formula += f"  = {TL:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TL, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["load_torque"],
            extra={'F': F}
        )
    
    def _calculate_acceleration_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """克服惯量的加速转矩计算"""
        M = params.get("M")
        PB = params.get("PB")
        LB = params.get("LB")
        DB = params.get("DB")
        MC = params.get("MC")
        DC = params.get("DC")
        NM = params.get("NM")
        JM = params.get("JM", 0.0002)
        t0 = params.get("t0")
        
        if M is None or M <= 0:
            raise ValueError("滑动部分质量M必须大于0")
        if PB is None or PB <= 0:
            raise ValueError("丝杠导程PB必须大于0")
        if LB is None or LB <= 0:
            raise ValueError("丝杠长度LB必须大于0")
        if DB is None or DB <= 0:
            raise ValueError("丝杠直径DB必须大于0")
        if MC is None or MC <= 0:
            raise ValueError("连轴器质量MC必须大于0")
        if DC is None or DC <= 0:
            raise ValueError("连轴器直径DC必须大于0")
        if NM is None or NM <= 0:
            raise ValueError("电机转速NM必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        if t0 is None or t0 <= 0:
            raise ValueError("加速时间t0必须大于0")
        
        # 直线运动平台与负载惯量 JL1 = M × (PB/(2π))²
        JL1 = M * (PB / (2 * self.PI)) ** 2
        
        # 滚珠丝杠惯量 JB = π × ρ × LB × DB⁴ / 32
        JB = self.PI * self.RHO * LB * (DB ** 4) / 32
        
        # 连轴器惯量 JC = MC × DC² / 8
        JC = MC * (DC ** 2) / 8
        
        # 总负荷惯量 JL = JL1 + JB + JC
        JL = JL1 + JB + JC
        
        # 启动转矩 TS = 2π × NM × (JM + JL) / (60 × t0)
        TS = 2 * self.PI * NM * (JM + JL) / (60 * t0)
        
        formula = f"直线运动平台惯量: J<sub>L1</sub> = M × (P<sub>B</sub>/(2π))²<br>"
        formula += f"  = {M} × ({PB}/(2π))²<br>"
        formula += f"  = {JL1:.6f} kg·m²<br>"
        formula += f"滚珠丝杠惯量: J<sub>B</sub> = (π/32) × ρ × L<sub>B</sub> × D<sub>B</sub>⁴<br>"
        formula += f"  = (π/32) × {self.RHO} × {LB} × {DB}⁴<br>"
        formula += f"  = {JB:.6f} kg·m²<br>"
        formula += f"连轴器惯量: J<sub>C</sub> = M<sub>C</sub> × D<sub>C</sub>² / 8<br>"
        formula += f"  = {MC} × {DC}² / 8<br>"
        formula += f"  = {JC:.6f} kg·m²<br>"
        formula += f"总负荷惯量: J<sub>L</sub> = J<sub>L1</sub> + J<sub>B</sub> + J<sub>C</sub><br>"
        formula += f"  = {JL1:.6f} + {JB:.6f} + {JC:.6f}<br>"
        formula += f"  = {JL:.6f} kg·m²<br>"
        formula += f"启动转矩: T<sub>S</sub> = (2π × N<sub>M</sub> × (J<sub>M</sub> + J<sub>L</sub>)) / (60 × t<sub>0</sub>)<br>"
        formula += f"  = (2π × {NM} × ({JM} + {JL:.6f})) / (60 × {t0})<br>"
        formula += f"  = {TS:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TS, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["acceleration_torque"],
            extra={
                'JL1': JL1,
                'JB': JB,
                'JC': JC,
                'JL': JL
            }
        )
    
    def _calculate_required_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """必须转矩计算"""
        TL = params.get("TL")
        TS = params.get("TS")
        S = params.get("S", 2)  # 垂直运动默认安全系数2
        
        if TL is None or TL < 0:
            raise ValueError("负载转矩TL必须大于等于0")
        if TS is None or TS < 0:
            raise ValueError("启动转矩TS必须大于等于0")
        if S is None or S <= 0:
            raise ValueError("安全系数S必须大于0")
        
        TM = (TL + TS) * S
        formula = f"T<sub>M</sub> = (T<sub>L</sub> + T<sub>S</sub>) × S<br>"
        formula += f"  = ({TL} + {TS}) × {S}<br>"
        formula += f"  = {TM:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TM, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["required_torque"]
        )
    
    def _calculate_inertia_ratio_motor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负荷与电机惯量比计算"""
        JL = params.get("JL")
        JM = params.get("JM")
        
        if JL is None or JL <= 0:
            raise ValueError("总负荷惯量JL必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        
        I1 = JL / JM
        formula = f"I<sub>1</sub> = J<sub>L</sub> / J<sub>M</sub><br>"
        formula += f"  = {JL} / {JM}<br>"
        formula += f"  = {I1:.2f}"
        
        return CurrentCalcResponse(
            result=round(I1, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["inertia_ratio_motor"]
        )
    
    def _calculate_inertia_ratio_reducer(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负荷与减速机惯量比计算"""
        JL = params.get("JL")
        JM = params.get("JM")
        i = params.get("i")
        
        if JL is None or JL <= 0:
            raise ValueError("总负荷惯量JL必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速机减速比i必须大于0")
        
        I2 = JL / (JM * (i ** 2))
        i_squared = i ** 2
        denominator = JM * i_squared
        formula = f"I<sub>2</sub> = J<sub>L</sub> / (J<sub>M</sub> × i²)<br>"
        formula += f"  = {JL} / ({JM} × {i}²)<br>"
        formula += f"  = {JL} / ({JM} × {i_squared})<br>"
        formula += f"  = {JL} / {denominator}<br>"
        formula += f"  = {I2:.2f}"
        
        return CurrentCalcResponse(
            result=round(I2, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["inertia_ratio_reducer"]
        )
    
    def _calculate_screw_vertical(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """丝杠垂直运动选型计算（完整计算）"""
        # 输入参数
        Vl = params.get("Vl")  # 速度 (m/min)
        M = params.get("M")  # 滑动部分质量 (kg)
        LB = params.get("LB")  # 丝杠长度 (m)
        DB = params.get("DB")  # 丝杠直径 (m)
        PB = params.get("PB")  # 丝杠导程 (m)
        MC = params.get("MC")  # 连轴器质量 (kg)
        DC = params.get("DC")  # 连轴器直径 (m)
        mu = params.get("mu", 0.1)  # 摩擦系数
        eta = params.get("eta", 0.9)  # 机械效率
        t = params.get("t")  # 定位时间 (s)
        A = params.get("A", 0.25)  # 加减速时间比
        FA = params.get("FA", 0)  # 外力 (N)
        a = params.get("a", 90)  # 移动方向与水平轴夹角 (°)，垂直运动默认90°
        S = params.get("S", 2)  # 安全系数，垂直运动默认2
        JM = params.get("JM", 0.0002)  # 电机惯量 (kg·m²)
        i = params.get("i", 4)  # 减速机减速比
        
        # 验证必需参数
        required_params = ["Vl", "M", "LB", "DB", "PB", "MC", "DC", "t"]
        missing = [p for p in required_params if params.get(p) is None]
        if missing:
            raise ValueError(f"缺少必需参数: {', '.join(missing)}")
        
        # 1) 速度曲线：加速时间
        t0 = t * A
        
        # 2) 电机转速
        NM = Vl / PB  # rpm
        
        # 3) 负荷转矩计算
        # 轴向负载 F = FA + M×G×(sin(a) + μ×cos(a))
        a_rad = math.radians(a)  # 角度转弧度
        F = FA + M * self.G * (math.sin(a_rad) + mu * math.cos(a_rad))
        
        # 负载转矩 TL = (F × PB) / (2π × η)
        TL = (F * PB) / (2 * self.PI * eta)
        
        # 4) 克服惯量的加速转矩计算
        # 直线运动平台与负载惯量 JL1 = M × (PB/(2π))²
        JL1 = M * (PB / (2 * self.PI)) ** 2
        
        # 滚珠丝杠惯量 JB = π × ρ × LB × DB⁴ / 32
        JB = self.PI * self.RHO * LB * (DB ** 4) / 32
        
        # 连轴器惯量 JC = MC × DC² / 8
        JC = MC * (DC ** 2) / 8
        
        # 总负荷惯量 JL = JL1 + JB + JC
        JL = JL1 + JB + JC
        
        # 启动转矩 TS = 2π × NM × (JM + JL) / (60 × t0)
        TS = 2 * self.PI * NM * (JM + JL) / (60 * t0)
        
        # 5) 必须转矩
        TM = (TL + TS) * S
        
        # 7) 负荷与电机惯量比
        I1 = JL / JM if JM > 0 else 0
        
        # 8) 负荷与减速机惯量比
        I2 = JL / (JM * (i ** 2)) if (JM > 0 and i > 0) else 0
        
        # 构建详细公式字符串
        formula = f"计算步骤：<br>"
        formula += f"1) 加速时间: t0 = t × A = {t} × {A} = {t0:.4f} s<br>"
        formula += f"2) 电机转速: NM = Vl / PB = {Vl} / {PB} = {NM:.2f} rpm<br>"
        formula += f"3) 轴向负载: F = FA + M×G×(sin(a) + μ×cos(a)) = {FA} + {M}×{self.G}×(sin({a}°) + {mu}×cos({a}°)) = {F:.4f} N<br>"
        formula += f"   负载转矩: TL = (F × PB) / (2π × η) = ({F:.4f} × {PB}) / (2π × {eta}) = {TL:.4f} Nm<br>"
        formula += f"4) 直线运动平台惯量: JL1 = M × (PB/(2π))² = {M} × ({PB}/(2π))² = {JL1:.6f} kg·m²<br>"
        formula += f"   滚珠丝杠惯量: JB = π × ρ × LB × DB⁴ / 32 = π × {self.RHO} × {LB} × {DB}⁴ / 32 = {JB:.6f} kg·m²<br>"
        formula += f"   连轴器惯量: JC = MC × DC² / 8 = {MC} × {DC}² / 8 = {JC:.6f} kg·m²<br>"
        formula += f"   总负荷惯量: JL = JL1 + JB + JC = {JL1:.6f} + {JB:.6f} + {JC:.6f} = {JL:.6f} kg·m²<br>"
        formula += f"   启动转矩: TS = 2π × NM × (JM + JL) / (60 × t0) = 2π × {NM:.2f} × ({JM} + {JL:.6f}) / (60 × {t0:.4f}) = {TS:.4f} Nm<br>"
        formula += f"5) 必须转矩: TM = (TL + TS) × S = ({TL:.4f} + {TS:.4f}) × {S} = {TM:.4f} Nm<br>"
        formula += f"7) 惯量比: I1 = JL / JM = {JL:.6f} / {JM} = {I1:.2f}<br>"
        formula += f"8) 折算后的惯量比: I2 = JL / (JM × i²) = {JL:.6f} / ({JM} × {i}²) = {I2:.2f}"
        
        # 返回主要结果（必须转矩）和详细信息
        return CurrentCalcResponse(
            result=round(TM, 4),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["screw_vertical"],
        )

