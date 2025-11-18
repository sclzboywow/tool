"""
鼓风机选型计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class BlowerSelectionCalculator:
    """鼓风机选型计算器"""
    
    SCENARIO_NAMES = {
        "blower_selection": "鼓风机选型计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算鼓风机选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "blower_selection":
            return self._calculate_blower_selection(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_blower_selection(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """鼓风机选型计算"""
        # 获取输入参数
        Pd = params.get("Pd")  # 高炉炉顶压力(MPa)
        delta_P1 = params.get("delta_P1")  # 高炉送风系统阻力(MPa)
        delta_Pf = params.get("delta_Pf")  # 高炉送风管路阻力(MPa)
        P0 = params.get("P0")  # 标准大气压(MPa)
        delta_Px = params.get("delta_Px")  # 风机入口阻力(MPa)
        Vu = params.get("Vu")  # 高炉有效容积(m³)
        i = params.get("i")  # 高炉利用系数(t/m³.d)
        q = params.get("q")  # 单位生铁耗风量(m³/t)
        delta = params.get("delta")  # 高炉漏风率(%)
        Qf = params.get("Qf")  # 高炉送风管路漏风量(m³/h)
        PX = params.get("PX")  # 风机入口实际大气压(Pa)
        T0 = params.get("T0")  # 标准温度(K)
        Ta = params.get("Ta")  # 风机入口实际温度(K)
        PZ = params.get("PZ")  # 风机入口水蒸气分压(Pa)
        Pa = params.get("Pa")  # 风机入口大气压(Pa)
        k = params.get("k")  # 绝热指数
        eta_n = params.get("eta_n")  # 内效率
        eta_m = params.get("eta_m")  # 机械效率
        
        # 验证必需参数
        required_params = {
            "Pd": Pd, "delta_P1": delta_P1, "delta_Pf": delta_Pf,
            "P0": P0, "Vu": Vu, "i": i, "q": q, "delta": delta,
            "PX": PX, "T0": T0, "Ta": Ta, "PZ": PZ, "Pa": Pa,
            "k": k, "eta_n": eta_n, "eta_m": eta_m
        }
        
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        # delta_Px和Qf可以为0，但需要设置默认值
        if delta_Px is None:
            delta_Px = 0
        if Qf is None:
            Qf = 0
        
        # 验证参数范围
        if P0 <= 0:
            raise ValueError("标准大气压P0必须大于0")
        if Vu <= 0:
            raise ValueError("高炉有效容积Vu必须大于0")
        if i <= 0:
            raise ValueError("高炉利用系数i必须大于0")
        if q <= 0:
            raise ValueError("单位生铁耗风量q必须大于0")
        if delta < 0 or delta > 100:
            raise ValueError("高炉漏风率delta应在0-100%之间")
        if T0 <= 0:
            raise ValueError("标准温度T0必须大于0")
        if Ta <= 0:
            raise ValueError("风机入口实际温度Ta必须大于0")
        if PX <= 0:
            raise ValueError("风机入口实际大气压PX必须大于0")
        if Pa <= 0:
            raise ValueError("风机入口大气压Pa必须大于0")
        if k <= 1:
            raise ValueError("绝热指数k必须大于1")
        if eta_n <= 0 or eta_n > 1:
            raise ValueError("内效率eta_n应在0-1之间")
        if eta_m <= 0 or eta_m > 1:
            raise ValueError("机械效率eta_m应在0-1之间")
        
        formula_parts = []
        intermediate_results = {}
        
        # 1. 计算高炉所需风压 Pc = Pd + delta_P1 + delta_Pf
        Pc = Pd + delta_P1 + delta_Pf
        intermediate_results["Pc"] = Pc
        formula_parts.append(f"高炉所需风压: P<sub>c</sub> = P<sub>d</sub> + ΔP<sub>1</sub> + ΔP<sub>f</sub> = {Pd} + {delta_P1} + {delta_Pf} = {Pc:.6f} MPa")
        
        # 2. 计算风机入口压力 Pfx = P0 - delta_Px
        Pfx = P0 - delta_Px
        intermediate_results["Pfx"] = Pfx
        formula_parts.append(f"风机入口压力: P<sub>fx</sub> = P<sub>0</sub> - ΔP<sub>x</sub> = {P0} - {delta_Px} = {Pfx:.6f} MPa")
        
        # 3. 计算风机出口风压 Ph = P0 + Pc
        Ph = P0 + Pc
        intermediate_results["Ph"] = Ph
        formula_parts.append(f"风机出口风压: P<sub>h</sub> = P<sub>0</sub> + P<sub>c</sub> = {P0} + {Pc:.6f} = {Ph:.6f} MPa")
        
        # 4. 计算压比 epsilon = Ph / Pfx
        if Pfx <= 0:
            raise ValueError("风机入口压力Pfx必须大于0")
        epsilon = Ph / Pfx
        intermediate_results["epsilon"] = epsilon
        formula_parts.append(f"压比: ε = P<sub>h</sub> / P<sub>fx</sub> = {Ph:.6f} / {Pfx:.6f} = {epsilon:.6f}")
        
        # 5. 计算高炉入炉风量 Qg = Vu * i * q / 1440
        Qg = Vu * i * q / 1440
        intermediate_results["Qg"] = Qg
        formula_parts.append(f"高炉入炉风量: Q<sub>g</sub> = V<sub>u</sub> × i × q / 1440 = {Vu} × {i} × {q} / 1440 = {Qg:.2f} m³/h")
        
        # 6. 计算风机出口风量1 Q2 = (1 + delta/100) * Qg
        Q2 = (1 + delta / 100) * Qg
        intermediate_results["Q2"] = Q2
        formula_parts.append(f"风机出口风量1: Q<sub>2</sub> = (1 + δ/100) × Q<sub>g</sub> = (1 + {delta}/100) × {Qg:.2f} = {Q2:.2f} m³/h")
        
        # 7. 计算风机出口风量2 Q3 = Q2 + Qf
        Q3 = Q2 + Qf
        intermediate_results["Q3"] = Q3
        formula_parts.append(f"风机出口风量2: Q<sub>3</sub> = Q<sub>2</sub> + Q<sub>f</sub> = {Q2:.2f} + {Qf} = {Q3:.2f} m³/h")
        
        # 8. 计算气压修正系数 K1 = PX / (P0 * 1000000)
        # 注意：PX是Pa，P0是MPa，需要统一单位
        P0_Pa = P0 * 1000000  # 转换为Pa
        K1 = PX / P0_Pa
        intermediate_results["K1"] = K1
        formula_parts.append(f"气压修正系数: K<sub>1</sub> = P<sub>X</sub> / P<sub>0</sub> = {PX} / {P0_Pa:.2f} = {K1:.6f}")
        
        # 9. 计算气温修正系数 K2 = T0 / Ta
        K2 = T0 / Ta
        intermediate_results["K2"] = K2
        formula_parts.append(f"气温修正系数: K<sub>2</sub> = T<sub>0</sub> / T<sub>a</sub> = {T0} / {Ta} = {K2:.6f}")
        
        # 10. 计算湿度修正系数 K3 = 1 - PZ / Pa
        if PZ >= Pa:
            raise ValueError("风机入口水蒸气分压PZ必须小于风机入口大气压Pa")
        K3 = 1 - PZ / Pa
        intermediate_results["K3"] = K3
        formula_parts.append(f"湿度修正系数: K<sub>3</sub> = 1 - P<sub>Z</sub> / P<sub>a</sub> = 1 - {PZ} / {Pa} = {K3:.6f}")
        
        # 11. 计算风量修正系数 K = K1 * K2 * K3
        K = K1 * K2 * K3
        intermediate_results["K"] = K
        formula_parts.append(f"风量修正系数: K = K<sub>1</sub> × K<sub>2</sub> × K<sub>3</sub> = {K1:.6f} × {K2:.6f} × {K3:.6f} = {K:.6f}")
        
        # 12. 计算实际送风量 Q = Q3 / K / 60 (转换为m³/min)
        if K <= 0:
            raise ValueError("风量修正系数K必须大于0")
        Q = Q3 / K / 60  # 转换为m³/min
        intermediate_results["Q"] = Q
        formula_parts.append(f"实际送风量: Q = Q<sub>3</sub> / K / 60 = {Q3:.2f} / {K:.6f} / 60 = {Q:.2f} m³/min")
        
        # 13. 计算鼓风机轴功率 Ne = 101937 * Pfx * Q * (epsilon^(1/k) - 1) / 6120 / eta_n / eta_m
        # 注意：Excel公式是 =101937*E15*E45*E48*(E17^(1/E50)-1)/6120/E46
        # 其中E48 = k/(k-1)，但实际计算中应该用 epsilon^(1/k)
        # 根据Excel公式，应该是 epsilon^(1/k) - 1
        epsilon_power = epsilon ** (1 / k)
        power_term = epsilon_power - 1
        
        # 将Pfx从MPa转换为Pa，Q从m³/min转换为m³/h
        Pfx_Pa = Pfx * 1000000  # MPa转Pa
        Q_m3h = Q * 60  # m³/min转m³/h
        
        # 根据Excel公式：Ne = 101937 * Pfx(MPa) * Q(m³/min) * (epsilon^(1/k) - 1) / 6120 / eta_n
        # 但Excel中E45是Q(m³/min)，E15是Pfx(MPa)
        Ne = 101937 * Pfx * Q * power_term / 6120 / eta_n / eta_m
        intermediate_results["Ne"] = Ne
        formula_parts.append(f"鼓风机轴功率: N<sub>e</sub> = 101937 × P<sub>fx</sub> × Q × (ε^(1/k) - 1) / 6120 / η<sub>n</sub> / η<sub>m</sub>")
        formula_parts.append(f"  = 101937 × {Pfx:.6f} × {Q:.2f} × ({epsilon:.6f}^(1/{k}) - 1) / 6120 / {eta_n} / {eta_m}")
        formula_parts.append(f"  = 101937 × {Pfx:.6f} × {Q:.2f} × {power_term:.6f} / 6120 / {eta_n} / {eta_m}")
        formula_parts.append(f"  = {Ne:.2f} kW")
        
        # 构建完整的公式字符串
        formula = "<br>".join(formula_parts)
        
        # 构建结果字典
        result = {
            "Pc": round(Pc, 6),
            "Pfx": round(Pfx, 6),
            "Ph": round(Ph, 6),
            "epsilon": round(epsilon, 6),
            "Qg": round(Qg, 2),
            "Q2": round(Q2, 2),
            "Q3": round(Q3, 2),
            "K1": round(K1, 6),
            "K2": round(K2, 6),
            "K3": round(K3, 6),
            "K": round(K, 6),
            "Q": round(Q, 2),
            "Ne": round(Ne, 2)
        }
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["blower_selection"]
        )

