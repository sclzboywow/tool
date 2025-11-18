"""
风机选型计算举例服务（锅炉送风机选型计算）
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class FanSelectionExampleCalculator:
    """风机选型计算举例计算器（锅炉送风机选型）"""
    
    SCENARIO_NAMES = {
        "fan_selection_example": "风机选型计算举例"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算风机选型举例
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "fan_selection_example":
            return self._calculate_fan_selection_example(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_fan_selection_example(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """风机选型计算举例（锅炉送风机选型）"""
        # 获取煤质参数
        Car = params.get("Car")  # 应用基碳 (%)
        OAR = params.get("OAR")  # 应用基氧 (%)
        Hy = params.get("Hy")  # 应用基氢 (%)
        Nar = params.get("Nar")  # 应用基氮 (%)
        War = params.get("War")  # 全水 (%)
        Aar = params.get("Aar")  # 应用基灰 (%)
        Sar = params.get("Sar")  # 全硫 (%)
        Vdaf = params.get("Vdaf")  # 挥发份 (%)
        Qnet_ar = params.get("Qnet_ar")  # 低位发热量 (kJ/kg)
        
        # 获取其他参数
        alpha = params.get("alpha", 1.2)  # 过量空气系数
        tk = params.get("tk", 20)  # 空气温度 (°C)
        tg = params.get("tg", 20)  # 烟气温度 (°C)
        b = params.get("b")  # 当地大气压 (kPa)
        k1 = params.get("k1", 1.15)  # 送风机风量储备系数
        k2_primary = params.get("k2_primary", 1.2)  # 一次风机风压储备系数
        k2_secondary = params.get("k2_secondary", 1.25)  # 二次风机风压储备系数
        delta_h_primary = params.get("delta_h_primary")  # 一次风机总阻力 (Pa)
        delta_h_secondary = params.get("delta_h_secondary")  # 二次风机总阻力 (Pa)
        eta1 = params.get("eta1", 0.85)  # 风机效率
        eta2 = params.get("eta2", 0.98)  # 机械效率
        eta3 = params.get("eta3", 0.9)  # 电动机效率
        K_motor = params.get("K_motor", 1.1)  # 电动机备用系数
        
        # 燃煤量相关参数（如果需要计算）
        B = params.get("B")  # 燃煤量 (t/h)，如果提供则直接使用
        B_calculated = False
        B_t_h = None
        # 或者通过其他参数计算
        if B is None:
            # 通过锅炉参数计算燃煤量
            D = params.get("D")  # 锅炉蒸发量 (t/h)
            h_main = params.get("h_main")  # 主蒸汽焓 (kJ/kg)
            h_feed = params.get("h_feed")  # 给水焓 (kJ/kg)
            blowdown = params.get("blowdown", 0.02)  # 排污率
            h_blowdown = params.get("h_blowdown", 1491)  # 排污水焓 (kJ/kg)
            eta_boiler = params.get("eta_boiler", 0.89)  # 锅炉效率
            
            if D is None or h_main is None or h_feed is None:
                raise ValueError("燃煤量B必须提供，或提供计算燃煤量所需的参数(D, h_main, h_feed)")
            
            # B = (D*(h_main-h_feed) + D*blowdown*(h_blowdown-h_feed)) / (eta*Qnet_ar)
            # Excel中的B单位是t/h，不是kg/s
            B = (D * (h_main - h_feed) + D * blowdown * (h_blowdown - h_feed)) / (eta_boiler * Qnet_ar)  # t/h
            B_calculated = True
        
        # 验证必需参数（B已经处理过了）
        required_params = {
            "Car": Car, "OAR": OAR, "Hy": Hy, "Nar": Nar,
            "War": War, "Aar": Aar, "Sar": Sar, "Qnet_ar": Qnet_ar,
            "b": b
        }
        
        for name, value in required_params.items():
            if value is None:
                raise ValueError(f"参数{name}必须提供")
        
        if B is None:
            raise ValueError("燃煤量B必须提供或通过锅炉参数计算")
        
        formula_parts = []
        intermediate_results = {}
        
        # 0. 燃煤量计算（如果需要）
        if B_calculated:
            D = params.get("D")
            h_main = params.get("h_main")
            h_feed = params.get("h_feed")
            blowdown = params.get("blowdown", 0.02)
            h_blowdown = params.get("h_blowdown", 1491)
            eta_boiler = params.get("eta_boiler", 0.89)
            formula_parts.append(f"燃煤量: B = (D×(h<sub>main</sub>-h<sub>feed</sub>) + D×blowdown×(h<sub>blowdown</sub>-h<sub>feed</sub>)) / (η×Q<sub>net.ar</sub>)<br>")
            formula_parts.append(f"  = ({D}×({h_main}-{h_feed}) + {D}×{blowdown}×({h_blowdown}-{h_feed})) / ({eta_boiler}×{Qnet_ar}) = {B:.6f} t/h<br>")
        
        # 1. 计算燃烧空气量 Vo = 0.0889*(Car+0.375*Sar)+0.265*Hy-0.033*OAR
        Vo = 0.0889 * (Car + 0.375 * Sar) + 0.265 * Hy - 0.033 * OAR
        intermediate_results["Vo"] = Vo
        formula_parts.append(f"燃烧空气量: V<sub>o</sub> = 0.0889×(C<sub>ar</sub>+0.375×S<sub>ar</sub>)+0.265×H<sub>y</sub>-0.033×O<sub>AR</sub><br>")
        formula_parts.append(f"  = 0.0889×({Car}+0.375×{Sar})+0.265×{Hy}-0.033×{OAR} = {Vo:.6f} Nm³/kg")
        
        # 2. 计算理论烟气量
        # 2.1 VRO2 = 1.866*Car/100+0.7*Sar/100
        VRO2 = 1.866 * Car / 100 + 0.7 * Sar / 100
        intermediate_results["VRO2"] = VRO2
        formula_parts.append(f"<br>CO<sub>2</sub>和SO<sub>2</sub>产生量: V<sub>RO2</sub> = 1.866×C<sub>ar</sub>/100+0.7×S<sub>ar</sub>/100<br>")
        formula_parts.append(f"  = 1.866×{Car}/100+0.7×{Sar}/100 = {VRO2:.6f} Nm³/kg")
        
        # 2.2 VN2 = 0.8*Nar/100+0.79*Vo
        VN2 = 0.8 * Nar / 100 + 0.79 * Vo
        intermediate_results["VN2"] = VN2
        formula_parts.append(f"<br>含氮量: V<sub>N2</sub> = 0.8×N<sub>ar</sub>/100+0.79×V<sub>o</sub><br>")
        formula_parts.append(f"  = 0.8×{Nar}/100+0.79×{Vo:.6f} = {VN2:.6f} Nm³/kg")
        
        # 2.3 VH2Oo = 0.0124*War+0.111*Hy+0.00161*10*Vo
        VH2Oo = 0.0124 * War + 0.111 * Hy + 0.00161 * 10 * Vo
        intermediate_results["VH2Oo"] = VH2Oo
        formula_parts.append(f"<br>理论水蒸气含量: V<sub>H2Oo</sub> = 0.0124×W<sub>ar</sub>+0.111×H<sub>y</sub>+0.00161×10×V<sub>o</sub><br>")
        formula_parts.append(f"  = 0.0124×{War}+0.111×{Hy}+0.00161×10×{Vo:.6f} = {VH2Oo:.6f} Nm³/kg")
        
        # 2.4 Vyo = VRO2+VN2+VH2Oo
        Vyo = VRO2 + VN2 + VH2Oo
        intermediate_results["Vyo"] = Vyo
        formula_parts.append(f"<br>理论烟气量: V<sub>yo</sub> = V<sub>RO2</sub>+V<sub>N2</sub>+V<sub>H2Oo</sub><br>")
        formula_parts.append(f"  = {VRO2:.6f}+{VN2:.6f}+{VH2Oo:.6f} = {Vyo:.6f} Nm³/kg")
        
        # 3. 计算实际烟气量
        # 3.1 过量N2 = 0.79*(α-1)*Vo
        VN2_excess = 0.79 * (alpha - 1) * Vo
        intermediate_results["VN2_excess"] = VN2_excess
        
        # 3.2 过量O2 = 0.21*(α-1)*Vo
        VO2_excess = 0.21 * (alpha - 1) * Vo
        intermediate_results["VO2_excess"] = VO2_excess
        
        # 3.3 过量H2O = 0.00161*10*(α-1)*Vo
        VH2O_excess = 0.00161 * 10 * (alpha - 1) * Vo
        intermediate_results["VH2O_excess"] = VH2O_excess
        
        # 3.4 Vy = Vyo + 过量O2 + 过量N2 + 过量H2O
        Vy = Vyo + VO2_excess + VN2_excess + VH2O_excess
        intermediate_results["Vy"] = Vy
        formula_parts.append(f"<br>实际烟气量: V<sub>y</sub> = V<sub>yo</sub>+过量O<sub>2</sub>+过量N<sub>2</sub>+过量H<sub>2</sub>O<br>")
        formula_parts.append(f"  = {Vyo:.6f}+{VO2_excess:.6f}+{VN2_excess:.6f}+{VH2O_excess:.6f} = {Vy:.6f} Nm³/kg")
        
        # 4. 计算送风机选型风量
        # Excel中使用的是C72 = B*(100-3.68)/100（飞灰量），而不是直接使用B
        # Vg = k1*C72*1000*α*Vo*(273+tk)*101/(273*b)
        # 其中C72 = B*(100-3.68)/100
        B_corrected = B * (100 - 3.68) / 100  # 对应Excel中的C72
        Vg = k1 * B_corrected * 1000 * alpha * Vo * (273 + tk) * 101 / (273 * b)
        intermediate_results["Vg"] = Vg
        formula_parts.append(f"<br>送风机风量: V<sub>g</sub> = k<sub>1</sub>×B×1000×α×V<sub>o</sub>×(273+t<sub>k</sub>)×101/(273×b)<br>")
        formula_parts.append(f"  = {k1}×{B}×1000×{alpha}×{Vo:.6f}×(273+{tk})×101/(273×{b}) = {Vg:.2f} m³/h")
        
        # 一次风量和二次风量
        Vg_primary = Vg * 0.6
        Vg_secondary = Vg * 0.4
        intermediate_results["Vg_primary"] = Vg_primary
        intermediate_results["Vg_secondary"] = Vg_secondary
        formula_parts.append(f"<br>一次风量: V<sub>g1</sub> = V<sub>g</sub>×0.6 = {Vg:.2f}×0.6 = {Vg_primary:.2f} m³/h")
        formula_parts.append(f"<br>二次风量: V<sub>g2</sub> = V<sub>g</sub>×0.4 = {Vg:.2f}×0.4 = {Vg_secondary:.2f} m³/h")
        
        # 5. 计算送风机选型阻力
        # Excel中的公式: Hg = K2*∑Δh*((273+tk)/(273+tg))*(101/b)*(1.293/ρko)
        # 当tk=tg且使用标准值(101, 1.293)时，公式简化为: Hg = K2*∑Δh
        # 但为了匹配Excel的实际计算，当tk=tg时使用简化公式
        rho_ko = params.get("rho_ko", 1.293)  # 空气密度 (kg/m³)
        
        # 一次风机阻力
        if delta_h_primary is None:
            raise ValueError("一次风机总阻力delta_h_primary必须提供")
        # Excel中当tk=tg时，公式简化为: Hg = K2*∑Δh
        if abs(tk - tg) < 0.1:  # tk和tg相等或接近
            Hg_primary = k2_primary * delta_h_primary
            formula_parts.append(f"<br><br>一次风机阻力: H<sub>g1</sub> = K<sub>2</sub>×∑Δh (当t<sub>k</sub>=t<sub>g</sub>时简化)<br>")
            formula_parts.append(f"  = {k2_primary}×{delta_h_primary} = {Hg_primary:.2f} Pa")
        else:
            Hg_primary = k2_primary * delta_h_primary * ((273 + tk) / (273 + tg)) * (101 / b) * (1.293 / rho_ko)
            formula_parts.append(f"<br><br>一次风机阻力: H<sub>g1</sub> = K<sub>2</sub>×∑Δh×((273+t<sub>k</sub>)/(273+t<sub>g</sub>))×(101/b)×(1.293/ρ<sub>ko</sub>)<br>")
            formula_parts.append(f"  = {k2_primary}×{delta_h_primary}×((273+{tk})/(273+{tg}))×(101/{b})×(1.293/{rho_ko}) = {Hg_primary:.2f} Pa")
        intermediate_results["Hg_primary"] = Hg_primary
        
        # 二次风机阻力
        if delta_h_secondary is None:
            raise ValueError("二次风机总阻力delta_h_secondary必须提供")
        # Excel中当tk=tg时，公式简化为: Hg = K2*∑Δh
        if abs(tk - tg) < 0.1:  # tk和tg相等或接近
            Hg_secondary = k2_secondary * delta_h_secondary
            formula_parts.append(f"<br>二次风机阻力: H<sub>g2</sub> = K<sub>2</sub>×∑Δh (当t<sub>k</sub>=t<sub>g</sub>时简化)<br>")
            formula_parts.append(f"  = {k2_secondary}×{delta_h_secondary} = {Hg_secondary:.2f} Pa")
        else:
            Hg_secondary = k2_secondary * delta_h_secondary * ((273 + tk) / (273 + tg)) * (101 / b) * (1.293 / rho_ko)
            formula_parts.append(f"<br>二次风机阻力: H<sub>g2</sub> = K<sub>2</sub>×∑Δh×((273+t<sub>k</sub>)/(273+t<sub>g</sub>))×(101/b)×(1.293/ρ<sub>ko</sub>)<br>")
            formula_parts.append(f"  = {k2_secondary}×{delta_h_secondary}×((273+{tk})/(273+{tg}))×(101/{b})×(1.293/{rho_ko}) = {Hg_secondary:.2f} Pa")
        intermediate_results["Hg_secondary"] = Hg_secondary
        
        # 6. 计算电动机功率
        # Ng = K*Vg*Hg/(3600*9.81*102*η1*η2*η3)
        Ng_primary = K_motor * Vg_primary * Hg_primary / (3600 * 9.81 * 102 * eta1 * eta2 * eta3)
        intermediate_results["Ng_primary"] = Ng_primary
        formula_parts.append(f"<br><br>一次风机电动机功率: N<sub>g1</sub> = K×V<sub>g1</sub>×H<sub>g1</sub>/(3600×9.81×102×η<sub>1</sub>×η<sub>2</sub>×η<sub>3</sub>)<br>")
        formula_parts.append(f"  = {K_motor}×{Vg_primary:.2f}×{Hg_primary:.2f}/(3600×9.81×102×{eta1}×{eta2}×{eta3}) = {Ng_primary:.2f} kW")
        
        Ng_secondary = K_motor * Vg_secondary * Hg_secondary / (3600 * 9.81 * 102 * eta1 * eta2 * eta3)
        intermediate_results["Ng_secondary"] = Ng_secondary
        formula_parts.append(f"<br>二次风机电动机功率: N<sub>g2</sub> = K×V<sub>g2</sub>×H<sub>g2</sub>/(3600×9.81×102×η<sub>1</sub>×η<sub>2</sub>×η<sub>3</sub>)<br>")
        formula_parts.append(f"  = {K_motor}×{Vg_secondary:.2f}×{Hg_secondary:.2f}/(3600×9.81×102×{eta1}×{eta2}×{eta3}) = {Ng_secondary:.2f} kW")
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        # 构建结果字典
        result = {
            "Vo": round(Vo, 6),
            "VRO2": round(VRO2, 6),
            "VN2": round(VN2, 6),
            "VH2Oo": round(VH2Oo, 6),
            "Vyo": round(Vyo, 6),
            "VN2_excess": round(VN2_excess, 6),
            "VO2_excess": round(VO2_excess, 6),
            "VH2O_excess": round(VH2O_excess, 6),
            "Vy": round(Vy, 6),
            "B": round(B, 6),  # 添加B到结果中
            "Vg": round(Vg, 2),
            "Vg_primary": round(Vg_primary, 2),
            "Vg_secondary": round(Vg_secondary, 2),
            "Hg_primary": round(Hg_primary, 2),
            "Hg_secondary": round(Hg_secondary, 2),
            "Ng_primary": round(Ng_primary, 2),
            "Ng_secondary": round(Ng_secondary, 2)
        }
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["fan_selection_example"]
        )

