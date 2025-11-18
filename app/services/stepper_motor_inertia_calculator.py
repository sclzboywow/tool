"""
步进电机惯量计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class StepperMotorInertiaCalculator:
    """步进电机惯量计算器"""
    
    SCENARIO_NAMES = {
        "ball_screw": "滚珠丝杠惯量计算",
        "rack_pinion": "齿条和小齿轮・传送带・链条传动惯量计算",
        "turntable": "旋转体・转盘驱动惯量计算",
        "angular_acceleration": "角加速度计算",
        "motor_torque": "电机力矩计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算步进电机惯量
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "ball_screw":
            return self._calculate_ball_screw(params)
        elif scenario == "rack_pinion":
            return self._calculate_rack_pinion(params)
        elif scenario == "turntable":
            return self._calculate_turntable(params)
        elif scenario == "angular_acceleration":
            return self._calculate_angular_acceleration(params)
        elif scenario == "motor_torque":
            return self._calculate_motor_torque(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_ball_screw(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """滚珠丝杠惯量计算"""
        W = params.get("W")  # 可动部分总重量 (kg)
        BP = params.get("BP")  # 丝杠螺距 (mm)
        GL = params.get("GL")  # 减速比
        
        if W is None or W <= 0:
            raise ValueError("可动部分总重量W必须大于0")
        if BP is None or BP <= 0:
            raise ValueError("丝杠螺距BP必须大于0")
        if GL is None or GL <= 0:
            raise ValueError("减速比GL必须大于0")
        
        # J₁ = W * (BP / (2 * π * 1000))² * GL²
        # Excel公式：I8 = I5*(I6/(2*PI()*1000))^2*I7^2
        J1 = W * (BP / (2 * math.pi * 1000)) ** 2 * GL ** 2
        
        formula = f"滚珠丝杠惯量: J₁ = W × (BP / (2 × π × 1000))² × GL²<br>"
        formula += f"  = {W} × ({BP} / (2 × π × 1000))² × {GL}²<br>"
        formula += f"  = {W} × ({BP / (2 * math.pi * 1000):.10f})² × {GL}²<br>"
        formula += f"  = {J1:.10f} kg·m²"
        
        return CurrentCalcResponse(
            result=round(J1, 10),
            unit="kg·m²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["ball_screw"]
        )
    
    def _calculate_rack_pinion(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """齿条和小齿轮・传送带・链条传动惯量计算"""
        W = params.get("W")  # 可动部分总重量 (kg)
        D = params.get("D")  # 小齿轮/链轮直径 (mm)
        GL = params.get("GL")  # 减速比
        
        if W is None or W <= 0:
            raise ValueError("可动部分总重量W必须大于0")
        if D is None or D <= 0:
            raise ValueError("小齿轮/链轮直径D必须大于0")
        if GL is None or GL <= 0:
            raise ValueError("减速比GL必须大于0")
        
        # J = W * (D / 2000)² * GL²
        # Excel公式：I20 = I17*(I18/2000)^2*I19^2
        J = W * (D / 2000) ** 2 * GL ** 2
        
        formula = f"齿条和小齿轮・传送带・链条传动惯量: J = W × (D / 2000)² × GL²<br>"
        formula += f"  = {W} × ({D} / 2000)² × {GL}²<br>"
        formula += f"  = {W} × ({D / 2000:.6f})² × {GL}²<br>"
        formula += f"  = {J:.6f} kg·m²"
        
        return CurrentCalcResponse(
            result=round(J, 6),
            unit="kg·m²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["rack_pinion"]
        )
    
    def _calculate_turntable(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """旋转体・转盘驱动惯量计算"""
        J1 = params.get("J1")  # 转盘的惯性矩 (kg·m²)
        W = params.get("W")  # 转盘上物体的重量 (kg)
        L = params.get("L")  # 物体与旋转轴的距离 (mm)
        GL = params.get("GL")  # 减速比
        
        if J1 is None or J1 < 0:
            raise ValueError("转盘的惯性矩J1必须大于等于0")
        if W is None or W <= 0:
            raise ValueError("转盘上物体的重量W必须大于0")
        if L is None or L <= 0:
            raise ValueError("物体与旋转轴的距离L必须大于0")
        if GL is None or GL <= 0:
            raise ValueError("减速比GL必须大于0")
        
        # J = (J₁ + W * (L / 1000)²) * GL²
        # Excel公式：I34 = (I30+I31*(I32/1000)^2)*I33^2
        J = (J1 + W * (L / 1000) ** 2) * GL ** 2
        
        formula = f"旋转体・转盘驱动惯量: J = (J₁ + W × (L / 1000)²) × GL²<br>"
        formula += f"  = ({J1} + {W} × ({L} / 1000)²) × {GL}²<br>"
        formula += f"  = ({J1} + {W} × {L / 1000:.6f}²) × {GL}²<br>"
        formula += f"  = ({J1} + {W * (L / 1000) ** 2:.6f}) × {GL}²<br>"
        formula += f"  = {J:.6f} kg·m²"
        
        return CurrentCalcResponse(
            result=round(J, 6),
            unit="kg·m²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["turntable"]
        )
    
    def _calculate_angular_acceleration(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """角加速度计算"""
        n = params.get("n")  # 转速 (n/s, 转/秒)
        delta_t = params.get("delta_t")  # 加速时间 (s)
        
        if n is None or n <= 0:
            raise ValueError("转速n必须大于0")
        if delta_t is None or delta_t <= 0:
            raise ValueError("加速时间Δt必须大于0")
        
        # ε = (n * 2 * π) / Δt
        # Excel公式：I63 = I60*2*PI()/I61
        # 转速单位是 n/s (转/秒)，转换为 rad/s: ω = n * 2π
        epsilon = (n * 2 * math.pi) / delta_t
        
        formula = f"角加速度: ε = (n × 2 × π) / Δt<br>"
        formula += f"  = ({n} × 2 × π) / {delta_t}<br>"
        formula += f"  = {n * 2 * math.pi:.6f} / {delta_t}<br>"
        formula += f"  = {epsilon:.6f} rad/s²"
        
        return CurrentCalcResponse(
            result=round(epsilon, 6),
            unit="rad/s²",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["angular_acceleration"]
        )
    
    def _calculate_motor_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电机力矩计算"""
        J = params.get("J")  # 惯量 (kg·m²)
        epsilon = params.get("epsilon")  # 角加速度 (rad/s²)
        T_L = params.get("T_L", 0)  # 系统外力折算到电机上的力矩 (Nm)，默认为0
        eta = params.get("eta")  # 传动系统的效率
        
        if J is None or J <= 0:
            raise ValueError("惯量J必须大于0")
        if epsilon is None or epsilon <= 0:
            raise ValueError("角加速度ε必须大于0")
        if eta is None or eta <= 0 or eta > 1:
            raise ValueError("传动系统的效率η应在0-1之间")
        
        # T = (J * ε + T_L) / η
        # Excel公式：I71 = (I67*I68+I69)/I70
        T = (J * epsilon + T_L) / eta
        
        formula = f"电机力矩: T = (J × ε + T<sub>L</sub>) / η<br>"
        formula += f"  = ({J} × {epsilon:.6f} + {T_L}) / {eta}<br>"
        formula += f"  = ({J * epsilon:.6f} + {T_L}) / {eta}<br>"
        formula += f"  = {T:.6f} Nm"
        
        return CurrentCalcResponse(
            result=round(T, 6),
            unit="Nm",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["motor_torque"]
        )

