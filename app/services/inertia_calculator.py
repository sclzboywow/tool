"""
惯量计算服务
实现不同形状物体惯量计算
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class InertiaCalculator:
    """惯量计算器"""
    
    SCENARIO_NAMES = {
        "cylinder_parallel": "圆柱体惯量计算（平行）",
        "cylinder_perpendicular": "圆柱体惯量计算（垂直）",
        "rectangular": "方形物体惯量计算",
        "disk": "饼状物体惯量计算",
        "linear_motion": "直线运动物体惯量计算",
        "direct_inertia": "直接惯量计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算惯量
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "cylinder_parallel":
            return self._calculate_cylinder_parallel(params)
        elif scenario == "cylinder_perpendicular":
            return self._calculate_cylinder_perpendicular(params)
        elif scenario == "rectangular":
            return self._calculate_rectangular(params)
        elif scenario == "disk":
            return self._calculate_disk(params)
        elif scenario == "linear_motion":
            return self._calculate_linear_motion(params)
        elif scenario == "direct_inertia":
            return self._calculate_direct_inertia(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_cylinder_parallel(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """圆柱体惯量计算（平行）：圆柱体长度方向中心线和旋转中心线平行"""
        d0 = params.get("d0")  # 外径 (mm)
        d1 = params.get("d1", 0)  # 内径 (mm)，默认为0（实心）
        L = params.get("L")  # 长度 (mm)
        rho = params.get("rho")  # 密度 (kg/m³)
        e = params.get("e", 0)  # 重心线与旋转轴线距离 (mm)
        
        if d0 is None or L is None or rho is None:
            raise ValueError("圆柱体惯量计算（平行）需要外径、长度和密度")
        
        # 转换为米
        d0_m = d0 / 1000
        d1_m = d1 / 1000
        L_m = L / 1000
        e_m = e / 1000
        
        # 计算质量: m = π × ((d0/2)² - (d1/2)²) × L × ρ
        m = math.pi * ((d0_m/2)**2 - (d1_m/2)**2) * L_m * rho
        
        # 计算惯量: J = (π/32) × ρ × L × (d0⁴ - d1⁴) + m × e²
        J0 = (math.pi / 32) * rho * L_m * (d0_m**4 - d1_m**4)
        J = J0 + m * e_m**2
        
        # 转换为 kg·cm²
        J_cm2 = J * 10000
        
        formula = f"J = (π/32) × ρ × L × (d0⁴ - d1⁴) + m × e²\n"
        formula += f"  = (π/32) × {rho} × {L_m:.4f} × ({d0_m:.4f}⁴ - {d1_m:.4f}⁴) + {m:.4f} × {e_m:.4f}²\n"
        formula += f"  = {J0:.6f} + {m:.4f} × {e_m:.4f}² = {J:.6f} kg·m² = {J_cm2:.4f} kg·cm²"
        
        return CurrentCalcResponse(
            result=round(J_cm2, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["cylinder_parallel"],
            mass=round(m, 4)  # 额外返回质量
        )
    
    def _calculate_cylinder_perpendicular(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """圆柱体惯量计算（垂直）：圆柱体长度方向中心线和旋转中心线垂直"""
        d0 = params.get("d0")  # 外径 (mm)
        d1 = params.get("d1", 0)  # 内径 (mm)
        L = params.get("L")  # 长度 (mm)
        rho = params.get("rho")  # 密度 (kg/m³)
        e = params.get("e", 0)  # 重心线与旋转轴线距离 (mm)
        
        if d0 is None or L is None or rho is None:
            raise ValueError("圆柱体惯量计算（垂直）需要外径、长度和密度")
        
        # 转换为米
        d0_m = d0 / 1000
        d1_m = d1 / 1000
        L_m = L / 1000
        e_m = e / 1000
        
        # 计算质量: m = π × ((d0/2)² - (d1/2)²) × L × ρ
        m = math.pi * ((d0_m/2)**2 - (d1_m/2)**2) * L_m * rho
        
        # 计算惯量: J = (1/4) × m × ((d0²+d1²)/4 + L²/3) + m × e²
        J0 = (1/4) * m * ((d0_m**2 + d1_m**2)/4 + (L_m**2/3))
        J = J0 + m * e_m**2
        
        # 转换为 kg·cm²
        J_cm2 = J * 10000
        
        formula = f"J = (1/4) × m × ((d0²+d1²)/4 + L²/3) + m × e²\n"
        formula += f"  = (1/4) × {m:.4f} × (({d0_m:.4f}²+{d1_m:.4f}²)/4 + {L_m:.4f}²/3) + {m:.4f} × {e_m:.4f}²\n"
        formula += f"  = {J0:.6f} + {m:.4f} × {e_m:.4f}² = {J:.6f} kg·m² = {J_cm2:.4f} kg·cm²"
        
        return CurrentCalcResponse(
            result=round(J_cm2, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["cylinder_perpendicular"],
            mass=round(m, 4)
        )
    
    def _calculate_rectangular(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """方形物体惯量计算：长方体惯量计算"""
        x = params.get("x")  # 长度 (mm)
        y = params.get("y")  # 宽度 (mm)
        z = params.get("z")  # 高度 (mm)
        rho = params.get("rho")  # 密度 (kg/m³)
        e = params.get("e", 0)  # 重心线与旋转轴线距离 (mm)
        
        if x is None or y is None or z is None or rho is None:
            raise ValueError("方形物体惯量计算需要长度、宽度、高度和密度")
        
        # 转换为米
        x_m = x / 1000
        y_m = y / 1000
        z_m = z / 1000
        e_m = e / 1000
        
        # 计算质量: m = x × y × z × ρ
        m = x_m * y_m * z_m * rho
        
        # 计算惯量: J = (1/12) × m × (x²+y²) + m × e²
        J0 = (1/12) * m * (x_m**2 + y_m**2)
        J = J0 + m * e_m**2
        
        # 转换为 kg·cm²
        J_cm2 = J * 10000
        
        formula = f"J = (1/12) × m × (x²+y²) + m × e²\n"
        formula += f"  = (1/12) × {m:.4f} × ({x_m:.4f}²+{y_m:.4f}²) + {m:.4f} × {e_m:.4f}²\n"
        formula += f"  = {J0:.6f} + {m:.4f} × {e_m:.4f}² = {J:.6f} kg·m² = {J_cm2:.4f} kg·cm²"
        
        return CurrentCalcResponse(
            result=round(J_cm2, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["rectangular"],
            mass=round(m, 4)
        )
    
    def _calculate_disk(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """饼状物体惯量计算：实心圆柱体惯量计算"""
        d = params.get("d")  # 直径 (mm)
        h = params.get("h")  # 厚度 (mm)
        rho = params.get("rho")  # 密度 (kg/m³)
        e = params.get("e", 0)  # 重心线与旋转轴线距离 (mm)
        
        if d is None or h is None or rho is None:
            raise ValueError("饼状物体惯量计算需要直径、厚度和密度")
        
        # 转换为米
        d_m = d / 1000
        h_m = h / 1000
        e_m = e / 1000
        
        # 计算质量: m = π × (d/2)² × h × ρ
        m = math.pi * (d_m/2)**2 * h_m * rho
        
        # 计算惯量: J = (1/8) × m × d² + m × e²
        J0 = (1/8) * m * d_m**2
        J = J0 + m * e_m**2
        
        # 转换为 kg·cm²
        J_cm2 = J * 10000
        
        formula = f"J = (1/8) × m × d² + m × e²\n"
        formula += f"  = (1/8) × {m:.4f} × {d_m:.4f}² + {m:.4f} × {e_m:.4f}²\n"
        formula += f"  = {J0:.6f} + {m:.4f} × {e_m:.4f}² = {J:.6f} kg·m² = {J_cm2:.4f} kg·cm²"
        
        return CurrentCalcResponse(
            result=round(J_cm2, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["disk"],
            mass=round(m, 4)
        )
    
    def _calculate_linear_motion(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """直线运动物体惯量计算：将直线运动转换为旋转惯量"""
        A = params.get("A")  # 电机每转1圈物体直线运动量 (mm)
        m = params.get("m")  # 物体质量 (kg)
        
        if A is None or m is None:
            raise ValueError("直线运动物体惯量计算需要运动量和质量")
        
        # 转换为米
        A_m = A / 1000
        
        # 计算等效半径: r = A/(2π)
        r = A_m / (2 * math.pi)
        
        # 计算惯量: J = m × r² = m × (A/(2π))²
        J = m * r**2
        
        # 转换为 kg·cm²
        J_cm2 = J * 10000
        
        formula = f"J = m × (A/(2π))²\n"
        formula += f"  = {m:.4f} × ({A_m:.4f}/(2π))²\n"
        formula += f"  = {m:.4f} × {r:.6f}² = {J:.6f} kg·m² = {J_cm2:.4f} kg·cm²"
        
        return CurrentCalcResponse(
            result=round(J_cm2, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["linear_motion"]
        )
    
    def _calculate_direct_inertia(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """直接惯量计算：已知惯量J0和质量m，计算平移后的惯量J1（平行轴定理）"""
        J0 = params.get("J0")  # 惯量 (kg·cm²)
        m = params.get("m")  # 质量 (kg)
        e = params.get("e")  # 重心线与旋转轴线距离 (mm)
        
        if J0 is None or m is None or e is None:
            raise ValueError("直接惯量计算需要惯量、质量和距离")
        
        # 转换为标准单位
        J0_m2 = J0 / 10000  # kg·cm² → kg·m²
        e_cm = e / 10  # mm → cm
        e_m = e / 1000  # mm → m
        
        # 计算惯量: J1 = J0 + m × (e/10)² = J0 + m × e²/100
        # 注意：e的单位是mm，需要转换为cm: e(cm) = e(mm)/10
        J1 = J0 + m * e_cm**2
        
        # 转换为 kg·m²（用于公式显示）
        J1_m2 = J1 / 10000
        
        formula = f"J1 = J0 + m × (e/10)² = J0 + m × e²/100\n"
        formula += f"  = {J0:.4f} + {m:.4f} × ({e}/10)²\n"
        formula += f"  = {J0:.4f} + {m:.4f} × {e_cm:.4f}² = {J1:.4f} kg·cm² = {J1_m2:.6f} kg·m²"
        
        return CurrentCalcResponse(
            result=round(J1, 4),
            unit="kg·cm²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["direct_inertia"],
            mass=round(m, 4)
        )

