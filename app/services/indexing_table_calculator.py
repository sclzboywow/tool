"""
分度盘机构选型计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class IndexingTableCalculator:
    """分度盘机构选型计算器"""
    
    SCENARIO_NAMES = {
        "indexing_table": "分度盘机构选型计算",
        "speed_curve": "速度曲线 - 加减速时间计算",
        "motor_speed": "电机转速计算",
        "load_torque": "负载转矩计算",
        "acceleration_torque": "加速转矩计算",
        "required_torque": "必须转矩计算",
        "inertia_ratio": "负荷与电机惯量比计算"
    }
    
    # 常数
    G = 9.8  # 重力加速度 m/s²
    PI = math.pi  # 圆周率
    PI_EXCEL = 3.1416  # Excel中使用的π值
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算分度盘机构选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "indexing_table":
            return self._calculate_indexing_table(params)
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
        """速度曲线 - 加减速时间计算"""
        t = params.get("t")
        A = params.get("A")
        
        if t is None or t <= 0:
            raise ValueError("定位时间t必须大于0")
        if A is None or A < 0 or A > 1:
            raise ValueError("加减速时间比A应在0-1之间")
        
        t0 = t * A
        formula = f"t<sub>0</sub> = t × A<br>"
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
        theta = params.get("theta")  # 定位角度 (°)
        t = params.get("t")  # 定位时间 (s)
        t0 = params.get("t0")  # 加减速时间 (s)
        i = params.get("i")  # 减速比
        
        if theta is None or theta <= 0:
            raise ValueError("定位角度θ必须大于0")
        if t is None or t <= 0:
            raise ValueError("定位时间t必须大于0")
        if t0 is None or t0 <= 0:
            raise ValueError("加减速时间t0必须大于0")
        if t0 >= t:
            raise ValueError("加减速时间t0必须小于定位时间t")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        
        # 减速机输出轴角加速度 βG = ((θ×π)/180)/(t0×(t-t0))
        # Excel公式：F24 = ((F11*K6)/180)/(F20*(F12-F20))
        betaG = ((theta * self.PI_EXCEL) / 180) / (t0 * (t - t0))
        
        # 减速机输出轴最大转速 N = (βG×t0×60)/(2×π)
        # Excel公式：F29 = (F24*F20*60)/(2*K6)
        N = (betaG * t0 * 60) / (2 * self.PI_EXCEL)
        
        # 电机轴角加速度 βm = βG × i
        # Excel公式：F32 = F24*F14
        betaM = betaG * i
        
        # 电机输出轴转速 NM = N × i
        # Excel公式：F35 = F29*F14
        NM = N * i
        
        formula = f"减速机输出轴角加速度: β<sub>G</sub> = ((θ×π)/180)/(t<sub>0</sub>×(t-t<sub>0</sub>))<br>"
        formula += f"  = (({theta}×π)/180)/({t0}×({t}-{t0}))<br>"
        formula += f"  = {betaG:.6f} rad/s²<br>"
        formula += f"减速机输出轴最大转速: N = (β<sub>G</sub>×t<sub>0</sub>×60)/(2×π)<br>"
        formula += f"  = ({betaG:.6f}×{t0}×60)/(2×π)<br>"
        formula += f"  = {N:.2f} rpm<br>"
        formula += f"电机轴角加速度: β<sub>m</sub> = β<sub>G</sub> × i<br>"
        formula += f"  = {betaG:.6f} × {i}<br>"
        formula += f"  = {betaM:.6f} rad/s²<br>"
        formula += f"电机输出轴转速: N<sub>M</sub> = N × i<br>"
        formula += f"  = {N:.2f} × {i}<br>"
        formula += f"  = {NM:.2f} rpm"
        
        return CurrentCalcResponse(
            result=round(NM, 2),
            unit="rpm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_speed"],
            extra={'betaG': betaG, 'N': N, 'betaM': betaM}
        )
    
    def _calculate_load_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负载转矩计算（分度盘摩擦负载很小，通常忽略）"""
        # Excel中说明：因为摩擦负载及小，故忽略
        TL = 0
        
        formula = f"因为摩擦负载很小，故忽略<br>"
        formula += f"T<sub>L</sub> = 0 Nm"
        
        return CurrentCalcResponse(
            result=0.0,
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["load_torque"],
            extra={'TL': TL}
        )
    
    def _calculate_acceleration_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机轴加速转矩计算"""
        DT = params.get("DT")  # 分度盘直径 (m)
        LT = params.get("LT")  # 分度盘厚度 (m)
        DW = params.get("DW")  # 工作物直径 (m)
        LW = params.get("LW")  # 工作物厚度 (m)
        rho = params.get("rho")  # 工作台材质密度 (kg/m³)
        n = params.get("n")  # 工作物数量
        l = params.get("l")  # 由分度盘中心至工作物中心的距离 (m)
        i = params.get("i")  # 减速比
        JM = params.get("JM", 0.00014)  # 电机惯量 (kg·m²)
        betaM = params.get("betaM")  # 电机轴角加速度 (rad/s²)
        etaG = params.get("etaG", 0.7)  # 减速机效率
        
        if DT is None or DT <= 0:
            raise ValueError("分度盘直径DT必须大于0")
        if LT is None or LT <= 0:
            raise ValueError("分度盘厚度LT必须大于0")
        if DW is None or DW <= 0:
            raise ValueError("工作物直径DW必须大于0")
        if LW is None or LW <= 0:
            raise ValueError("工作物厚度LW必须大于0")
        if rho is None or rho <= 0:
            raise ValueError("工作台材质密度ρ必须大于0")
        if n is None or n <= 0:
            raise ValueError("工作物数量n必须大于0")
        if l is None or l <= 0:
            raise ValueError("由分度盘中心至工作物中心的距离l必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        if betaM is None or betaM <= 0:
            raise ValueError("电机轴角加速度βm必须大于0")
        if etaG <= 0 or etaG > 1:
            raise ValueError("减速机效率ηG应在0-1之间")
        
        # 工作台的惯量 JT = (π×ρ×LT×DT⁴)/32
        # Excel公式：F46 = (K6*F8*F5*F4^4)/32
        JT = (self.PI_EXCEL * rho * LT * (DT ** 4)) / 32
        
        # 工作物的惯量（绕工作物中心轴旋转）JW1 = (π×ρ×LW×DW⁴)/32
        # Excel公式：F51 = (K6*F8*F7*F6^4)/32
        JW1 = (self.PI_EXCEL * rho * LW * (DW ** 4)) / 32
        
        # 工作物质量 mw = (π×ρ×LW×DW²)/4
        # Excel公式：F55 = (K6*F8*F7*F6^2)/4
        mw = (self.PI_EXCEL * rho * LW * (DW ** 2)) / 4
        
        # 工作物的惯量（按工作物体中心自转）JW = n×(JW1 + mw×l²)
        # Excel公式：F58 = F9*(F51+F55*F10^2)
        JW = n * (JW1 + mw * (l ** 2))
        
        # 全负载惯量 JL = JT + JW
        # Excel公式：F61 = F46+F58
        JL = JT + JW
        
        # 负载折算到电机轴上的惯量 JLM = JL/i²
        # Excel公式：F67 = F61/(F14^2)
        JLM = JL / (i ** 2)
        
        # 电机轴加速转矩 Ts = ((JLM + JM)×βm)/ηG
        # Excel公式：F70 = ((F67+K55)*F32)/F15
        TS = ((JLM + JM) * betaM) / etaG
        
        formula = f"工作台的惯量: J<sub>T</sub> = (π×ρ×L<sub>T</sub>×D<sub>T</sub><sup>4</sup>)/32<br>"
        formula += f"  = (π×{rho}×{LT}×{DT}<sup>4</sup>)/32<br>"
        formula += f"  = {JT:.6f} kg·m²<br>"
        formula += f"工作物的惯量（绕工作物中心轴旋转）: J<sub>W1</sub> = (π×ρ×L<sub>W</sub>×D<sub>W</sub><sup>4</sup>)/32<br>"
        formula += f"  = (π×{rho}×{LW}×{DW}<sup>4</sup>)/32<br>"
        formula += f"  = {JW1:.6f} kg·m²<br>"
        formula += f"工作物质量: m<sub>w</sub> = (π×ρ×L<sub>W</sub>×D<sub>W</sub><sup>2</sup>)/4<br>"
        formula += f"  = (π×{rho}×{LW}×{DW}<sup>2</sup>)/4<br>"
        formula += f"  = {mw:.6f} kg<br>"
        formula += f"工作物的惯量（按工作物体中心自转）: J<sub>W</sub> = n×(J<sub>W1</sub> + m<sub>w</sub>×l<sup>2</sup>)<br>"
        formula += f"  = {n}×({JW1:.6f} + {mw:.6f}×{l}<sup>2</sup>)<br>"
        formula += f"  = {JW:.6f} kg·m²<br>"
        formula += f"全负载惯量: J<sub>L</sub> = J<sub>T</sub> + J<sub>W</sub><br>"
        formula += f"  = {JT:.6f} + {JW:.6f}<br>"
        formula += f"  = {JL:.6f} kg·m²<br>"
        formula += f"负载折算到电机轴上的惯量: J<sub>LM</sub> = J<sub>L</sub>/i<sup>2</sup><br>"
        formula += f"  = {JL:.6f}/{i}<sup>2</sup><br>"
        formula += f"  = {JLM:.6f} kg·m²<br>"
        formula += f"电机轴加速转矩: T<sub>S</sub> = ((J<sub>LM</sub> + J<sub>M</sub>)×β<sub>m</sub>)/η<sub>G</sub><br>"
        formula += f"  = (({JLM:.6f} + {JM})×{betaM:.6f})/{etaG}<br>"
        formula += f"  = {TS:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(TS, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["acceleration_torque"],
            extra={
                'JT': JT,
                'JW1': JW1,
                'mw': mw,
                'JW': JW,
                'JL': JL,
                'JLM': JLM
            }
        )
    
    def _calculate_required_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """必须转矩计算"""
        TS = params.get("TS")
        TL = params.get("TL", 0)  # 负载转矩，通常为0
        S = params.get("S", 2)
        
        if TS is None or TS < 0:
            raise ValueError("电机轴加速转矩TS必须大于等于0")
        if TL is None or TL < 0:
            raise ValueError("负载转矩TL必须大于等于0")
        if S is None or S <= 0:
            raise ValueError("安全系数S必须大于0")
        
        # 必须转矩 T = (TS + TL) × S
        # Excel公式：F74 = (F70+F39)*K73
        TM = (TS + TL) * S
        
        formula = f"T = (T<sub>S</sub> + T<sub>L</sub>) × S<br>"
        formula += f"  = ({TS:.6f} + {TL:.6f}) × {S}<br>"
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
            raise ValueError("全负载惯量JL必须大于0")
        if i is None or i <= 0:
            raise ValueError("减速比i必须大于0")
        if JM is None or JM <= 0:
            raise ValueError("电机惯量JM必须大于0")
        
        # 惯量比 N1 = (JL/(i²)) / JM
        # Excel公式：F79 = (F61/(F14^2))/K55
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
    
    def _calculate_indexing_table(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """分度盘机构选型计算（完整计算）"""
        # 输入参数
        DT = params.get("DT")
        LT = params.get("LT")
        DW = params.get("DW")
        LW = params.get("LW")
        rho = params.get("rho")
        n = params.get("n")
        l = params.get("l")
        theta = params.get("theta")
        t = params.get("t")
        A = params.get("A", 0.5)
        i = params.get("i")
        etaG = params.get("etaG", 0.7)
        JM = params.get("JM", 0.00014)
        S = params.get("S", 2)
        
        # 验证必需参数
        required_params = ["DT", "LT", "DW", "LW", "rho", "n", "l", "theta", "t", "i"]
        missing = [p for p in required_params if params.get(p) is None]
        if missing:
            raise ValueError(f"缺少必需参数: {', '.join(missing)}")
        
        # 1) 决定加减速时间
        t0 = t * A
        
        # 2) 电机转速
        betaG = ((theta * self.PI_EXCEL) / 180) / (t0 * (t - t0))
        N = (betaG * t0 * 60) / (2 * self.PI_EXCEL)
        betaM = betaG * i
        NM = N * i
        
        # 3) 负载转矩（忽略）
        TL = 0
        
        # 4) 计算电机轴加速转矩（克服惯量）
        JT = (self.PI_EXCEL * rho * LT * (DT ** 4)) / 32
        JW1 = (self.PI_EXCEL * rho * LW * (DW ** 4)) / 32
        mw = (self.PI_EXCEL * rho * LW * (DW ** 2)) / 4
        JW = n * (JW1 + mw * (l ** 2))
        JL = JT + JW
        JLM = JL / (i ** 2)
        TS = ((JLM + JM) * betaM) / etaG
        
        # 5) 必须转矩
        TM = (TS + TL) * S
        
        # 6) 惯量比
        N1 = (JL / (i ** 2)) / JM
        
        # 构建详细公式字符串
        formula = f"计算步骤：<br>"
        formula += f"1) 加减速时间: t<sub>0</sub> = t × A = {t} × {A} = {t0:.4f} s<br>"
        formula += f"2) 减速机输出轴角加速度: β<sub>G</sub> = ((θ×π)/180)/(t<sub>0</sub>×(t-t<sub>0</sub>)) = (({theta}×π)/180)/({t0:.4f}×({t}-{t0:.4f})) = {betaG:.6f} rad/s²<br>"
        formula += f"   减速机输出轴最大转速: N = (β<sub>G</sub>×t<sub>0</sub>×60)/(2×π) = {N:.2f} rpm<br>"
        formula += f"   电机轴角加速度: β<sub>m</sub> = β<sub>G</sub> × i = {betaG:.6f} × {i} = {betaM:.6f} rad/s²<br>"
        formula += f"   电机输出轴转速: N<sub>M</sub> = N × i = {N:.2f} × {i} = {NM:.2f} rpm<br>"
        formula += f"3) 负载转矩: T<sub>L</sub> = 0 Nm（因为摩擦负载很小，故忽略）<br>"
        formula += f"4) 工作台的惯量: J<sub>T</sub> = (π×ρ×L<sub>T</sub>×D<sub>T</sub><sup>4</sup>)/32 = {JT:.6f} kg·m²<br>"
        formula += f"   工作物的惯量（绕工作物中心轴旋转）: J<sub>W1</sub> = (π×ρ×L<sub>W</sub>×D<sub>W</sub><sup>4</sup>)/32 = {JW1:.6f} kg·m²<br>"
        formula += f"   工作物质量: m<sub>w</sub> = (π×ρ×L<sub>W</sub>×D<sub>W</sub><sup>2</sup>)/4 = {mw:.6f} kg<br>"
        formula += f"   工作物的惯量（按工作物体中心自转）: J<sub>W</sub> = n×(J<sub>W1</sub> + m<sub>w</sub>×l<sup>2</sup>) = {JW:.6f} kg·m²<br>"
        formula += f"   全负载惯量: J<sub>L</sub> = J<sub>T</sub> + J<sub>W</sub> = {JL:.6f} kg·m²<br>"
        formula += f"   负载折算到电机轴上的惯量: J<sub>LM</sub> = J<sub>L</sub>/i<sup>2</sup> = {JLM:.6f} kg·m²<br>"
        formula += f"   电机轴加速转矩: T<sub>S</sub> = ((J<sub>LM</sub> + J<sub>M</sub>)×β<sub>m</sub>)/η<sub>G</sub> = {TS:.6f} Nm<br>"
        formula += f"5) 必须转矩: T = (T<sub>S</sub> + T<sub>L</sub>) × S = ({TS:.6f} + {TL}) × {S} = {TM:.6f} Nm<br>"
        formula += f"6) 惯量比: N<sub>1</sub> = (J<sub>L</sub>/(i<sup>2</sup>))/J<sub>M</sub> = ({JL:.6f}/({i}<sup>2</sup>))/{JM} = {N1:.2f}"
        
        return CurrentCalcResponse(
            result=round(TM, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["indexing_table"],
        )

