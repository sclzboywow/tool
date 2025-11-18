"""
履带机器人驱动力计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class CrawlerRobotForceCalculator:
    """履带机器人驱动力计算器"""
    
    SCENARIO_NAMES = {
        "crawler_robot_force": "履带机器人驱动力计算",
        "power_calc": "功率计算",
        "torque_calc": "扭矩计算",
        "acceleration_torque_calc": "加速扭矩计算",
        "obstacle_calc": "越障计算",
        "rotation_calc": "原地回转计算",
        "reducer_check": "减速器校验",
        "speed_calc": "速度计算"
    }
    
    # 常数
    G = 10  # 重力加速度 m/s² (Excel中使用10)
    # 使用math.pi确保精度一致性
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算履带机器人驱动力
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "crawler_robot_force":
            return self._calculate_crawler_robot_force(params)
        elif scenario == "power_calc":
            return self._calculate_power(params)
        elif scenario == "torque_calc":
            return self._calculate_torque(params)
        elif scenario == "acceleration_torque_calc":
            return self._calculate_acceleration_torque(params)
        elif scenario == "obstacle_calc":
            return self._calculate_obstacle(params)
        elif scenario == "rotation_calc":
            return self._calculate_rotation(params)
        elif scenario == "reducer_check":
            return self._calculate_reducer_check(params)
        elif scenario == "speed_calc":
            return self._calculate_speed(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _get_common_params(self, params: Dict[str, Any]) -> Dict[str, float]:
        """获取通用参数并计算中间值"""
        # 道路参数
        f = params.get("f", 0.11)  # 滚动摩擦系数
        u = params.get("u", 1.1)  # 滑动摩擦系数
        peak_attachment = params.get("peak_attachment", 1.1)  # 地面峰值附着系数
        slope_percent = params.get("slope_percent", 55)  # 轨道坡度 (%)
        obstacle_height = params.get("obstacle_height")  # 障碍高度 (mm)，None表示未提供
        
        # 车体参数
        m1 = params.get("m1", 50)  # 车体重量 (kg)
        m2 = params.get("m2", 50)  # 负载重量 (kg)
        D = params.get("D", 120)  # 履带轮子直径 (mm)
        D_drive = params.get("D_drive", 120)  # 履带驱动轮直径 (mm)
        B = params.get("B", 446)  # 履带间距（左右）(mm)
        L = params.get("L", 592)  # 接地长度（前后）(mm)
        
        # 运行参数
        v_rated = params.get("v_rated", 0.4)  # 平地车体额定速度 (m/s)
        v_max = params.get("v_max", 0.5)  # 平地车体最大速度 (m/s)
        a = params.get("a", 0.3)  # 运行加速度 (m/s²)
        a_slope = params.get("a_slope")  # 坡道加速度 (m/s²)，默认等于a
        
        # 电机参数
        n_motor = params.get("n_motor", 2)  # 电机数量
        n_effective = params.get("n_effective", 2)  # 有效电机数
        P_motor = params.get("P_motor", 250)  # 电机功率 (W)
        I_no_load = params.get("I_no_load", 1)  # 空转电流 (A)
        I_actual = params.get("I_actual", 9)  # 实际电流(平均) (A)
        T_rated = params.get("T_rated", 0.52)  # 额定扭矩 (Nm)
        I_rated = params.get("I_rated", 9.1)  # 额定电流 (A)
        T_max = params.get("T_max", 1.5)  # 最大扭矩 (Nm)
        n_rated = params.get("n_rated", 4700)  # 额定转速 (rpm)
        n_max = params.get("n_max", 5500)  # 最高转速 (rpm)
        current_unevenness = params.get("current_unevenness", 1.1)  # 电流最大不均匀度
        
        # 减速器参数
        i_total = params.get("i_total")  # 总减速比
        i_custom = params.get("i_custom")  # 自制减速比
        i_reducer = params.get("i_reducer", 64)  # 减速器减速比
        gear_large = params.get("gear_large", 25)  # 大齿轮
        gear_small = params.get("gear_small", 25)  # 小齿轮
        T_gear_large = params.get("T_gear_large")  # 大齿轮许用扭矩 (Nm)
        T_gear_small = params.get("T_gear_small")  # 小齿轮许用扭矩 (Nm)
        n_reducer_rated = params.get("n_reducer_rated", 3500)  # 减速器额定转速 (rpm)
        n_reducer_max = params.get("n_reducer_max", 6000)  # 减速器最高转速 (rpm)
        T_reducer_rated = params.get("T_reducer_rated", 35)  # 减速器额定扭矩 (Nm)
        
        # 计算中间值
        if a_slope is None:
            a_slope = a
        
        # 轨道坡度角度（弧度）
        slope_rad = math.atan(slope_percent / 100)  # B7 = ATAN(B6/100)
        slope_deg = slope_rad * 180 / math.pi  # B8 = B7*180/π
        
        # 自制减速比
        if i_custom is None:
            if gear_large and gear_small:
                i_custom = gear_large / gear_small  # E27 = E28/E29
        
        # 总减速比
        if i_total is None:
            if i_custom and i_reducer:
                i_total = i_custom * i_reducer  # E26 = E27*E32
        
        # 实际扭矩
        T_actual = (I_actual - I_no_load) / I_rated * T_rated  # E9 = (E11-E10)/E13*E12
        
        # 总质量
        m_total = m1 + m2
        
        return {
            'f': f, 'u': u, 'peak_attachment': peak_attachment, 'slope_percent': slope_percent,
            'obstacle_height': obstacle_height, 'm1': m1, 'm2': m2, 'm_total': m_total,
            'D': D, 'D_drive': D_drive, 'B': B, 'L': L,
            'v_rated': v_rated, 'v_max': v_max, 'a': a, 'a_slope': a_slope,
            'n_motor': n_motor, 'n_effective': n_effective, 'P_motor': P_motor,
            'I_no_load': I_no_load, 'I_actual': I_actual, 'T_rated': T_rated,
            'I_rated': I_rated, 'T_max': T_max, 'n_rated': n_rated, 'n_max': n_max,
            'current_unevenness': current_unevenness,
            'i_total': i_total, 'i_custom': i_custom, 'i_reducer': i_reducer,
            'gear_large': gear_large, 'gear_small': gear_small,
            'T_gear_large': T_gear_large, 'T_gear_small': T_gear_small,
            'n_reducer_rated': n_reducer_rated, 'n_reducer_max': n_reducer_max,
            'T_reducer_rated': T_reducer_rated,
            'slope_rad': slope_rad, 'slope_deg': slope_deg, 'T_actual': T_actual
        }
    
    def _calculate_power(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """功率计算"""
        p = self._get_common_params(params)
        
        # 整车平地行走所需功率: P1 = f×(m1+m2)×10×v
        # Excel公式：H3 = B3*(B19+B20)*10*B25
        P1 = p['f'] * p['m_total'] * self.G * p['v_rated']
        
        # 整车坡度行走所需功率: P2 = f×(m1+m2)×cos(θ)×10×v + (m1+m2)×sin(θ)×10×v
        # Excel公式：H4 = B3*(B19+B20)*COS(B7)*10*B25+(B19+B20)*SIN(B7)*10*B25
        P2 = p['f'] * p['m_total'] * math.cos(p['slope_rad']) * self.G * p['v_rated'] + \
             p['m_total'] * math.sin(p['slope_rad']) * self.G * p['v_rated']
        
        # 整车电机提供有效功率: P3 = n×P_motor
        # Excel公式：H5 = E5*E7
        P3 = p['n_effective'] * p['P_motor']
        
        # 行走功率安全系数: K1 = P3/P2
        # Excel公式：H6 = H5/H4
        K1 = P3 / P2 if P2 > 0 else 0
        
        formula = f"整车平地行走所需功率: P<sub>1</sub> = f×(m<sub>1</sub>+m<sub>2</sub>)×10×v<br>"
        formula += f"  = {p['f']}×{p['m_total']}×10×{p['v_rated']}<br>"
        formula += f"  = {P1:.2f} W<br>"
        formula += f"整车坡度行走所需功率: P<sub>2</sub> = f×(m<sub>1</sub>+m<sub>2</sub>)×cos(θ)×10×v + (m<sub>1</sub>+m<sub>2</sub>)×sin(θ)×10×v<br>"
        formula += f"  = {p['f']}×{p['m_total']}×cos({p['slope_deg']:.2f}°)×10×{p['v_rated']} + {p['m_total']}×sin({p['slope_deg']:.2f}°)×10×{p['v_rated']}<br>"
        formula += f"  = {P2:.2f} W<br>"
        formula += f"整车电机提供有效功率: P<sub>3</sub> = n×P<sub>motor</sub><br>"
        formula += f"  = {p['n_effective']}×{p['P_motor']}<br>"
        formula += f"  = {P3:.2f} W<br>"
        formula += f"行走功率安全系数: K<sub>1</sub> = P<sub>3</sub>/P<sub>2</sub><br>"
        formula += f"  = {P3:.2f}/{P2:.2f}<br>"
        formula += f"  = {K1:.2f}"
        
        return CurrentCalcResponse(
            result=round(K1, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["power_calc"],
            extra={'P1': P1, 'P2': P2, 'P3': P3}
        )
    
    def _calculate_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """扭矩计算"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        # 整车平地所需行走扭矩: T1 = f×(m1+m2)×10×D/2000
        # Excel公式：H7 = B3*(B19+B20)*10*B14/2000
        T1 = p['f'] * p['m_total'] * self.G * p['D'] / 2000
        
        # 整车坡道所需行走扭矩: T2 = f×(m1+m2)×cos(θ)×10×D/2000 + (m1+m2)×sin(θ)×10×D/2000
        # Excel公式：H8 = B3*(B19+B20)*COS(B7)*10*B14/2000+(B19+B20)*SIN(B7)*10*B14/2000
        T2 = p['f'] * p['m_total'] * math.cos(p['slope_rad']) * self.G * p['D'] / 2000 + \
             p['m_total'] * math.sin(p['slope_rad']) * self.G * p['D'] / 2000
        
        # 整车电机额定输出扭矩: T3 = T_actual×i×n
        # Excel公式：H9 = E9*E26*E5
        T3 = p['T_actual'] * p['i_total'] * p['n_effective']
        
        # 行走额定扭矩安全系数: K2 = T3/T2
        # Excel公式：H10 = H9/H8
        K2 = T3 / T2 if T2 > 0 else 0
        
        formula = f"整车平地所需行走扭矩: T<sub>1</sub> = f×(m<sub>1</sub>+m<sub>2</sub>)×10×D/2000<br>"
        formula += f"  = {p['f']}×{p['m_total']}×10×{p['D']}/2000<br>"
        formula += f"  = {T1:.4f} Nm<br>"
        formula += f"整车坡道所需行走扭矩: T<sub>2</sub> = f×(m<sub>1</sub>+m<sub>2</sub>)×cos(θ)×10×D/2000 + (m<sub>1</sub>+m<sub>2</sub>)×sin(θ)×10×D/2000<br>"
        formula += f"  = {T2:.4f} Nm<br>"
        formula += f"整车电机额定输出扭矩: T<sub>3</sub> = T<sub>actual</sub>×i×n<br>"
        formula += f"  = {p['T_actual']:.4f}×{p['i_total']}×{p['n_effective']}<br>"
        formula += f"  = {T3:.4f} Nm<br>"
        formula += f"行走额定扭矩安全系数: K<sub>2</sub> = T<sub>3</sub>/T<sub>2</sub><br>"
        formula += f"  = {T3:.4f}/{T2:.4f}<br>"
        formula += f"  = {K2:.2f}"
        
        return CurrentCalcResponse(
            result=round(K2, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["torque_calc"],
            extra={'T1': T1, 'T2': T2, 'T3': T3}
        )
    
    def _calculate_acceleration_torque(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """加速扭矩计算"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        # 整车平地所需加速扭矩: T4 = T1 + (m1+m2)×a×D/2000
        # Excel公式：H11 = B3*(B19+B20)*10*B14/2000+(B19+B20)*B28*B14/2000
        T1 = p['f'] * p['m_total'] * self.G * p['D'] / 2000
        T4 = T1 + p['m_total'] * p['a'] * p['D'] / 2000
        
        # 整车坡道所需加速扭矩: T5 = T2 + (m1+m2)×a_slope×D/2000
        # Excel公式：H12 = B3*(B19+B20)*COS(B7)*10*B14/2000+(B19+B20)*SIN(B7)*10*B14/2000+(B19+B20)*B29*B14/2000
        T2 = p['f'] * p['m_total'] * math.cos(p['slope_rad']) * self.G * p['D'] / 2000 + \
             p['m_total'] * math.sin(p['slope_rad']) * self.G * p['D'] / 2000
        T5 = T2 + p['m_total'] * p['a_slope'] * p['D'] / 2000
        
        # 整车电机最大输出扭矩: T6 = T_max×i×n×0.5
        # Excel公式：H13 = E14*E26*E5*0.5
        T6 = p['T_max'] * p['i_total'] * p['n_effective'] * 0.5
        
        # 加速最大扭矩安全系数: K3 = T6/T5
        # Excel公式：H14 = H13/H12
        K3 = T6 / T5 if T5 > 0 else 0
        
        formula = f"整车平地所需加速扭矩: T<sub>4</sub> = T<sub>1</sub> + (m<sub>1</sub>+m<sub>2</sub>)×a×D/2000<br>"
        formula += f"  = {T1:.4f} + {p['m_total']}×{p['a']}×{p['D']}/2000<br>"
        formula += f"  = {T4:.4f} Nm<br>"
        formula += f"整车坡道所需加速扭矩: T<sub>5</sub> = T<sub>2</sub> + (m<sub>1</sub>+m<sub>2</sub>)×a<sub>slope</sub>×D/2000<br>"
        formula += f"  = {T2:.4f} + {p['m_total']}×{p['a_slope']}×{p['D']}/2000<br>"
        formula += f"  = {T5:.4f} Nm<br>"
        formula += f"整车电机最大输出扭矩: T<sub>6</sub> = T<sub>max</sub>×i×n×0.5<br>"
        formula += f"  = {p['T_max']}×{p['i_total']}×{p['n_effective']}×0.5<br>"
        formula += f"  = {T6:.4f} Nm<br>"
        formula += f"加速最大扭矩安全系数: K<sub>3</sub> = T<sub>6</sub>/T<sub>5</sub><br>"
        formula += f"  = {T6:.4f}/{T5:.4f}<br>"
        formula += f"  = {K3:.2f}"
        
        return CurrentCalcResponse(
            result=round(K3, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["acceleration_torque_calc"],
            extra={'T4': T4, 'T5': T5, 'T6': T6}
        )
    
    def _calculate_obstacle(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """越障计算"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        # 先计算T5（坡道所需加速扭矩）
        T2 = p['f'] * p['m_total'] * math.cos(p['slope_rad']) * self.G * p['D'] / 2000 + \
             p['m_total'] * math.sin(p['slope_rad']) * self.G * p['D'] / 2000
        T5 = T2 + p['m_total'] * p['a_slope'] * p['D'] / 2000
        
        # 越障附加扭矩（改进的动力学模型）
        # 基于履带车辆越障理论，考虑障碍物高度和轮径的几何关系
        # T7 = m×g×h_obstacle/(D/2) = 2×m×g×h_obstacle/D
        # 单位转换：h_obstacle和D都是mm，转换为m后计算扭矩
        # T7 = 2×m×g×h_obstacle/(D×1000) = m×g×h_obstacle/(D×500)
        # 如果未提供障碍物高度，使用简化经验公式：T7 = m×D/4000
        if p.get('obstacle_height') is not None and p['obstacle_height'] > 0:
            # 使用精确的越障动力学模型
            T7 = p['m_total'] * self.G * p['obstacle_height'] / (p['D'] * 500)
            formula_T7 = f"越障附加扭矩: T<sub>7</sub> = (m<sub>1</sub>+m<sub>2</sub>)×g×h<sub>obstacle</sub>/(D×500)<br>"
            formula_T7 += f"  = {p['m_total']}×10×{p['obstacle_height']}/({p['D']}×500)<br>"
        else:
            # 使用简化经验公式（向后兼容）
            T7 = p['m_total'] * p['D'] / 4000
            formula_T7 = f"越障附加扭矩: T<sub>7</sub> = (m<sub>1</sub>+m<sub>2</sub>)×D/4000 (经验公式)<br>"
            formula_T7 += f"  = {p['m_total']}×{p['D']}/4000<br>"
        
        # 越障整车所需扭矩: T8 = T7 + T5
        # Excel公式：H16 = H15+H12
        T8 = T7 + T5
        
        # 越障整车电机最大扭矩: T9 = T_max×i×n×0.8
        # Excel公式：H17 = E14*E26*E5*0.8
        T9 = p['T_max'] * p['i_total'] * p['n_effective'] * 0.8
        
        # 整车路面提供的最大扭矩: T_road = peak_attachment×(m1+m2)×10×D/2000
        # Excel公式：H18 = B5*(B19+B20)*10*B14/2000
        T_road = p['peak_attachment'] * p['m_total'] * self.G * p['D'] / 2000
        
        # 越障最大扭矩安全系数: K4 = T9/T8
        # Excel公式：H19 = H17/H16
        K4 = T9 / T8 if T8 > 0 else 0
        
        # 路面提供扭矩安全系数: K_road = T_road/T8
        # Excel公式：H20 = H18/H16
        K_road = T_road / T8 if T8 > 0 else 0
        
        formula = formula_T7
        formula += f"  = {T7:.4f} Nm<br>"
        formula += f"越障整车所需扭矩: T<sub>8</sub> = T<sub>7</sub> + T<sub>5</sub><br>"
        formula += f"  = {T7:.4f} + {T5:.4f}<br>"
        formula += f"  = {T8:.4f} Nm<br>"
        formula += f"越障整车电机最大扭矩: T<sub>9</sub> = T<sub>max</sub>×i×n×0.8<br>"
        formula += f"  = {p['T_max']}×{p['i_total']}×{p['n_effective']}×0.8<br>"
        formula += f"  = {T9:.4f} Nm<br>"
        formula += f"整车路面提供的最大扭矩: T<sub>road</sub> = peak_attachment×(m<sub>1</sub>+m<sub>2</sub>)×10×D/2000<br>"
        formula += f"  = {p['peak_attachment']}×{p['m_total']}×10×{p['D']}/2000<br>"
        formula += f"  = {T_road:.4f} Nm<br>"
        formula += f"越障最大扭矩安全系数: K<sub>4</sub> = T<sub>9</sub>/T<sub>8</sub><br>"
        formula += f"  = {T9:.4f}/{T8:.4f}<br>"
        formula += f"  = {K4:.2f}<br>"
        formula += f"路面提供扭矩安全系数: K<sub>road</sub> = T<sub>road</sub>/T<sub>8</sub><br>"
        formula += f"  = {T_road:.4f}/{T8:.4f}<br>"
        formula += f"  = {K_road:.2f}"
        
        return CurrentCalcResponse(
            result=round(K4, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["obstacle_calc"],
            extra={'T7': T7, 'T8': T8, 'T9': T9, 'T_road': T_road, 'K_road': K_road}
        )
    
    def _calculate_rotation(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """原地回转计算"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        # 单履带阻力: F1 = (m1+m2)×10×f/2 + u×(m1+m2)×10×L/(4×B)
        # Excel公式：H21 = (B19+B20)*10*B3/2+B4*(B19+B20)*10*B18/4/B17
        F1 = p['m_total'] * self.G * p['f'] / 2 + \
             p['u'] * p['m_total'] * self.G * p['L'] / (4 * p['B'])
        
        # 单电机额定提供驱动力: F2 = T_actual×i/D_drive×2000
        # Excel公式：H22 = E9*E26/B15*2000
        F2 = p['T_actual'] * p['i_total'] / p['D_drive'] * 2000
        
        # 原地回转扭矩安全系数: K5 = F2/F1
        # Excel公式：H23 = H22/H21
        K5 = F2 / F1 if F1 > 0 else 0
        
        formula = f"单履带阻力: F<sub>1</sub> = (m<sub>1</sub>+m<sub>2</sub>)×10×f/2 + u×(m<sub>1</sub>+m<sub>2</sub>)×10×L/(4×B)<br>"
        formula += f"  = {p['m_total']}×10×{p['f']}/2 + {p['u']}×{p['m_total']}×10×{p['L']}/(4×{p['B']})<br>"
        formula += f"  = {F1:.2f} N<br>"
        formula += f"单电机额定提供驱动力: F<sub>2</sub> = T<sub>actual</sub>×i/D<sub>drive</sub>×2000<br>"
        formula += f"  = {p['T_actual']:.4f}×{p['i_total']}/{p['D_drive']}×2000<br>"
        formula += f"  = {F2:.2f} N<br>"
        formula += f"原地回转扭矩安全系数: K<sub>5</sub> = F<sub>2</sub>/F<sub>1</sub><br>"
        formula += f"  = {F2:.2f}/{F1:.2f}<br>"
        formula += f"  = {K5:.2f}"
        
        return CurrentCalcResponse(
            result=round(K5, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["rotation_calc"],
            extra={'F1': F1, 'F2': F2}
        )
    
    def _calculate_reducer_check(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """减速器校验"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        if p['i_custom'] is None:
            raise ValueError("需要提供自制减速比i_custom或大齿轮gear_large和小齿轮gear_small")
        
        # 额定时，大齿轮输出扭矩: T_gear_large_out = T_actual×i_reducer×i_custom
        # Excel公式：H30 = E9*E32*E27
        T_gear_large_out = p['T_actual'] * p['i_reducer'] * p['i_custom']
        
        # 额定时，小齿轮输出扭矩: T_gear_small_out = T_actual×i_reducer
        # Excel公式：H31 = E9*E32
        T_gear_small_out = p['T_actual'] * p['i_reducer']
        
        # 额定时，减速器输出扭矩: T_reducer_out = T_actual×i_reducer
        # Excel公式：H35 = E9*E32
        T_reducer_out = p['T_actual'] * p['i_reducer']
        
        # 安全系数
        K_gear_large = p['T_gear_large'] / T_gear_large_out if T_gear_large_out > 0 and p['T_gear_large'] else 0
        K_gear_small = p['T_gear_small'] / T_gear_small_out if T_gear_small_out > 0 and p['T_gear_small'] else 0
        K_reducer = p['T_reducer_rated'] / T_reducer_out if T_reducer_out > 0 else 0
        
        formula = f"额定时，大齿轮输出扭矩: T<sub>gear_large_out</sub> = T<sub>actual</sub>×i<sub>reducer</sub>×i<sub>custom</sub><br>"
        formula += f"  = {p['T_actual']:.4f}×{p['i_reducer']}×{p['i_custom']}<br>"
        formula += f"  = {T_gear_large_out:.4f} Nm<br>"
        formula += f"额定时，小齿轮输出扭矩: T<sub>gear_small_out</sub> = T<sub>actual</sub>×i<sub>reducer</sub><br>"
        formula += f"  = {p['T_actual']:.4f}×{p['i_reducer']}<br>"
        formula += f"  = {T_gear_small_out:.4f} Nm<br>"
        formula += f"额定时，减速器输出扭矩: T<sub>reducer_out</sub> = T<sub>actual</sub>×i<sub>reducer</sub><br>"
        formula += f"  = {p['T_actual']:.4f}×{p['i_reducer']}<br>"
        formula += f"  = {T_reducer_out:.4f} Nm<br>"
        if p['T_gear_large']:
            formula += f"大齿轮安全系数: K<sub>gear_large</sub> = T<sub>gear_large</sub>/T<sub>gear_large_out</sub><br>"
            formula += f"  = {p['T_gear_large']}/{T_gear_large_out:.4f}<br>"
            formula += f"  = {K_gear_large:.2f}<br>"
        if p['T_gear_small']:
            formula += f"小齿轮安全系数: K<sub>gear_small</sub> = T<sub>gear_small</sub>/T<sub>gear_small_out</sub><br>"
            formula += f"  = {p['T_gear_small']}/{T_gear_small_out:.4f}<br>"
            formula += f"  = {K_gear_small:.2f}<br>"
        formula += f"减速器安全系数: K<sub>reducer</sub> = T<sub>reducer_rated</sub>/T<sub>reducer_out</sub><br>"
        formula += f"  = {p['T_reducer_rated']}/{T_reducer_out:.4f}<br>"
        formula += f"  = {K_reducer:.2f}"
        
        return CurrentCalcResponse(
            result=round(K_reducer, 2),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["reducer_check"],
            extra={
                'T_gear_large_out': T_gear_large_out,
                'T_gear_small_out': T_gear_small_out,
                'T_reducer_out': T_reducer_out,
                'K_gear_large': K_gear_large,
                'K_gear_small': K_gear_small
            }
        )
    
    def _calculate_speed(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """速度计算"""
        p = self._get_common_params(params)
        
        if p['i_total'] is None:
            raise ValueError("需要提供总减速比i_total或自制减速比i_custom和减速器减速比i_reducer")
        
        # 平地（坡道）额定速度: v_rated_calc = n_rated/60/i_total×π×D/1000
        # Excel公式：H25 = E17/60/E26*3.14*B14/1000 (使用math.pi提高精度)
        v_rated_calc = p['n_rated'] / 60 / p['i_total'] * math.pi * p['D'] / 1000
        
        # 平地（坡道）最大速度: v_max_calc = n_max/60/i_total×π×D/1000
        # Excel公式：H26 = E18/60/E26*3.14*B14/1000 (使用math.pi提高精度)
        v_max_calc = p['n_max'] / 60 / p['i_total'] * math.pi * p['D'] / 1000
        
        formula = f"平地（坡道）额定速度: v<sub>rated_calc</sub> = n<sub>rated</sub>/60/i<sub>total</sub>×π×D/1000<br>"
        formula += f"  = {p['n_rated']}/60/{p['i_total']}×π×{p['D']}/1000<br>"
        formula += f"  = {v_rated_calc:.4f} m/s<br>"
        formula += f"平地（坡道）最大速度: v<sub>max_calc</sub> = n<sub>max</sub>/60/i<sub>total</sub>×π×D/1000<br>"
        formula += f"  = {p['n_max']}/60/{p['i_total']}×π×{p['D']}/1000<br>"
        formula += f"  = {v_max_calc:.4f} m/s"
        
        return CurrentCalcResponse(
            result=round(v_rated_calc, 4),
            unit="m/s",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["speed_calc"],
            extra={'v_max_calc': v_max_calc}
        )
    
    def _calculate_crawler_robot_force(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """履带机器人驱动力计算（完整计算）"""
        # 调用功率计算作为主要结果
        return self._calculate_power(params)