"""
伺服电机参数计算服务
基于FANUC伺服电机选型要求
"""
import math
from typing import Dict, Any, Optional
from app.models.schemas import CurrentCalcResponse


class ServoMotorParamsCalculator:
    """伺服电机参数计算器"""
    
    SCENARIO_NAMES = {
        "servo_motor_params": "伺服电机参数计算"
    }
    
    # 丝杠材料密度 (kg/m³)
    STEEL_DENSITY = 7800
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        计算伺服电机参数
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "servo_motor_params":
            return self._calculate_servo_motor_params(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_servo_motor_params(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """伺服电机参数计算"""
        # 获取输入参数
        axis_type = params.get("axis_type", "水平轴")  # 轴类型: 水平轴、重力轴、倾斜轴
        m = params.get("m")  # 质量 (kg)
        mb = params.get("mb", 0)  # 平衡质量 (kg)
        Fb = params.get("Fb", 0)  # 平衡力 (N)
        d = params.get("d")  # 丝杠直径 (mm)
        Pb = params.get("Pb")  # 丝杠导程 (mm/rev)
        l = params.get("l")  # 丝杠长度 (mm)
        z = params.get("z", 1)  # 减速比分母（减速比 = 1/z）
        J13 = params.get("J13", 0)  # 其他惯量 (kg·m²)
        u = params.get("u", 0.1)  # 摩擦系数
        Fc = params.get("Fc", 0)  # 切削力 (N)
        eta = params.get("eta", 0.9)  # 机械效率
        theta = params.get("theta", 0)  # 倾斜角 (°)
        V = params.get("V")  # 最大进给速度 (m/min)
        amax = params.get("amax")  # 最大加速度 (m/s²)
        
        # 电机参数（可选，用于选型确认）
        Jm = params.get("Jm")  # 电机惯量 (kg·m²)
        Ts = params.get("Ts")  # 电机扭矩 (N·m)
        Tmax_motor = params.get("Tmax_motor")  # 电机最大扭矩 (N·m)
        Nmax_motor = params.get("Nmax_motor")  # 电机最高转速 (rev/min)
        
        # 验证必需参数
        required_params = {"m": m, "d": d, "Pb": Pb, "l": l, "V": V, "amax": amax}
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        formula_parts = []
        intermediate_results = {}
        g = 9.8  # 重力加速度 (m/s²)
        
        # 单位转换
        d_m = d / 1000  # 丝杠直径 (m)
        Pb_m = Pb / 1000  # 丝杠导程 (m/rev)
        l_m = l / 1000  # 丝杠长度 (m)
        
        # 1. 电机一转移动量 P = Pb * (1/z)
        P = Pb_m * (1 / z)
        intermediate_results["P"] = P
        formula_parts.append(f"电机一转移动量: P = P<sub>b</sub> × (1/z) = {Pb_m:.6f} × (1/{z}) = {P:.6f} m/rev<br>")
        
        # 2. 电机最大转速 N = V / P
        N = round(V / P, 0)
        intermediate_results["N"] = N
        formula_parts.append(f"电机最大转速: N = V / P = {V} / {P:.6f} = {N:.0f} rev/min<br>")
        
        # 3. 质量折算惯量 J11 = m * (P/(2π))² + mb * (P/(2π))²
        J11 = m * (P / (2 * math.pi)) ** 2 + mb * (P / (2 * math.pi)) ** 2
        J11 = round(J11, 5)
        intermediate_results["J11"] = J11
        formula_parts.append(f"质量折算惯量: J<sub>11</sub> = m × (P/(2π))² + m<sub>b</sub> × (P/(2π))²<br>")
        formula_parts.append(f"  = {m} × ({P:.6f}/(2π))² + {mb} × ({P:.6f}/(2π))² = {J11:.5f} kg·m²<br>")
        
        # 4. 丝杠折算惯量 J12 = (π×ρ)/32 × d⁴ × l × (1/z)²
        J12 = (math.pi * self.STEEL_DENSITY) / 32 * (d_m ** 4) * l_m * ((1 / z) ** 2)
        J12 = round(J12, 4)
        intermediate_results["J12"] = J12
        formula_parts.append(f"丝杠折算惯量: J<sub>12</sub> = (π×ρ)/32 × d⁴ × l × (1/z)²<br>")
        formula_parts.append(f"  = (π×{self.STEEL_DENSITY})/32 × {d_m:.6f}⁴ × {l_m:.6f} × (1/{z})² = {J12:.4f} kg·m²<br>")
        
        # 5. 其他惯量 J13（直接使用输入值）
        intermediate_results["J13"] = J13
        if J13 > 0:
            formula_parts.append(f"其他惯量: J<sub>13</sub> = {J13} kg·m²<br>")
        
        # 6. 负载惯量 J1 = J11 + J12 + J13
        J1 = J11 + J12 + J13
        intermediate_results["J1"] = J1
        formula_parts.append(f"负载惯量: J<sub>1</sub> = J<sub>11</sub> + J<sub>12</sub> + J<sub>13</sub> = {J11:.5f} + {J12:.4f} + {J13} = {J1:.5f} kg·m²<br>")
        
        # 7. 摩擦扭矩 Tf（根据轴类型不同）
        if axis_type == "水平轴":
            Tf = (u * m * g * P) / (2 * math.pi * eta)
        elif axis_type == "倾斜轴":
            Tf = (u * m * g * math.cos(math.radians(theta)) * P) / (2 * math.pi * eta)
        else:  # 重力轴
            Tf = 0
        Tf = round(Tf, 4)
        intermediate_results["Tf"] = Tf
        if axis_type == "水平轴":
            formula_parts.append(f"<br>摩擦扭矩: T<sub>f</sub> = (u × m × g × P) / (2π × η)<br>")
            formula_parts.append(f"  = ({u} × {m} × {g} × {P:.6f}) / (2π × {eta}) = {Tf:.4f} N·m<br>")
        elif axis_type == "倾斜轴":
            formula_parts.append(f"<br>摩擦扭矩: T<sub>f</sub> = (u × m × g × cos(θ) × P) / (2π × η)<br>")
            formula_parts.append(f"  = ({u} × {m} × {g} × cos({theta}°) × {P:.6f}) / (2π × {eta}) = {Tf:.4f} N·m<br>")
        else:
            formula_parts.append(f"<br>摩擦扭矩: T<sub>f</sub> = 0 (重力轴不考虑摩擦扭矩)<br>")
        
        # 8. 重力扭矩 Tg（根据轴类型不同）
        if axis_type == "重力轴":
            Tg = ((m * g - Fb) * P) / (2 * math.pi * eta)
        elif axis_type == "倾斜轴":
            Tg = ((m * g * math.sin(math.radians(theta)) - Fb) * P) / (2 * math.pi * eta)
        else:  # 水平轴
            Tg = 0
        Tg = round(Tg, 4)
        intermediate_results["Tg"] = Tg
        if axis_type == "重力轴":
            formula_parts.append(f"重力扭矩: T<sub>g</sub> = ((m × g - F<sub>b</sub>) × P) / (2π × η)<br>")
            formula_parts.append(f"  = (({m} × {g} - {Fb}) × {P:.6f}) / (2π × {eta}) = {Tg:.4f} N·m<br>")
        elif axis_type == "倾斜轴":
            formula_parts.append(f"重力扭矩: T<sub>g</sub> = ((m × g × sin(θ) - F<sub>b</sub>) × P) / (2π × η)<br>")
            formula_parts.append(f"  = (({m} × {g} × sin({theta}°) - {Fb}) × {P:.6f}) / (2π × {eta}) = {Tg:.4f} N·m<br>")
        else:
            formula_parts.append(f"重力扭矩: T<sub>g</sub> = 0 (水平轴不考虑重力扭矩)<br>")
        
        # 9. 空载扭矩 Tm = Tf + Tg
        Tm = Tf + Tg
        intermediate_results["Tm"] = Tm
        formula_parts.append(f"空载扭矩: T<sub>m</sub> = T<sub>f</sub> + T<sub>g</sub> = {Tf:.4f} + {Tg:.4f} = {Tm:.4f} N·m<br>")
        
        # 10. 切削扭矩 Tc = Fc × P / (2π × η)
        Tc = (Fc * P) / (2 * math.pi * eta)
        Tc = round(Tc, 4)
        intermediate_results["Tc"] = Tc
        formula_parts.append(f"切削扭矩: T<sub>c</sub> = F<sub>c</sub> × P / (2π × η) = {Fc} × {P:.6f} / (2π × {eta}) = {Tc:.4f} N·m<br>")
        
        # 11. 负载扭矩 Tmc = Tm + Tc
        Tmc = Tm + Tc
        intermediate_results["Tmc"] = Tmc
        formula_parts.append(f"负载扭矩: T<sub>mc</sub> = T<sub>m</sub> + T<sub>c</sub> = {Tm:.4f} + {Tc:.4f} = {Tmc:.4f} N·m<br>")
        
        # 12. 加速扭矩 Tmax（根据轴类型不同）
        if axis_type == "水平轴":
            Tmax = J1 * 2 * math.pi * amax / P
        elif axis_type == "重力轴":
            Tmax = J1 * 2 * math.pi * amax / P + (m * g * P) / (2 * math.pi * eta)
        else:  # 倾斜轴
            Tmax = J1 * 2 * math.pi * amax / P + (m * g * math.sin(math.radians(theta)) * P) / (2 * math.pi * eta)
        Tmax = round(Tmax, 4)
        intermediate_results["Tmax"] = Tmax
        if axis_type == "水平轴":
            formula_parts.append(f"<br>加速扭矩: T<sub>max</sub> = J<sub>1</sub> × 2π × a<sub>max</sub> / P<br>")
            formula_parts.append(f"  = {J1:.5f} × 2π × {amax} / {P:.6f} = {Tmax:.4f} N·m<br>")
        elif axis_type == "重力轴":
            formula_parts.append(f"<br>加速扭矩: T<sub>max</sub> = J<sub>1</sub> × 2π × a<sub>max</sub> / P + (m × g × P) / (2π × η)<br>")
            formula_parts.append(f"  = {J1:.5f} × 2π × {amax} / {P:.6f} + ({m} × {g} × {P:.6f}) / (2π × {eta}) = {Tmax:.4f} N·m<br>")
        else:
            formula_parts.append(f"<br>加速扭矩: T<sub>max</sub> = J<sub>1</sub> × 2π × a<sub>max</sub> / P + (m × g × sin(θ) × P) / (2π × η)<br>")
            formula_parts.append(f"  = {J1:.5f} × 2π × {amax} / {P:.6f} + ({m} × {g} × sin({theta}°) × {P:.6f}) / (2π × {eta}) = {Tmax:.4f} N·m<br>")
        
        # 构建结果字典
        result = {
            "P": round(P, 6),
            "N": int(N),
            "J11": round(J11, 5),
            "J12": round(J12, 4),
            "J13": J13,
            "J1": round(J1, 5),
            "Tf": round(Tf, 4),
            "Tg": round(Tg, 4),
            "Tm": round(Tm, 4),
            "Tc": round(Tc, 4),
            "Tmc": round(Tmc, 4),
            "Tmax": round(Tmax, 4)
        }
        
        # 如果提供了电机参数，进行选型确认
        if Jm is not None and Jm > 0:
            # 负载惯量比
            inertia_ratio = (J1 / Jm) * 100
            result["inertia_ratio"] = round(inertia_ratio, 2)
            
            # 判定结论
            if inertia_ratio > 500:
                inertia_judgment = "不能满足零件加工设备的要求"
            elif inertia_ratio > 300:
                inertia_judgment = "不能满足模具加工或有频繁加减速的设备运动要求"
            else:
                inertia_judgment = "满足条件"
            result["inertia_judgment"] = inertia_judgment
            
            formula_parts.append(f"<br>负载惯量比: J<sub>1</sub>/J<sub>m</sub> × 100% = {J1:.5f}/{Jm} × 100% = {inertia_ratio:.2f}%<br>")
            formula_parts.append(f"判定: {inertia_judgment}<br>")
        
        if Ts is not None and Ts > 0:
            # 空载扭矩比率
            no_load_ratio = (Tm / Ts) * 100
            result["no_load_ratio"] = round(no_load_ratio, 2)
            
            # 判定结论
            if no_load_ratio > 30:
                no_load_judgment = "扭矩不能满足要求"
            else:
                no_load_judgment = "满足条件"
            result["no_load_judgment"] = no_load_judgment
            
            formula_parts.append(f"空载扭矩比率: T<sub>m</sub>/T<sub>s</sub> × 100% = {Tm:.4f}/{Ts} × 100% = {no_load_ratio:.2f}%<br>")
            formula_parts.append(f"判定: {no_load_judgment}<br>")
            
            # 负载扭矩比率
            load_ratio = (Tmc / Ts) * 100
            result["load_ratio"] = round(load_ratio, 2)
            
            # 判定结论
            if load_ratio > 85:
                load_judgment = "扭矩不能满足要求"
            else:
                load_judgment = "满足条件"
            result["load_judgment"] = load_judgment
            
            formula_parts.append(f"负载扭矩比率: T<sub>mc</sub>/T<sub>s</sub> × 100% = {Tmc:.4f}/{Ts} × 100% = {load_ratio:.2f}%<br>")
            formula_parts.append(f"判定: {load_judgment}<br>")
        
        if Nmax_motor is not None and Nmax_motor > 0:
            # 最高转速判定
            if N > Nmax_motor:
                speed_judgment = "电机转速不能满足要求，超出电机最高转速"
            else:
                speed_judgment = "满足条件"
            result["speed_judgment"] = speed_judgment
            
            formula_parts.append(f"最高转速判定: 需求转速 {N:.0f} rev/min，电机最高转速 {Nmax_motor} rev/min<br>")
            formula_parts.append(f"判定: {speed_judgment}<br>")
        
        if Tmax_motor is not None and Tmax_motor > 0:
            # 加速扭矩比率
            accel_ratio = (Tmax / Tmax_motor) * 100
            result["accel_ratio"] = round(accel_ratio, 2)
            
            # 判定结论
            if accel_ratio > 85:
                accel_judgment = "扭矩不能满足要求"
            else:
                accel_judgment = "满足条件"
            result["accel_judgment"] = accel_judgment
            
            formula_parts.append(f"加速扭矩比率: T<sub>max</sub>/T<sub>max_motor</sub> × 100% = {Tmax:.4f}/{Tmax_motor} × 100% = {accel_ratio:.2f}%<br>")
            formula_parts.append(f"判定: {accel_judgment}<br>")
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["servo_motor_params"]
        )

