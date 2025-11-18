"""
风机性能表计算服务
"""
import math
from typing import Dict, Any, List
from app.models.schemas import CurrentCalcResponse


class FanPerformanceCalculator:
    """风机性能表计算器"""
    
    SCENARIO_NAMES = {
        "fan_performance": "风机性能表计算",
        "air_density": "空气密度计算",
        "pressure": "压力计算",
        "flow_rate": "流量计算",
        "internal_power": "内功率计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算风机性能
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "fan_performance":
            return self._calculate_fan_performance(params)
        elif scenario == "air_density":
            return self._calculate_air_density(params)
        elif scenario == "pressure":
            return self._calculate_pressure(params)
        elif scenario == "flow_rate":
            return self._calculate_flow_rate(params)
        elif scenario == "internal_power":
            return self._calculate_internal_power(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_air_density(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算空气密度"""
        P_inlet = params.get("P_inlet")  # 进口大气压 (pa)
        T = params.get("T")  # 介质温度 (°C)
        
        if P_inlet is None:
            raise ValueError("进口大气压P_inlet必须提供")
        if T is None:
            raise ValueError("介质温度T必须提供")
        
        # 空气密度: ρ = 1.2 × P_inlet / 101325 × 293 / (273 + T)
        rho = 1.2 * P_inlet / 101325 * 293 / (273 + T)
        
        formula = f"空气密度: ρ = 1.2 × P<sub>inlet</sub> / 101325 × 293 / (273 + T)<br>"
        formula += f"  = 1.2 × {P_inlet} / 101325 × 293 / (273 + {T})<br>"
        formula += f"  = {rho:.10f} kg/m³"
        
        return CurrentCalcResponse(
            result=round(rho, 10),
            unit="kg/m³",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["air_density"]
        )
    
    def _calculate_pressure(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算压力"""
        rho = params.get("rho")  # 空气密度 (kg/m³)
        D = params.get("D")  # 叶轮直径 (m)
        n = params.get("n")  # 主轴转速 (rpm)
        psi_p = params.get("psi_p")  # 压力系数
        
        if rho is None:
            raise ValueError("空气密度rho必须提供")
        if D is None or D <= 0:
            raise ValueError("叶轮直径D必须大于0")
        if n is None or n <= 0:
            raise ValueError("主轴转速n必须大于0")
        if psi_p is None:
            raise ValueError("压力系数psi_p必须提供")
        
        # 压力: P = 101300 × ((ρ × (π×D×n/60)² × ψ_p / 354550 + 1)^3.5 - 1)
        u = math.pi * D * n / 60  # 叶轮圆周速度 (m/s)
        P = 101300 * ((rho * (u ** 2) * psi_p / 354550 + 1) ** 3.5 - 1)
        
        formula = f"压力: P = 101300 × ((ρ × (π×D×n/60)² × ψ<sub>p</sub> / 354550 + 1)^3.5 - 1)<br>"
        formula += f"  圆周速度: u = π×D×n/60 = π×{D}×{n}/60 = {u:.6f} m/s<br>"
        formula += f"  P = 101300 × (({rho:.6f} × {u:.6f}² × {psi_p} / 354550 + 1)^3.5 - 1)<br>"
        formula += f"  = {P:.2f} Pa"
        
        return CurrentCalcResponse(
            result=round(P, 2),
            unit="Pa",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["pressure"]
        )
    
    def _calculate_flow_rate(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算流量"""
        D = params.get("D")  # 叶轮直径 (m)
        n = params.get("n")  # 主轴转速 (rpm)
        phi = params.get("phi")  # 流量系数
        
        if D is None or D <= 0:
            raise ValueError("叶轮直径D必须大于0")
        if n is None or n <= 0:
            raise ValueError("主轴转速n必须大于0")
        if phi is None:
            raise ValueError("流量系数phi必须提供")
        
        # 流量: Q = 900 × π × D² × (π×D×n/60) × φ
        u = math.pi * D * n / 60  # 叶轮圆周速度 (m/s)
        Q = 900 * math.pi * (D ** 2) * u * phi
        
        formula = f"流量: Q = 900 × π × D² × (π×D×n/60) × φ<br>"
        formula += f"  圆周速度: u = π×D×n/60 = π×{D}×{n}/60 = {u:.6f} m/s<br>"
        formula += f"  Q = 900 × π × {D}² × {u:.6f} × {phi}<br>"
        formula += f"  = {Q:.2f} m³/h"
        
        return CurrentCalcResponse(
            result=round(Q, 2),
            unit="m³/h",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["flow_rate"]
        )
    
    def _calculate_internal_power(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算内功率"""
        P = params.get("P")  # 压力 (Pa)
        Q = params.get("Q")  # 流量 (m³/h)
        eta = params.get("eta")  # 效率
        
        if P is None:
            raise ValueError("压力P必须提供")
        if Q is None:
            raise ValueError("流量Q必须提供")
        if eta is None or eta <= 0 or eta > 1:
            raise ValueError("效率eta应在0-1之间")
        
        # 内功率: P_internal = P × Q / 3600 / η / 1000
        P_internal = P * Q / 3600 / eta / 1000
        
        formula = f"内功率: P<sub>internal</sub> = P × Q / 3600 / η / 1000<br>"
        formula += f"  = {P:.2f} × {Q:.2f} / 3600 / {eta} / 1000<br>"
        formula += f"  = {P_internal:.2f} kW"
        
        return CurrentCalcResponse(
            result=round(P_internal, 2),
            unit="kW",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["internal_power"]
        )
    
    def _calculate_fan_performance(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """计算完整的风机性能表"""
        D = params.get("D")  # 叶轮直径 (m)
        n = params.get("n")  # 主轴转速 (rpm)
        T = params.get("T")  # 介质温度 (°C)
        P_inlet = params.get("P_inlet")  # 进口大气压 (pa)
        performance_points = params.get("performance_points")  # 性能点列表
        
        if D is None or D <= 0:
            raise ValueError("叶轮直径D必须大于0")
        if n is None or n <= 0:
            raise ValueError("主轴转速n必须大于0")
        if T is None:
            raise ValueError("介质温度T必须提供")
        if P_inlet is None:
            raise ValueError("进口大气压P_inlet必须提供")
        if not performance_points or not isinstance(performance_points, list):
            raise ValueError("性能点列表performance_points必须提供且为列表")
        
        # 1. 计算空气密度
        rho = 1.2 * P_inlet / 101325 * 293 / (273 + T)
        
        # 2. 计算每个性能点的压力、流量和内功率
        results = []
        u = math.pi * D * n / 60  # 叶轮圆周速度 (m/s)
        
        for point in performance_points:
            psi_p = point.get("psi_p")  # 压力系数
            phi = point.get("phi")  # 流量系数
            eta = point.get("eta")  # 效率
            
            if psi_p is None or phi is None or eta is None:
                continue
            
            # 计算压力
            P = 101300 * ((rho * (u ** 2) * psi_p / 354550 + 1) ** 3.5 - 1)
            
            # 计算流量
            Q = 900 * math.pi * (D ** 2) * u * phi
            
            # 计算内功率
            P_internal = P * Q / 3600 / eta / 1000
            
            results.append({
                "psi_p": psi_p,
                "phi": phi,
                "eta": eta,
                "pressure": round(P, 2),
                "flow_rate": round(Q, 2),
                "internal_power": round(P_internal, 2)
            })
        
        formula = f"风机性能计算完成<br>"
        formula += f"叶轮直径: D = {D} m<br>"
        formula += f"主轴转速: n = {n} rpm<br>"
        formula += f"介质温度: T = {T} °C<br>"
        formula += f"进口大气压: P<sub>inlet</sub> = {P_inlet} Pa<br>"
        formula += f"空气密度: ρ = {rho:.6f} kg/m³<br>"
        formula += f"圆周速度: u = {u:.6f} m/s<br>"
        formula += f"<br>共计算 {len(results)} 个性能点"
        
        return CurrentCalcResponse(
            result=results,
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["fan_performance"],
            extra={
                "rho": rho,
                "u": u,
                "D": D,
                "n": n,
                "T": T,
                "P_inlet": P_inlet
            }
        )

