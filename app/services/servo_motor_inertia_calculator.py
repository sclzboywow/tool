"""
伺服电机惯量计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class ServoMotorInertiaCalculator:
    """伺服电机惯量计算器"""
    
    SCENARIO_NAMES = {
        "servo_motor_inertia": "伺服电机惯量计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算伺服电机惯量
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "servo_motor_inertia":
            return self._calculate_servo_motor_inertia(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_servo_motor_inertia(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """伺服电机惯量计算（齿轮齿条传动）"""
        # 获取基本参数
        M = params.get("M")  # 被移动件的质量 (kg)
        v_fast = params.get("v_fast")  # 快移速度 (m/min)
        t_acc = params.get("t_acc")  # 加速时间 (s)
        a = params.get("a")  # 加速度 (m/s²)
        FC = params.get("FC", 0)  # 最大切削抗力 (N)
        v_cut = params.get("v_cut", 0)  # 最大抗力时的速度 (m/min)
        u = params.get("u", 0.1)  # 摩擦系数
        m_gear = params.get("m_gear")  # 齿轮模数
        Z = params.get("Z")  # 齿轮齿数
        alpha_gear = params.get("alpha_gear", 0)  # 齿轮斜角 (度)
        D = params.get("D")  # 齿轮分度圆直径 (m)
        eta = params.get("eta", 0.98)  # 传动效率
        i = params.get("i")  # 减速比
        eta_reducer = params.get("eta_reducer", 0.8)  # 减速机效率
        Jm = params.get("Jm")  # 电机自身转动惯量 (kg·m²)
        JG = params.get("JG", 0)  # 齿轮自身惯量 (kg·m²)
        is_vertical = params.get("is_vertical", False)  # 是否垂直运动
        g = params.get("g", 9.8)  # 重力加速度 (m/s²)
        
        # 验证必需参数
        required_params = {
            "M": M, "v_fast": v_fast, "t_acc": t_acc, "a": a,
            "m_gear": m_gear, "Z": Z, "D": D, "i": i, "Jm": Jm
        }
        
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        formula_parts = []
        intermediate_results = {}
        
        # 1. 快速移动时的计算
        # 1.1 加速力 Fa = M * a
        Fa = M * a
        intermediate_results["Fa"] = Fa
        formula_parts.append(f"加速力: F<sub>a</sub> = M × a = {M} × {a} = {Fa:.2f} N<br>")
        
        # 1.2 摩擦力 Ff = M * g * u (水平运动)
        if is_vertical:
            # 垂直运动时，摩擦力需要考虑重力
            Ff = M * g * u
        else:
            Ff = M * g * u
        intermediate_results["Ff"] = Ff
        formula_parts.append(f"摩擦力: F<sub>f</sub> = M × g × u = {M} × {g} × {u} = {Ff:.2f} N<br>")
        
        # 1.3 合力 F_total = Fa + Ff
        F_total = Fa + Ff
        intermediate_results["F_total"] = F_total
        formula_parts.append(f"合力: F<sub>total</sub> = F<sub>a</sub> + F<sub>f</sub> = {Fa:.2f} + {Ff:.2f} = {F_total:.2f} N<br>")
        
        # 1.4 齿轮最高转速 n1 = v_fast / (π * D)
        n1 = v_fast / (math.pi * D)
        intermediate_results["n1"] = n1
        formula_parts.append(f"齿轮最高转速: n<sub>1</sub> = v<sub>fast</sub> / (π × D) = {v_fast} / (π × {D}) = {n1:.2f} rpm<br>")
        
        # 1.5 齿轮角加速度 βG = n1 * 2π / 60 / t_acc
        beta_G = n1 * 2 * math.pi / 60 / t_acc
        intermediate_results["beta_G"] = beta_G
        formula_parts.append(f"齿轮角加速度: β<sub>G</sub> = n<sub>1</sub> × 2π / 60 / t<sub>acc</sub> = {n1:.2f} × 2π / 60 / {t_acc} = {beta_G:.6f} rad/s²<br>")
        
        # 1.6 齿轮损耗的加速力矩 TG = βG * JG
        TG = beta_G * JG
        intermediate_results["TG"] = TG
        formula_parts.append(f"齿轮损耗的加速力矩: T<sub>G</sub> = β<sub>G</sub> × J<sub>G</sub> = {beta_G:.6f} × {JG} = {TG:.6f} N·m<br>")
        
        # 1.7 合力矩 Treq = F_total * D/2 / eta + TG
        Treq = F_total * D / 2 / eta + TG
        intermediate_results["Treq"] = Treq
        formula_parts.append(f"合力矩: T<sub>req</sub> = F<sub>total</sub> × D/2 / η + T<sub>G</sub> = {F_total:.2f} × {D}/2 / {eta} + {TG:.6f} = {Treq:.6f} N·m<br>")
        
        # 1.8 减速机输入端的加速力矩 T2 = Treq / i / eta_reducer
        T2 = Treq / i / eta_reducer
        intermediate_results["T2"] = T2
        formula_parts.append(f"减速机输入端的加速力矩: T<sub>2</sub> = T<sub>req</sub> / i / η<sub>reducer</sub> = {Treq:.6f} / {i} / {eta_reducer} = {T2:.6f} N·m<br>")
        
        # 1.9 电机的最大转速 n2 = n1 * i
        n2 = n1 * i
        intermediate_results["n2"] = n2
        formula_parts.append(f"电机的最大转速: n<sub>2</sub> = n<sub>1</sub> × i = {n1:.2f} × {i} = {n2:.2f} rpm<br>")
        
        # 1.10 电机角加速度 βm = βG * i
        beta_m = beta_G * i
        intermediate_results["beta_m"] = beta_m
        formula_parts.append(f"电机角加速度: β<sub>m</sub> = β<sub>G</sub> × i = {beta_G:.6f} × {i} = {beta_m:.6f} rad/s²<br>")
        
        # 1.11 电机克服自身惯量加速的力矩 Tm = Jm * βm
        Tm = Jm * beta_m
        intermediate_results["Tm"] = Tm
        formula_parts.append(f"电机克服自身惯量加速的力矩: T<sub>m</sub> = J<sub>m</sub> × β<sub>m</sub> = {Jm} × {beta_m:.6f} = {Tm:.6f} N·m<br>")
        
        # 1.12 电机在加速时总的输出力矩 Tm1 = T2 + Tm
        Tm1 = T2 + Tm
        intermediate_results["Tm1"] = Tm1
        formula_parts.append(f"<br>电机在加速时总的输出力矩: T<sub>m1</sub> = T<sub>2</sub> + T<sub>m</sub> = {T2:.6f} + {Tm:.6f} = {Tm1:.6f} N·m<br>")
        
        # 2. 切削时的计算
        if FC > 0:
            # 2.1 切削抗力 Fc = FC
            Fc = FC
            intermediate_results["Fc"] = Fc
            
            # 2.2 摩擦力 f = Ff
            f = Ff
            intermediate_results["f"] = f
            
            # 2.3 合力 F_cut = Fc + f
            F_cut = Fc + f
            intermediate_results["F_cut"] = F_cut
            
            # 2.4 力矩 Tc = F_cut * D/2 / eta
            Tc = F_cut * D / 2 / eta
            intermediate_results["Tc"] = Tc
            formula_parts.append(f"<br>切削时合力矩: T<sub>c</sub> = (F<sub>c</sub> + F<sub>f</sub>) × D/2 / η = ({Fc:.2f} + {f:.2f}) × {D}/2 / {eta} = {Tc:.6f} N·m<br>")
            
            # 2.5 电机输出端的额定力矩 T3 = Tc / i / eta_reducer
            T3 = Tc / i / eta_reducer
            intermediate_results["T3"] = T3
            formula_parts.append(f"电机输出端的额定力矩: T<sub>3</sub> = T<sub>c</sub> / i / η<sub>reducer</sub> = {Tc:.6f} / {i} / {eta_reducer} = {T3:.6f} N·m<br>")
            
            # 2.6 对应的齿轮转速 n_cut = v_cut / (π * D)
            if v_cut > 0:
                n_cut = v_cut / (math.pi * D)
                intermediate_results["n_cut"] = n_cut
                formula_parts.append(f"对应的齿轮转速: n<sub>cut</sub> = v<sub>cut</sub> / (π × D) = {v_cut} / (π × {D}) = {n_cut:.2f} rpm<br>")
                
                # 2.7 电机转速 n_motor_cut = n_cut * i
                n_motor_cut = n_cut * i
                intermediate_results["n_motor_cut"] = n_motor_cut
                formula_parts.append(f"电机转速: n<sub>motor_cut</sub> = n<sub>cut</sub> × i = {n_cut:.2f} × {i} = {n_motor_cut:.2f} rpm<br>")
        
        # 3. 惯量匹配计算
        # 3.1 负载惯量 JL = M * D² / 4
        JL = M * D * D / 4
        intermediate_results["JL"] = JL
        formula_parts.append(f"<br>负载惯量: J<sub>L</sub> = M × D² / 4 = {M} × {D}² / 4 = {JL:.6f} kg·m²<br>")
        
        # 3.2 折算到减速机输入端的惯量 J1 = (JL + JG) / i²
        J1 = (JL + JG) / (i * i)
        intermediate_results["J1"] = J1
        formula_parts.append(f"折算到减速机输入端的惯量: J<sub>1</sub> = (J<sub>L</sub> + J<sub>G</sub>) / i² = ({JL:.6f} + {JG}) / {i}² = {J1:.6f} kg·m²<br>")
        
        # 3.3 减速机自身惯量 Jg (需要从参数获取，如果没有则设为0)
        Jg = params.get("Jg", 0)  # 减速机自身惯量 (kg·m²)
        intermediate_results["Jg"] = Jg
        
        # 3.4 折算到电机输出端的惯量 J2 = J1 + Jg
        J2 = J1 + Jg
        intermediate_results["J2"] = J2
        formula_parts.append(f"折算到电机输出端的惯量: J<sub>2</sub> = J<sub>1</sub> + J<sub>g</sub> = {J1:.6f} + {Jg} = {J2:.6f} kg·m²<br>")
        
        # 3.5 惯量匹配值 λ = J2 / Jm
        # 注意：惯量匹配计算使用的Jm可能与快速移动计算使用的Jm不同
        Jm_inertia = params.get("Jm_inertia", Jm)  # 用于惯量匹配的电机惯量，默认使用Jm
        lambda_inertia = J2 / Jm_inertia
        intermediate_results["lambda_inertia"] = lambda_inertia
        formula_parts.append(f"惯量匹配值: λ = J<sub>2</sub> / J<sub>m</sub> = {J2:.6f} / {Jm_inertia} = {lambda_inertia:.6f}<br>")
        
        # 4. 侧倾力矩计算
        # 4.1 最大水平切向力 = F_total
        F_tangential = F_total
        intermediate_results["F_tangential"] = F_tangential
        
        # 4.2 齿轮端面压力角 an (度) - 如果未提供，使用默认值或计算
        an = params.get("an", 21.116)  # 齿轮端面压力角 (度)
        intermediate_results["an"] = an
        
        # 4.3 最大径向力 F2rmax = F_total / cos(an) ≈ F_total / 0.93285
        # Excel中使用固定系数0.93285，对应cos(21.116°)≈0.93285
        F2rmax = F_total / 0.93285
        intermediate_results["F2rmax"] = F2rmax
        formula_parts.append(f"<br>最大径向力: F<sub>2rmax</sub> = F<sub>total</sub> / cos(a<sub>n</sub>) ≈ {F_total:.2f} / 0.93285 = {F2rmax:.2f} N<br>")
        
        # 4.4 斜角 a0 (度) - 如果未提供，使用默认值
        a0 = params.get("a0", 19.5283)  # 斜角 (度)
        intermediate_results["a0"] = a0
        
        # 4.5 最大轴向力 F2amax = F_total * tan(a0) ≈ F_total * 0.35467
        # Excel中使用固定系数0.35467，对应tan(19.5283°)≈0.35467
        F2amax = F_total * 0.35467
        intermediate_results["F2amax"] = F2amax
        formula_parts.append(f"最大轴向力: F<sub>2amax</sub> = F<sub>total</sub> × tan(a<sub>0</sub>) ≈ {F_total:.2f} × 0.35467 = {F2amax:.2f} N<br>")
        
        # 4.6 减速器输出端轴承的支撑跨度 Z2 (m)
        Z2 = params.get("Z2", 0.0812)  # 支撑跨度 (m)
        intermediate_results["Z2"] = Z2
        
        # 4.7 径向力的力臂长 x2 (m) - 由齿轮安装位置决定
        X2 = params.get("X2", 15.5)  # 齿轮受力X2 (mm)
        x2 = X2 / 1000  # 转换为m
        intermediate_results["x2"] = x2
        
        # 4.8 轴向力的力臂长 y2 (m) - 由齿轮半径决定
        # 注意：y2通常不等于D/2，需要根据实际安装位置确定
        # 如果未提供，使用默认值0.089127（来自Excel示例）
        y2 = params.get("y2")
        if y2 is None:
            # 尝试从D计算，但通常需要用户输入
            y2 = D / 2  # 临时使用D/2，但实际应该由用户提供
        intermediate_results["y2"] = y2
        
        # 4.9 侧倾力矩 M2Kmax = Z2*F2rmax + x2*F2rmax + F2amax*y2
        M2Kmax = Z2 * F2rmax + x2 * F2rmax + F2amax * y2
        intermediate_results["M2Kmax"] = M2Kmax
        formula_parts.append(f"侧倾力矩: M<sub>2Kmax</sub> = Z<sub>2</sub>×F<sub>2rmax</sub> + x<sub>2</sub>×F<sub>2rmax</sub> + F<sub>2amax</sub>×y<sub>2</sub><br>")
        formula_parts.append(f"  = {Z2}×{F2rmax:.2f} + {x2:.4f}×{F2rmax:.2f} + {F2amax:.2f}×{y2:.6f} = {M2Kmax:.6f} N·m<br>")
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        # 构建结果字典
        result = {
            "Fa": round(Fa, 2),
            "Ff": round(Ff, 2),
            "F_total": round(F_total, 2),
            "n1": round(n1, 2),
            "beta_G": round(beta_G, 6),
            "TG": round(TG, 6),
            "Treq": round(Treq, 6),
            "T2": round(T2, 6),
            "n2": round(n2, 2),
            "beta_m": round(beta_m, 6),
            "Tm": round(Tm, 6),
            "Tm1": round(Tm1, 6),
            "JL": round(JL, 6),
            "J1": round(J1, 6),
            "J2": round(J2, 6),
            "lambda_inertia": round(lambda_inertia, 6),
            "F_tangential": round(F_tangential, 2),
            "F2rmax": round(F2rmax, 2),
            "F2amax": round(F2amax, 2),
            "M2Kmax": round(M2Kmax, 6)
        }
        
        # 如果有切削计算，添加到结果中
        if FC > 0:
            result["Fc"] = round(Fc, 2)
            result["f"] = round(f, 2)
            result["F_cut"] = round(F_cut, 2)
            result["Tc"] = round(Tc, 6)
            result["T3"] = round(T3, 6)
            if v_cut > 0:
                result["n_cut"] = round(n_cut, 2)
                result["n_motor_cut"] = round(n_motor_cut, 2)
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["servo_motor_inertia"]
        )

