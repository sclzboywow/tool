"""
风机选型计算服务
"""
import math
from typing import Dict, Any, List, Optional
from app.models.schemas import CurrentCalcResponse
from app.db.database import get_fan_performance


class FanSelectionCalculator:
    """风机选型计算器"""
    
    SCENARIO_NAMES = {
        "fan_selection": "风机选型计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算风机选型
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "fan_selection":
            return self._calculate_fan_selection(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_fan_selection(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """风机选型计算"""
        # 获取输入参数
        Q = params.get("Q")  # 流量(m³/h)
        P = params.get("P")  # 全压(Pa)
        H = params.get("H", 0)  # 海拔高度(m)
        P_inlet = params.get("P_inlet", 0)  # 进口压力(Pa)
        T = params.get("T")  # 工作温度(℃)
        k = params.get("k", 1.4)  # 绝热指数
        n = params.get("n")  # 工作转速(rpm)
        fan_type = params.get("fan_type", "4-68")  # 风机型号
        D = params.get("D")  # 给定叶轮直径(m)
        suction_type = params.get("suction_type", "单吸")  # 单吸/双吸
        rho_standard = params.get("rho_standard", 1.2)  # 标准密度(kg/m³)
        
        # 性能参数（如果提供，则使用；否则从数据库查找）
        performance_points = params.get("performance_points")  # 性能点列表，每个点包含phi, psi_p, eta
        
        # 验证必需参数
        if Q is None or Q <= 0:
            raise ValueError("流量Q必须大于0")
        if P is None or P <= 0:
            raise ValueError("全压P必须大于0")
        if T is None:
            raise ValueError("工作温度T必须提供")
        if n is None or n <= 0:
            raise ValueError("工作转速n必须大于0")
        if D is None or D <= 0:
            raise ValueError("叶轮直径D必须大于0")
        if k <= 1:
            raise ValueError("绝热指数k必须大于1")
        
        formula_parts = []
        intermediate_results = {}
        
        # 1. 计算当地大气压 P_atm = 101325 × (1 - 0.02257 × H/1000)^5.256
        P_atm = 101325 * ((1 - 0.02257 * H / 1000) ** 5.256)
        intermediate_results["P_atm"] = P_atm
        formula_parts.append(f"当地大气压: P<sub>atm</sub> = 101325 × (1 - 0.02257 × H/1000)^5.256<br>")
        formula_parts.append(f"  = 101325 × (1 - 0.02257 × {H}/1000)^5.256 = {P_atm:.2f} Pa")
        
        # 2. 计算工况密度 rho_working = (273/(273+T)) × (P_atm + P_inlet)/101325 × rho_standard
        T_K = T + 273  # 转换为开尔文
        rho_working = (273 / T_K) * ((P_atm + P_inlet) / 101325) * rho_standard
        intermediate_results["rho_working"] = rho_working
        formula_parts.append(f"<br>工况密度: ρ<sub>working</sub> = (273/(273+T)) × (P<sub>atm</sub> + P<sub>inlet</sub>)/101325 × ρ<sub>standard</sub><br>")
        formula_parts.append(f"  = (273/(273+{T})) × ({P_atm:.2f} + {P_inlet})/101325 × {rho_standard} = {rho_working:.6f} kg/m³")
        
        # 3. 计算压缩性系数 Z = (k/(k-1)) × ((1 + P/(P_atm + P_inlet))^((k-1)/k) - 1) × (P/(P_atm + P_inlet))^(-1)
        P_total = P_atm + P_inlet
        if P_total <= 0:
            raise ValueError("当地大气压与进口压力之和必须大于0")
        pressure_ratio = P / P_total
        Z = (k / (k - 1)) * (((1 + pressure_ratio) ** ((k - 1) / k)) - 1) * (pressure_ratio ** (-1))
        intermediate_results["Z"] = Z
        formula_parts.append(f"<br>压缩性系数: Z = (k/(k-1)) × ((1 + P/(P<sub>atm</sub> + P<sub>inlet</sub>))^((k-1)/k) - 1) × (P/(P<sub>atm</sub> + P<sub>inlet</sub>))^(-1)<br>")
        formula_parts.append(f"  = ({k}/({k}-1)) × ((1 + {P}/({P_atm:.2f} + {P_inlet}))^(({k}-1)/{k}) - 1) × ({P}/({P_atm:.2f} + {P_inlet}))^(-1) = {Z:.6f}")
        
        # 4. 计算比转数 ns = 5.54 × n × (Q/3600)^0.5 / (P × 1.2/rho_working)^0.75
        ns = 5.54 * n * ((Q / 3600) ** 0.5) / ((P * 1.2 / rho_working) ** 0.75)
        intermediate_results["ns"] = ns
        formula_parts.append(f"<br>比转数: n<sub>s</sub> = 5.54 × n × (Q/3600)^0.5 / (P × 1.2/ρ<sub>working</sub>)^0.75<br>")
        formula_parts.append(f"  = 5.54 × {n} × ({Q}/3600)^0.5 / ({P} × 1.2/{rho_working:.6f})^0.75 = {ns:.2f}")
        
        # 5. 获取性能点数据
        if performance_points and len(performance_points) > 0:
            # 使用用户提供的性能点
            points = performance_points
        else:
            # 从SQLite数据库查询
            db_points = get_fan_performance(fan_type)
            if db_points and len(db_points) > 0:
                points = db_points
            else:
                raise ValueError(f"未找到风机型号 {fan_type} 的性能数据，请提供性能点数据或确保数据库中已导入该型号的数据")
        
        # 6. 计算每个性能点的参数
        u = math.pi * D * n / 60  # 线速度 (m/s)
        intermediate_results["u"] = u
        formula_parts.append(f"<br>线速度: u = π × D × n/60 = π × {D} × {n}/60 = {u:.2f} m/s")
        
        # 判断是否为双吸
        is_double_suction = (suction_type == "双吸")
        suction_factor = 2 if is_double_suction else 1
        
        # 计算每个性能点
        performance_results = []
        formula_parts.append(f"<br><br>性能点计算:")
        
        for idx, point in enumerate(points, 1):
            phi = point.get("phi")
            psi_p = point.get("psi_p")
            eta = point.get("eta")
            
            if phi is None or psi_p is None or eta is None:
                continue
            
            # 计算流量 Q = phi × π/4 × D² × π × D × n/60 × 3600 × suction_factor
            Q_point = phi * (math.pi / 4) * (D ** 2) * math.pi * D * n / 60 * 3600 * suction_factor
            intermediate_results[f"Q_{idx}"] = Q_point
            
            # 计算全压
            # 对于BB24和BB50型号，需要特殊处理
            if fan_type in ["BB24", "BB50"]:
                P_point = psi_p * rho_working * (u ** 2) / Z * 0.9784
            else:
                P_point = psi_p * rho_working * (u ** 2)
            intermediate_results[f"P_{idx}"] = P_point
            
            # 计算内功率 P_internal = Q/3600 × P / eta / 10
            P_internal = (Q_point / 3600) * P_point / (eta / 100) / 10
            intermediate_results[f"P_internal_{idx}"] = P_internal
            
            # 计算轴功率 P_shaft = P_internal/0.98 × 1.15 (T<200℃) 或 × 1.3 (T≥200℃)
            if T < 200:
                P_shaft = P_internal / 0.98 * 1.15
            else:
                P_shaft = P_internal / 0.98 * 1.3
            intermediate_results[f"P_shaft_{idx}"] = P_shaft
            
            performance_results.append({
                "序号": idx,
                "流量": round(Q_point, 2),
                "全压": round(P_point, 2),
                "内效率": round(eta, 1),
                "内功率": round(P_internal, 2),
                "轴功率": round(P_shaft, 2)
            })
            
            formula_parts.append(f"<br>点{idx}: Q = {phi} × π/4 × {D}² × π × {D} × {n}/60 × 3600 × {suction_factor} = {Q_point:.2f} m³/h")
            formula_parts.append(f"<br>  P = {psi_p} × {rho_working:.6f} × {u:.2f}² = {P_point:.2f} Pa")
            formula_parts.append(f"<br>  P<sub>internal</sub> = {Q_point:.2f}/3600 × {P_point:.2f} / ({eta}/100) / 10 = {P_internal:.2f} kW")
            formula_parts.append(f"<br>  P<sub>shaft</sub> = {P_internal:.2f}/0.98 × {'1.15' if T < 200 else '1.3'} = {P_shaft:.2f} kW")
        
        # 7. 粗算叶轮直径（需要psi_p，使用第一个性能点的psi_p）
        if len(points) > 0:
            psi_p_first = points[0].get("psi_p")
            if psi_p_first:
                D_rough = 27 / n * ((P / 2 / rho_working / psi_p_first) ** 0.5)
                intermediate_results["D_rough"] = D_rough
                formula_parts.append(f"<br><br>粗算叶轮直径: D<sub>rough</sub> = 27/n × (P/2/ρ<sub>working</sub>/ψ<sub>p</sub>)^0.5<br>")
                formula_parts.append(f"  = 27/{n} × ({P}/2/{rho_working:.6f}/{psi_p_first})^0.5 = {D_rough:.4f} m")
        
        # 构建选型结果
        fan_model = f"{fan_type}№{int(D * 10)}"
        intermediate_results["fan_model"] = fan_model
        
        # 构建完整的公式字符串
        formula = "".join(formula_parts)
        
        # 构建结果字典
        result = {
            "P_atm": round(P_atm, 2),
            "rho_working": round(rho_working, 6),
            "Z": round(Z, 6),
            "ns": round(ns, 2),
            "u": round(u, 2),
            "fan_model": fan_model,
            "D_rough": round(intermediate_results.get("D_rough", 0), 4) if "D_rough" in intermediate_results else None,
            "performance_points": performance_results
        }
        
        return CurrentCalcResponse(
            result=result,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["fan_selection"]
        )

