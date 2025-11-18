"""
伺服电机选型计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class ServoMotorSelectionCalculator:
    """伺服电机选型计算器"""
    
    SCENARIO_NAMES = {
        "linear_motor": "直线电机选型计算",
        "rotary_motor": "旋转电机选型计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算伺服电机选型
        
        Args:
            scenario: 计算场景 (linear_motor 或 rotary_motor)
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "linear_motor":
            return self._calculate_linear_motor(params)
        elif scenario == "rotary_motor":
            return self._calculate_rotary_motor(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_linear_motor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """直线电机选型计算"""
        # 获取输入参数
        a = params.get("a")  # 加速度 (m/s²)
        V = params.get("V")  # 平台移动速度 (m/min)
        S = params.get("S")  # 单一性行程移动距离 (mm)
        Mt = params.get("Mt")  # 移动平台质量 (kg)
        Mf = params.get("Mf", 0)  # 负载质量 (kg)
        mu = params.get("mu", 0.2)  # 导轨摩擦系数
        g = params.get("g", 9.8)  # 重力加速度 (m/s²)
        
        # 验证必需参数
        required_params = {"a": a, "V": V, "S": S, "Mt": Mt}
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        formula_parts = []
        intermediate_results = {}
        
        # 1. 加减速阶段推力 Fa = Fd = (Mf+Mt)*a + (Mf+Mt)*g*μ
        M_total = Mf + Mt
        Fa = M_total * a + M_total * g * mu
        intermediate_results["Fa"] = Fa
        formula_parts.append(f"加减速阶段推力: F<sub>a</sub> = F<sub>d</sub> = (M<sub>f</sub>+M<sub>t</sub>)×a + (M<sub>f</sub>+M<sub>t</sub>)×g×μ<br>")
        formula_parts.append(f"  = ({Mf}+{Mt})×{a} + ({Mf}+{Mt})×{g}×{mu} = {Fa:.2f} N<br>")
        
        # 2. 匀速阶段推力 Fv = (Mf+Mt)*g*μ
        Fv = M_total * g * mu
        intermediate_results["Fv"] = Fv
        formula_parts.append(f"匀速阶段推力: F<sub>v</sub> = (M<sub>f</sub>+M<sub>t</sub>)×g×μ = ({Mf}+{Mt})×{g}×{mu} = {Fv:.2f} N<br>")
        
        # 3. 加减速时间 t1 = t3 = V/a/60
        t1 = V / a / 60
        intermediate_results["t1"] = t1
        formula_parts.append(f"加减速时间: t<sub>1</sub> = t<sub>3</sub> = V/a/60 = {V}/{a}/60 = {t1:.6f} s<br>")
        
        # 4. 匀速运动时间 t2 = (S - a*t1²)/V*60 + 0.012
        t2 = (S - a * t1 * t1) / V * 60 + 0.012
        intermediate_results["t2"] = t2
        formula_parts.append(f"匀速运动时间: t<sub>2</sub> = (S - a×t<sub>1</sub>²)/V×60 + 0.012 = ({S} - {a}×{t1:.6f}²)/{V}×60 + 0.012 = {t2:.6f} s<br>")
        
        # 5. 峰值推力 Fp = Fa * 1.2
        Fp = Fa * 1.2
        intermediate_results["Fp"] = Fp
        formula_parts.append(f"<br>峰值推力: F<sub>p</sub> = F<sub>a</sub> × 1.2 = {Fa:.2f} × 1.2 = {Fp:.2f} N<br>")
        
        # 6. 有效推力 Fc = sqrt((Fa²*t1 + Fv²*t2 + Fa²*t1)/(t1+t1+t2)) * 1.2
        Fc = math.sqrt((Fa * Fa * t1 + Fv * Fv * t2 + Fa * Fa * t1) / (t1 + t1 + t2)) * 1.2
        intermediate_results["Fc"] = Fc
        formula_parts.append(f"有效推力: F<sub>c</sub> = √((F<sub>a</sub>²×t<sub>1</sub> + F<sub>v</sub>²×t<sub>2</sub> + F<sub>a</sub>²×t<sub>1</sub>)/(t<sub>1</sub>+t<sub>1</sub>+t<sub>2</sub>)) × 1.2<br>")
        formula_parts.append(f"  = √(({Fa:.2f}²×{t1:.6f} + {Fv:.2f}²×{t2:.6f} + {Fa:.2f}²×{t1:.6f})/({t1:.6f}+{t1:.6f}+{t2:.6f})) × 1.2 = {Fc:.6f} N<br>")
        
        # 7. 反电势常数 Ke = 250/V*60
        Ke = 250 / V * 60
        intermediate_results["Ke"] = Ke
        formula_parts.append(f"反电势常数: K<sub>e</sub> = 250/V×60 = 250/{V}×60 = {Ke:.2f}<br>")
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        # 构建结果字典
        result = {
            "Fa": round(Fa, 2),
            "Fv": round(Fv, 2),
            "t1": round(t1, 6),
            "t2": round(t2, 6),
            "Fp": round(Fp, 2),
            "Fc": round(Fc, 6),
            "Ke": round(Ke, 2)
        }
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["linear_motor"]
        )
    
    def _calculate_rotary_motor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """旋转电机选型计算"""
        # 获取输入参数
        a = params.get("a")  # 加速度 (m/s²)
        V = params.get("V")  # 速度 (m/min)
        S = params.get("S")  # 行程 (mm)
        Mt = params.get("Mt")  # 移动平台质量 (kg)
        Mf = params.get("Mf", 0)  # 负载质量 (kg)
        mu = params.get("mu", 1)  # 摩擦系数
        eta = params.get("eta", 0.9)  # 机械传动效率
        PB = params.get("PB")  # 导螺杆节距 (mm)
        DB = params.get("DB")  # 丝杆直径 (mm)
        MB = params.get("MB", 0)  # 丝杆质量 (kg)
        g = params.get("g", 9.8)  # 重力加速度 (m/s²)
        
        # 验证必需参数
        required_params = {"a": a, "V": V, "S": S, "Mt": Mt, "PB": PB, "DB": DB}
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        formula_parts = []
        intermediate_results = {}
        
        # 1. 工作台转动惯量 Ja = (Mt+Mf)*(PB/10/2/π)²
        M_total = Mf + Mt
        Ja = M_total * (PB / 10 / 2 / math.pi) ** 2
        intermediate_results["Ja"] = Ja
        formula_parts.append(f"工作台转动惯量: J<sub>a</sub> = (M<sub>t</sub>+M<sub>f</sub>)×(P<sub>B</sub>/10/2/π)²<br>")
        formula_parts.append(f"  = ({Mt}+{Mf})×({PB}/10/2/π)² = {Ja:.6f} kg·m²<br>")
        
        # 2. 丝杆转动惯量 Jb = MB*DB/10*DB/10/8
        Jb = MB * DB / 10 * DB / 10 / 8
        intermediate_results["Jb"] = Jb
        formula_parts.append(f"丝杆转动惯量: J<sub>b</sub> = M<sub>B</sub>×D<sub>B</sub>/10×D<sub>B</sub>/10/8<br>")
        formula_parts.append(f"  = {MB}×{DB}/10×{DB}/10/8 = {Jb:.6f} kg·m²<br>")
        
        # 3. 电机转速 N = V/PB*1000
        N = V / PB * 1000
        intermediate_results["N"] = N
        formula_parts.append(f"电机转速: N = V/P<sub>B</sub>×1000 = {V}/{PB}×1000 = {N:.2f} rpm<br>")
        
        # 4. 加减速时间 t1 = t3 = V/60/a
        t1 = V / 60 / a
        intermediate_results["t1"] = t1
        formula_parts.append(f"加减速时间: t<sub>1</sub> = t<sub>3</sub> = V/60/a = {V}/60/{a} = {t1:.6f} s<br>")
        
        # 5. 匀速移动时间 t2 = (S/1000 - a*t1²)/V*60 + 0.02
        t2 = (S / 1000 - a * t1 * t1) / V * 60 + 0.02
        intermediate_results["t2"] = t2
        formula_parts.append(f"匀速移动时间: t<sub>2</sub> = (S/1000 - a×t<sub>1</sub>²)/V×60 + 0.02 = ({S}/1000 - {a}×{t1:.6f}²)/{V}×60 + 0.02 = {t2:.6f} s<br>")
        
        # 6. 加速扭矩 TA = ((Mt+Mf)*a*PB/2/π/η/1000) + (Jb*(N*2π/60/t1)/η)/10000
        TA_part1 = (M_total * a * PB / 2 / math.pi / eta / 1000)
        TA_part2 = (Jb * (N * 2 * math.pi / 60 / t1) / eta) / 10000
        TA = TA_part1 + TA_part2
        intermediate_results["TA"] = TA
        formula_parts.append(f"<br>加速扭矩: T<sub>A</sub> = ((M<sub>t</sub>+M<sub>f</sub>)×a×P<sub>B</sub>/2/π/η/1000) + (J<sub>b</sub>×(N×2π/60/t<sub>1</sub>)/η)/10000<br>")
        formula_parts.append(f"  = (({Mt}+{Mf})×{a}×{PB}/2/π/{eta}/1000) + ({Jb:.6f}×({N:.2f}×2π/60/{t1:.6f})/{eta})/10000 = {TA:.6f} N·m<br>")
        
        # 7. 匀速扭矩 TB = (Mt+Mf)*g*μ*PB/1000/2/π/η
        TB = M_total * g * mu * PB / 1000 / 2 / math.pi / eta
        intermediate_results["TB"] = TB
        formula_parts.append(f"匀速扭矩: T<sub>B</sub> = (M<sub>t</sub>+M<sub>f</sub>)×g×μ×P<sub>B</sub>/1000/2/π/η<br>")
        formula_parts.append(f"  = ({Mt}+{Mf})×{g}×{mu}×{PB}/1000/2/π/{eta} = {TB:.6f} N·m<br>")
        
        # 8. 减速扭矩 TC = TA - TB
        TC = TA - TB
        intermediate_results["TC"] = TC
        formula_parts.append(f"减速扭矩: T<sub>C</sub> = T<sub>A</sub> - T<sub>B</sub> = {TA:.6f} - {TB:.6f} = {TC:.6f} N·m<br>")
        
        # 9. 峰值扭矩 Tmax = (TA+TB)*1.2
        Tmax = (TA + TB) * 1.2
        intermediate_results["Tmax"] = Tmax
        formula_parts.append(f"<br>峰值扭矩: T<sub>max</sub> = (T<sub>A</sub>+T<sub>B</sub>)×1.2 = ({TA:.6f}+{TB:.6f})×1.2 = {Tmax:.6f} N·m<br>")
        
        # 10. 时效扭矩 Trmsx = sqrt((TA²*t1 + TB²*t2 + TC²*t1)/(t1+t1+t2))
        Trmsx = math.sqrt((TA * TA * t1 + TB * TB * t2 + TC * TC * t1) / (t1 + t1 + t2))
        intermediate_results["Trmsx"] = Trmsx
        formula_parts.append(f"时效扭矩: T<sub>rmsx</sub> = √((T<sub>A</sub>²×t<sub>1</sub> + T<sub>B</sub>²×t<sub>2</sub> + T<sub>C</sub>²×t<sub>1</sub>)/(t<sub>1</sub>+t<sub>1</sub>+t<sub>2</sub>))<br>")
        formula_parts.append(f"  = √(({TA:.6f}²×{t1:.6f} + {TB:.6f}²×{t2:.6f} + {TC:.6f}²×{t1:.6f})/({t1:.6f}+{t1:.6f}+{t2:.6f})) = {Trmsx:.6f} N·m<br>")
        
        # 11. 额定扭矩 Tf = TB*2
        Tf = TB * 2
        intermediate_results["Tf"] = Tf
        formula_parts.append(f"额定扭矩: T<sub>f</sub> = T<sub>B</sub>×2 = {TB:.6f}×2 = {Tf:.6f} N·m<br>")
        
        # 12. 转子惯量 JA = (Ja+Jb)/5 (单位×10⁻⁴ kg·m²)
        JA = (Ja + Jb) / 5
        intermediate_results["JA"] = JA
        formula_parts.append(f"转子惯量: J<sub>A</sub> = (J<sub>a</sub>+J<sub>b</sub>)/5 = ({Ja:.6f}+{Jb:.6f})/5 = {JA:.6f} ×10⁻⁴ kg·m²<br>")
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        # 构建结果字典
        result = {
            "Ja": round(Ja, 6),
            "Jb": round(Jb, 6),
            "N": round(N, 2),
            "t1": round(t1, 6),
            "t2": round(t2, 6),
            "TA": round(TA, 6),
            "TB": round(TB, 6),
            "TC": round(TC, 6),
            "Tmax": round(Tmax, 6),
            "Trmsx": round(Trmsx, 6),
            "Tf": round(Tf, 6),
            "JA": round(JA, 6)
        }
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["rotary_motor"]
        )

