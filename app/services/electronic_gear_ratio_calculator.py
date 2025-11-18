"""
伺服电机电子齿轮比计算器
"""
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class ElectronicGearRatioCalculator:
    """伺服电机电子齿轮比计算器"""
    
    SCENARIO_NAMES = {
        "forward": "正向计算（已知负载移动距离和电机转数）",
        "reverse": "反向计算（已知脉冲当量）"
    }
    
    def calculate(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        计算电子齿轮比
        
        参数:
        - encoder_resolution: 编码器分辨率 (脉冲/转)
        - mechanical_ratio: 机械减速比
        - load_distance: 负载移动距离 (mm)
        - motor_revolutions: 电机转数 (转)
        - pulse_equivalent: 脉冲当量 (mm/脉冲) - 可选，用于反向计算
        
        返回:
        - electronic_gear_ratio: 电子齿轮比
        - pulse_equivalent_calc: 计算得到的脉冲当量 (mm/脉冲)
        """
        # 获取输入参数
        encoder_resolution = params.get("encoder_resolution")  # 编码器分辨率 (脉冲/转)
        mechanical_ratio = params.get("mechanical_ratio")  # 机械减速比
        load_distance = params.get("load_distance")  # 负载移动距离 (mm)
        motor_revolutions = params.get("motor_revolutions")  # 电机转数 (转)
        pulse_equivalent = params.get("pulse_equivalent")  # 脉冲当量 (mm/脉冲) - 可选
        
        # 验证必需参数
        if encoder_resolution is None or encoder_resolution <= 0:
            raise ValueError("编码器分辨率必须大于0")
        if mechanical_ratio is None or mechanical_ratio <= 0:
            raise ValueError("机械减速比必须大于0")
        
        formula_parts = []
        intermediate_results = {}
        
        # 情况2: 已知脉冲当量，反向计算电子齿轮比（优先判断）
        if pulse_equivalent is not None and pulse_equivalent > 0:
            # 根据Excel公式：电子齿轮比 = (编码器分辨率 × 脉冲当量 × 减速比分母 / 减速比分子) / 机械部分每圈位移量
            # 其中：机械部分每圈位移量 = 负载移动距离 / 电机转数（电机转1圈时负载移动的距离）
            # 机械减速比 = 减速比分子 / 减速比分母
            # 所以：减速比分母 / 减速比分子 = 1 / 机械减速比
            # 代入得：电子齿轮比 = (编码器分辨率 × 脉冲当量 / 机械减速比) / (负载移动距离 / 电机转数)
            #                    = (编码器分辨率 × 脉冲当量 × 电机转数) / (负载移动距离 × 机械减速比)
            # 如果提供了负载移动距离和电机转数，使用Excel公式
            if load_distance is not None and load_distance > 0 and motor_revolutions is not None and motor_revolutions > 0:
                # 计算机械部分每圈位移量（电机转1圈时负载移动的距离）
                displacement_per_revolution = load_distance / motor_revolutions
                # Excel公式：电子齿轮比 = (编码器分辨率 × 脉冲当量 × (1 / 机械减速比)) / 机械部分每圈位移量
                # 其中：1 / 机械减速比 = 减速比分母 / 减速比分子
                electronic_gear_ratio = (encoder_resolution * pulse_equivalent * (1 / mechanical_ratio)) / displacement_per_revolution
                
                formula_parts.append(f"<strong>电子齿轮比计算（反向）：</strong><br>")
                formula_parts.append(f"机械部分每圈位移量 = 负载移动距离 / 电机转数<br>")
                formula_parts.append(f"  = {load_distance} / {motor_revolutions}<br>")
                formula_parts.append(f"  = {displacement_per_revolution:.6f} mm<br><br>")
                formula_parts.append(f"电子齿轮比 = (编码器分辨率 × 脉冲当量 × (1 / 机械减速比)) / 机械部分每圈位移量<br>")
                formula_parts.append(f"  = ({encoder_resolution} × {pulse_equivalent} × {1 / mechanical_ratio:.6f}) / {displacement_per_revolution:.6f}<br>")
                formula_parts.append(f"  = {encoder_resolution * pulse_equivalent * (1 / mechanical_ratio):.6f} / {displacement_per_revolution:.6f}<br>")
                formula_parts.append(f"  = {electronic_gear_ratio:.6f}<br><br>")
            else:
                # 如果没有提供负载移动距离和电机转数，无法用Excel公式计算
                # 使用简化公式（虽然不完全符合Excel，但符合网页逻辑）
                electronic_gear_ratio = encoder_resolution / (pulse_equivalent * mechanical_ratio)
                
                formula_parts.append(f"<strong>电子齿轮比计算（反向）：</strong><br>")
                formula_parts.append(f"电子齿轮比 = 编码器分辨率 / (脉冲当量 × 机械减速比)<br>")
                formula_parts.append(f"  = {encoder_resolution} / ({pulse_equivalent} × {mechanical_ratio})<br>")
                formula_parts.append(f"  = {encoder_resolution} / {pulse_equivalent * mechanical_ratio}<br>")
                formula_parts.append(f"  = {electronic_gear_ratio:.6f}<br><br>")
            
            intermediate_results["electronic_gear_ratio"] = electronic_gear_ratio
            
            # 如果提供了负载移动距离，可以计算电机转数
            if load_distance is not None and load_distance > 0:
                motor_revolutions_calc = load_distance / (encoder_resolution * electronic_gear_ratio * mechanical_ratio * pulse_equivalent)
                intermediate_results["motor_revolutions_calc"] = motor_revolutions_calc
                
                formula_parts.append(f"<strong>电机转数计算：</strong><br>")
                formula_parts.append(f"电机转数 = 负载移动距离 / (编码器分辨率 × 电子齿轮比 × 机械减速比 × 脉冲当量)<br>")
                formula_parts.append(f"  = {load_distance} / ({encoder_resolution} × {electronic_gear_ratio:.6f} × {mechanical_ratio} × {pulse_equivalent})<br>")
                formula_parts.append(f"  = {motor_revolutions_calc:.6f} 转<br>")
            
            result_value = electronic_gear_ratio
            result_unit = ""
            scenario_name = self.SCENARIO_NAMES["reverse"]
            
        # 情况1: 已知负载移动距离和电机转数，计算电子齿轮比
        elif load_distance is not None and motor_revolutions is not None and motor_revolutions > 0:
            # 根据Excel公式：电子齿轮比 = (编码器分辨率 × 脉冲当量) / (机械部分每圈位移量 × 机械减速比)
            # 其中：机械部分每圈位移量 = 负载移动距离 / (电机转数 × 机械减速比)
            # 但正向计算不知道脉冲当量，所以使用另一种公式：
            # 电子齿轮比 = (编码器分辨率 × 机械减速比 × 电机转数) / 负载移动距离
            # 
            # 注意：这个公式和Excel公式在物理意义上等价，但需要知道脉冲当量才能完全对应
            # 这里使用网页上的逻辑
            
            electronic_gear_ratio = (encoder_resolution * mechanical_ratio * motor_revolutions) / load_distance
            intermediate_results["electronic_gear_ratio"] = electronic_gear_ratio
            
            formula_parts.append(f"<strong>电子齿轮比计算：</strong><br>")
            formula_parts.append(f"电子齿轮比 = (编码器分辨率 × 机械减速比 × 电机转数) / 负载移动距离<br>")
            formula_parts.append(f"  = ({encoder_resolution} × {mechanical_ratio} × {motor_revolutions}) / {load_distance}<br>")
            formula_parts.append(f"  = {encoder_resolution * mechanical_ratio * motor_revolutions} / {load_distance}<br>")
            formula_parts.append(f"  = {electronic_gear_ratio:.6f}<br><br>")
            
            # 计算脉冲当量
            pulse_equivalent_calc = load_distance / (encoder_resolution * electronic_gear_ratio * mechanical_ratio * motor_revolutions)
            intermediate_results["pulse_equivalent_calc"] = pulse_equivalent_calc
            
            formula_parts.append(f"<strong>脉冲当量计算：</strong><br>")
            formula_parts.append(f"脉冲当量 = 负载移动距离 / (编码器分辨率 × 电子齿轮比 × 机械减速比 × 电机转数)<br>")
            formula_parts.append(f"  = {load_distance} / ({encoder_resolution} × {electronic_gear_ratio:.6f} × {mechanical_ratio} × {motor_revolutions})<br>")
            formula_parts.append(f"  = {pulse_equivalent_calc:.6f} mm/脉冲<br>")
            
            result_value = electronic_gear_ratio
            result_unit = ""
            scenario_name = self.SCENARIO_NAMES["forward"]
            
        else:
            raise ValueError("必须提供以下参数之一：1) 负载移动距离和电机转数，或 2) 脉冲当量")
        
        # 构建公式字符串
        formula = "".join(formula_parts)
        
        return CurrentCalcResponse(
            result=result_value,
            unit=result_unit,
            formula=formula,
            scenario_name=scenario_name,
            extra=intermediate_results
        )
