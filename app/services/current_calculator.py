"""
电流计算服务
实现常用电流计算公式
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class CurrentCalculator:
    """电流计算器"""
    
    SCENARIO_NAMES = {
        "pure_resistor": "纯电阻负荷",
        "inductive": "感性负荷",
        "single_phase_motor": "单相电动机负荷",
        "three_phase_motor": "三相电动机负荷",
        "residential": "住宅总负荷",
        "wire_resistance": "导线电阻计算",
        "busbar_resistance": "母线电阻计算",
        "wire_current_3phase": "按安全载流量选择导线截面（三相）",
        "wire_current_1phase": "按安全载流量选择导线截面（单相）",
        "voltage_loss": "电压损失计算",
        "voltage_loss_percent": "电压损失率计算",
        "energy_meter_multiplier": "电能表倍率计算",
        "power_from_current_3phase": "三相功率计算（从电流）",
        "power_from_current_1phase": "单相功率计算（从电流）",
        "air_conditioner_home": "家庭用空调器容量选择",
        "air_conditioner_large": "较大场所用空调器容量选择",
        "refrigeration_unit_convert": "制冷量单位换算",
        "voltage_loss_end_load": "负荷在末端的线路电压损失计算",
        "voltage_loss_line_voltage": "线电压的电压损失计算",
        "voltage_loss_percent_formula": "电压损失率公式计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算电流
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "pure_resistor":
            return self._calculate_pure_resistor(params)
        elif scenario == "inductive":
            return self._calculate_inductive(params)
        elif scenario == "single_phase_motor":
            return self._calculate_single_phase_motor(params)
        elif scenario == "three_phase_motor":
            return self._calculate_three_phase_motor(params)
        elif scenario == "residential":
            return self._calculate_residential(params)
        elif scenario == "wire_resistance":
            return self._calculate_wire_resistance(params)
        elif scenario == "busbar_resistance":
            return self._calculate_busbar_resistance(params)
        elif scenario == "wire_current_3phase":
            return self._calculate_wire_current_3phase(params)
        elif scenario == "wire_current_1phase":
            return self._calculate_wire_current_1phase(params)
        elif scenario == "voltage_loss":
            return self._calculate_voltage_loss(params)
        elif scenario == "voltage_loss_percent":
            return self._calculate_voltage_loss_percent(params)
        elif scenario == "energy_meter_multiplier":
            return self._calculate_energy_meter_multiplier(params)
        elif scenario == "power_from_current_3phase":
            return self._calculate_power_from_current_3phase(params)
        elif scenario == "power_from_current_1phase":
            return self._calculate_power_from_current_1phase(params)
        elif scenario == "air_conditioner_home":
            return self._calculate_air_conditioner_home(params)
        elif scenario == "air_conditioner_large":
            return self._calculate_air_conditioner_large(params)
        elif scenario == "refrigeration_unit_convert":
            return self._calculate_refrigeration_unit_convert(params)
        elif scenario == "voltage_loss_end_load":
            return self._calculate_voltage_loss_end_load(params)
        elif scenario == "voltage_loss_line_voltage":
            return self._calculate_voltage_loss_line_voltage(params)
        elif scenario == "voltage_loss_percent_formula":
            return self._calculate_voltage_loss_percent_formula(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_pure_resistor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """纯电阻负荷: I = P / U"""
        power = params.get("power")
        voltage = params.get("voltage")
        
        if power is None or voltage is None:
            raise ValueError("纯电阻负荷计算需要功率和电压参数")
        if voltage == 0:
            raise ValueError("电压不能为0")
        
        result = power / voltage
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula="I = P / U",
            scenario_name=self.SCENARIO_NAMES["pure_resistor"]
        )
    
    def _calculate_inductive(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """感性负荷: I = P / (U × cosφ)"""
        power = params.get("power")
        voltage = params.get("voltage")
        cos_phi = params.get("cos_phi", 0.85)  # 默认功率因数
        
        if power is None or voltage is None:
            raise ValueError("感性负荷计算需要功率和电压参数")
        if voltage == 0 or cos_phi == 0:
            raise ValueError("电压和功率因数不能为0")
        
        result = power / (voltage * cos_phi)
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula="I = P / (U × cosφ)",
            scenario_name=self.SCENARIO_NAMES["inductive"]
        )
    
    def _calculate_single_phase_motor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """单相电动机: I = P / (U × η × cosφ)"""
        power = params.get("power")
        voltage = params.get("voltage")
        efficiency = params.get("efficiency", 0.875)  # 默认效率
        cos_phi = params.get("cos_phi", 0.89)  # 默认功率因数
        
        if power is None or voltage is None:
            raise ValueError("单相电动机计算需要功率和电压参数")
        if voltage == 0 or efficiency == 0 or cos_phi == 0:
            raise ValueError("电压、效率和功率因数不能为0")
        
        result = power / (voltage * efficiency * cos_phi)
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula="I = P / (U × η × cosφ)",
            scenario_name=self.SCENARIO_NAMES["single_phase_motor"]
        )
    
    def _calculate_three_phase_motor(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """三相电动机: I = P / (√3 × U × η × cosφ)"""
        power = params.get("power")
        voltage = params.get("voltage")
        efficiency = params.get("efficiency", 0.875)  # 默认效率
        cos_phi = params.get("cos_phi", 0.89)  # 默认功率因数
        
        if power is None or voltage is None:
            raise ValueError("三相电动机计算需要功率和电压参数")
        if voltage == 0 or efficiency == 0 or cos_phi == 0:
            raise ValueError("电压、效率和功率因数不能为0")
        
        sqrt3 = math.sqrt(3)
        result = power / (sqrt3 * voltage * efficiency * cos_phi)
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula="I = P / (√3 × U × η × cosφ)",
            scenario_name=self.SCENARIO_NAMES["three_phase_motor"]
        )
    
    def _calculate_residential(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """住宅总负荷: 两步计算"""
        total_power = params.get("total_power")
        kc = params.get("kc", 0.5)  # 默认同期系数
        voltage = params.get("voltage", 220)  # 默认电压
        cos_phi = params.get("cos_phi", 0.8)  # 默认功率因数
        
        if total_power is None:
            raise ValueError("住宅总负荷计算需要总功率参数")
        if voltage == 0 or cos_phi == 0:
            raise ValueError("电压和功率因数不能为0")
        
        # 第一步：计算负荷 Pjs = Kc × PΣ
        pjs = kc * total_power
        
        # 第二步：计算电流 Ijs = Pjs / (U × cosφ)
        result = pjs / (voltage * cos_phi)
        
        # 构建详细公式字符串，显示两步计算过程
        formula = f"第一步: Pjs = Kc × PΣ = {kc} × {total_power} = {pjs:.2f}W; 第二步: Ijs = Pjs / (U × cosφ) = {pjs:.2f} / ({voltage} × {cos_phi}) = {result:.4f}A"
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["residential"]
        )
    
    def _calculate_wire_resistance(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """导线电阻计算: Ro = ρ / S, Rt = R20[1 + a20(t-20)]"""
        rho = params.get("rho")  # 电阻率 (Ω·mm²/km)
        area = params.get("area")  # 截面积 (mm²)
        r20 = params.get("r20")  # 20℃时的电阻 (Ω/km)
        a20 = params.get("a20", 0.004)  # 温度系数，默认0.004
        temperature = params.get("temperature", 20)  # 温度 (℃)
        
        # 优先检查温度修正计算（如果提供了r20参数）
        if r20 is not None:
            # 计算温度修正后的电阻 Rt = R20[1 + a20(t-20)]
            if a20 is None:
                a20 = 0.004  # 默认温度系数
            if temperature is None:
                temperature = 20  # 默认温度
            result = r20 * (1 + a20 * (temperature - 20))
            formula = f"Rt = R20[1 + a20(t-20)] = {r20} × [1 + {a20} × ({temperature} - 20)]"
        elif rho is not None and area is not None:
            # 计算基础电阻 Ro = ρ / S
            if area == 0:
                raise ValueError("截面积不能为0")
            result = rho / area
            formula = f"Ro = ρ / S = {rho} / {area}"
        else:
            raise ValueError("导线电阻计算需要电阻率和截面积，或20℃时的电阻值")
        
        return CurrentCalcResponse(
            result=round(result, 6),
            unit="Ω/km",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["wire_resistance"]
        )
    
    def _calculate_busbar_resistance(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """母线电阻计算: R0 = 1000 / (r × S) (mΩ/m)"""
        conductivity = params.get("conductivity")  # 电导率（铜54，铝32）
        area = params.get("area")  # 截面积 (mm²)
        
        if conductivity is None or area is None:
            raise ValueError("母线电阻计算需要电导率和截面积参数")
        if conductivity == 0 or area == 0:
            raise ValueError("电导率和截面积不能为0")
        
        # R0 = 1000 / (r × S)
        result = 1000 / (conductivity * area)
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="mΩ/m",
            formula="R0 = 1000 / (r × S)",
            scenario_name=self.SCENARIO_NAMES["busbar_resistance"]
        )
    
    def _calculate_wire_current_3phase(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """按安全载流量选择导线截面（三相电路）: I = P / (√3 × U × cosφ) 或 I = S / (√3 × U)"""
        power = params.get("power")  # 有功功率 (KW)
        apparent_power = params.get("apparent_power")  # 视在功率 (KVA)
        voltage = params.get("voltage", 380)  # 电压 (V)
        cos_phi = params.get("cos_phi", 0.89)  # 功率因数
        
        if power is not None:
            # 使用有功功率计算: Ijs = Pjs / (√3 × Ue × cosφ)
            if voltage == 0 or cos_phi == 0:
                raise ValueError("电压和功率因数不能为0")
            pjs = power * 1000  # 转换为W
            sqrt3 = math.sqrt(3)
            result = pjs / (sqrt3 * voltage * cos_phi)
            formula = f"Ijs = Pjs / (√3 × Ue × cosφ) = {power} / (√3 × {voltage} × {cos_phi}) = {result:.3f}A"
        elif apparent_power is not None:
            # 使用视在功率计算: Ijs = Sjs / (√3 × Ue)
            if voltage == 0:
                raise ValueError("电压不能为0")
            sjs = apparent_power * 1000  # 转换为VA
            sqrt3 = math.sqrt(3)
            result = sjs / (sqrt3 * voltage)
            formula = f"Ijs = Sjs / (√3 × Ue) = {apparent_power} / (√3 × {voltage}) = {result:.3f}A"
        else:
            raise ValueError("需要提供有功功率或视在功率")
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["wire_current_3phase"]
        )
    
    def _calculate_wire_current_1phase(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """按安全载流量选择导线截面（单相电路）: I = P / (U × cosφ) 或 I = S / U"""
        power = params.get("power")  # 有功功率 (KW)
        apparent_power = params.get("apparent_power")  # 视在功率 (KVA)
        voltage = params.get("voltage", 220)  # 电压 (V)
        cos_phi = params.get("cos_phi", 0.8)  # 功率因数
        
        if power is not None:
            # 使用有功功率计算: Ijs = Pjs / (Ue × cosφ)
            if voltage == 0 or cos_phi == 0:
                raise ValueError("电压和功率因数不能为0")
            pjs = power * 1000  # 转换为W
            result = pjs / (voltage * cos_phi)
            formula = f"Ijs = Pjs / (Ue × cosφ) = {power} / ({voltage} × {cos_phi}) = {result:.3f}A"
        elif apparent_power is not None:
            # 使用视在功率计算: Ijs = Sjs / Ue
            if voltage == 0:
                raise ValueError("电压不能为0")
            sjs = apparent_power * 1000  # 转换为VA
            result = sjs / voltage
            formula = f"Ijs = Sjs / Ue = {apparent_power} / {voltage} = {result:.3f}A"
        else:
            raise ValueError("需要提供有功功率或视在功率")
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="A",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["wire_current_1phase"]
        )
    
    def _calculate_voltage_loss(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电压损失计算: △U = U1 - U2"""
        u1 = params.get("u1")  # 送电端电压 (V)
        u2 = params.get("u2")  # 受电端电压 (V)
        
        if u1 is None or u2 is None:
            raise ValueError("电压损失计算需要送电端电压和受电端电压")
        
        result = u1 - u2
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="V",
            formula="△U = U1 - U2",
            scenario_name=self.SCENARIO_NAMES["voltage_loss"]
        )
    
    def _calculate_voltage_loss_percent(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电压损失率计算: △U% = (U1 - U2) / Ue × 100"""
        u1 = params.get("u1")  # 送电端电压 (V)
        u2 = params.get("u2")  # 受电端电压 (V)
        ue = params.get("ue")  # 线路额定电压 (V)
        
        if u1 is None or u2 is None or ue is None:
            raise ValueError("电压损失率计算需要送电端电压、受电端电压和线路额定电压")
        if ue == 0:
            raise ValueError("线路额定电压不能为0")
        
        # △U% = (U1 - U2) / Ue × 100
        result = (u1 - u2) / ue * 100
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="%",
            formula="△U% = (U1 - U2) / Ue × 100",
            scenario_name=self.SCENARIO_NAMES["voltage_loss_percent"]
        )
    
    def _calculate_energy_meter_multiplier(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电能表倍率计算: K = (KTA/KTAe) × (KTV/KTVe) × Kj"""
        kta = params.get("kta")  # 实际电流互感器变比
        ktae = params.get("ktae", 1)  # 电能表铭牌电流互感器变比，默认1
        ktv = params.get("ktv")  # 实际电压互感器变比
        ktve = params.get("ktve", 1)  # 电能表铭牌电压互感器变比，默认1
        kj = params.get("kj", 1)  # 计能器倍率，默认1
        
        if kta is None or ktv is None:
            raise ValueError("电能表倍率计算需要实际电流互感器变比和电压互感器变比")
        if ktae == 0 or ktve == 0:
            raise ValueError("电能表铭牌变比不能为0")
        
        # K = (KTA/KTAe) × (KTV/KTVe) × Kj
        result = (kta / ktae) * (ktv / ktve) * kj
        
        # 构建详细公式字符串
        formula = f"K = (KTA/KTAe) × (KTV/KTVe) × Kj = ({kta}/{ktae}) × ({ktv}/{ktve}) × {kj} = {result:.0f}"
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["energy_meter_multiplier"]
        )
    
    def _calculate_power_from_current_3phase(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """三相功率计算（从电流）: P = √3 × U × I × cosφ × η"""
        current = params.get("current")  # 电流 (A)
        voltage = params.get("voltage")  # 电压 (V)
        cos_phi = params.get("cos_phi")  # 功率因数
        efficiency = params.get("efficiency", 1.0)  # 效率，默认1.0
        
        if current is None or voltage is None or cos_phi is None:
            raise ValueError("三相功率计算需要电流、电压和功率因数参数")
        if voltage == 0:
            raise ValueError("电压不能为0")
        
        # P = √3 × U × I × cosφ × η (W)
        sqrt3 = math.sqrt(3)
        power_w = sqrt3 * voltage * current * cos_phi * efficiency
        
        # 转换为kW
        power_kw = power_w / 1000
        
        return CurrentCalcResponse(
            result=round(power_kw, 4),
            unit="kW",
            formula="P = √3 × U × I × cosφ × η",
            scenario_name=self.SCENARIO_NAMES["power_from_current_3phase"]
        )
    
    def _calculate_power_from_current_1phase(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """单相功率计算（从电流）: P = U × I × cosφ × η"""
        current = params.get("current")  # 电流 (A)
        voltage = params.get("voltage")  # 电压 (V)
        cos_phi = params.get("cos_phi")  # 功率因数
        efficiency = params.get("efficiency", 1.0)  # 效率，默认1.0
        
        if current is None or voltage is None or cos_phi is None:
            raise ValueError("单相功率计算需要电流、电压和功率因数参数")
        if voltage == 0:
            raise ValueError("电压不能为0")
        
        # P = U × I × cosφ × η (W)
        power_w = voltage * current * cos_phi * efficiency
        
        # 转换为kW
        power_kw = power_w / 1000
        
        return CurrentCalcResponse(
            result=round(power_kw, 4),
            unit="kW",
            formula="P = U × I × cosφ × η",
            scenario_name=self.SCENARIO_NAMES["power_from_current_1phase"]
        )
    
    def _calculate_air_conditioner_home(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """家庭用空调器容量选择: Q = 面积 × 单位面积制冷量"""
        area = params.get("area")  # 房间面积(m²)
        unit_capacity = params.get("unit_capacity", 130)  # 单位面积制冷量(W/m²)，默认130W/m²
        
        if area is None or area <= 0:
            raise ValueError("房间面积必须大于0")
        if unit_capacity <= 0:
            raise ValueError("单位面积制冷量必须大于0")
        
        # 计算制冷量 Q = 面积 × 单位面积制冷量 (W)
        capacity_w = area * unit_capacity
        
        # 转换为kW
        capacity_kw = capacity_w / 1000
        
        return CurrentCalcResponse(
            result=round(capacity_kw, 2),
            unit="kW",
            formula=f"Q = 面积 × 单位面积制冷量 = {area} × {unit_capacity}",
            scenario_name=self.SCENARIO_NAMES["air_conditioner_home"]
        )
    
    def _calculate_air_conditioner_large(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """较大场所用空调器容量选择: Q = k ( q V + η X + u Qz )"""
        # 参数说明：
        # k: 容量裕量系数（短期K=1，长期K=1.05~1.1）
        # q: 房间所需冷量（105~143）
        # V: 房间的总容积(m³)
        # η: 房间总人数
        # X: 人体排热量（坐时X=432KJ/h，活动时X=1591KJ/h）
        # u: 房内设备同时使用率和利用率之积（u=0~0.6）
        # Qz: 房间设备总发热量(KJ)
        
        k = params.get("k", 1.05)  # 容量裕量系数，默认1.05（长期）
        q = params.get("q", 120)  # 房间所需冷量，默认120
        volume = params.get("volume")  # 房间总容积(m³)
        people_count = params.get("people_count", 0)  # 房间总人数，默认0
        x = params.get("x", 432)  # 人体排热量，默认432KJ/h（坐时）
        u = params.get("u", 0)  # 设备同时使用率和利用率之积，默认0
        qz = params.get("qz", 0)  # 房间设备总发热量(KJ)，默认0
        
        if volume is None or volume <= 0:
            raise ValueError("房间总容积必须大于0")
        if q <= 0:
            raise ValueError("房间所需冷量必须大于0")
        if k <= 0:
            raise ValueError("容量裕量系数必须大于0")
        if x <= 0:
            raise ValueError("人体排热量必须大于0")
        if u < 0 or u > 0.6:
            raise ValueError("设备同时使用率和利用率之积应在0~0.6之间")
        if qz < 0:
            raise ValueError("房间设备总发热量不能为负数")
        
        # 计算制冷量 Q = k ( q V + η X + u Qz ) (KJ/h)
        qv_term = q * volume  # 房间所需冷量项
        eta_x_term = people_count * x  # 人体排热量项
        u_qz_term = u * qz  # 设备发热量项
        
        capacity_kj_h = k * (qv_term + eta_x_term + u_qz_term)
        
        # 转换为kW（1kW = 3600KJ/h）
        capacity_kw = capacity_kj_h / 3600
        
        # 构建公式字符串
        formula_parts = []
        formula_parts.append(f"qV = {q} × {volume} = {qv_term:.2f}")
        if people_count > 0:
            formula_parts.append(f"ηX = {people_count} × {x} = {eta_x_term:.2f}")
        if u > 0 and qz > 0:
            formula_parts.append(f"uQz = {u} × {qz} = {u_qz_term:.2f}")
        
        formula_str = f"Q = k ( qV + ηX + uQz ) = {k} × ({qv_term:.2f}"
        if people_count > 0:
            formula_str += f" + {eta_x_term:.2f}"
        if u > 0 and qz > 0:
            formula_str += f" + {u_qz_term:.2f}"
        formula_str += f") = {capacity_kj_h:.2f} KJ/h = {capacity_kw:.2f} kW"
        
        return CurrentCalcResponse(
            result=round(capacity_kw, 2),
            unit="kW",
            formula=formula_str,
            scenario_name=self.SCENARIO_NAMES["air_conditioner_large"]
        )
    
    def _calculate_refrigeration_unit_convert(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """制冷量单位换算"""
        # 换算系数（以W为基准）
        # 1 W = 0.8598 Kcal/h = 3.412 BTU/h = 3.6 KJ/H
        # 1 Kcal/h = 1.163 W = 3.9683 BTU/h = 4.1886 KJ/H
        # 1 BTU/h = 0.293 W = 0.252 Kcal/h = 1.055 KJ/H
        # 1 KJ/H = 0.278 W = 0.239 Kcal/h = 0.948 BTU/h
        
        from_unit = params.get("from_unit")
        to_unit = params.get("to_unit")
        value = params.get("value")
        
        if from_unit is None or to_unit is None or value is None:
            raise ValueError("需要提供：从单位、到单位和数值")
        if value < 0:
            raise ValueError("数值不能为负数")
        if from_unit == to_unit:
            raise ValueError("从单位和到单位不能相同")
        
        # 先转换为W（基准单位）
        value_in_w = None
        if from_unit == "W":
            value_in_w = value
        elif from_unit == "Kcal/h":
            value_in_w = value * 1.163
        elif from_unit == "BTU/h":
            value_in_w = value * 0.293
        elif from_unit == "KJ/H":
            value_in_w = value * 0.278
        else:
            raise ValueError(f"不支持的从单位: {from_unit}")
        
        # 从W转换为目标单位
        result = None
        if to_unit == "W":
            result = value_in_w
        elif to_unit == "Kcal/h":
            result = value_in_w / 1.163
        elif to_unit == "BTU/h":
            result = value_in_w / 0.293
        elif to_unit == "KJ/H":
            result = value_in_w / 0.278
        else:
            raise ValueError(f"不支持的目标单位: {to_unit}")
        
        # 构建公式字符串
        formula = f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        return CurrentCalcResponse(
            result=round(result, 4),
            unit=to_unit,
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["refrigeration_unit_convert"]
        )
    
    def _calculate_voltage_loss_end_load(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """负荷在末端的线路电压损失计算: ΔUx = I (R cosφ + X sinφ) = (PR + QX) / (√3 × U2)"""
        # 方法1: 使用电流、电阻、电抗计算
        current = params.get("current")  # 电流(A)
        resistance = params.get("resistance")  # 线路电阻(Ω)
        reactance = params.get("reactance")  # 线路电抗(Ω)
        cos_phi = params.get("cos_phi")  # 功率因数
        
        # 方法2: 使用功率、电阻、电抗计算
        power = params.get("power")  # 有功功率(KW)
        reactive_power = params.get("reactive_power")  # 无功功率(KVar)
        voltage = params.get("voltage")  # 电压(V)，可以是U2或Ue
        
        # 优先使用方法2（更常用）
        if power is not None and resistance is not None and reactance is not None and voltage is not None:
            # 如果没有提供无功功率，通过有功功率和功率因数计算
            if reactive_power is None:
                if cos_phi is None:
                    raise ValueError("需要提供无功功率或功率因数")
                # Q = P × tan(φ) = P × √(1/cos²φ - 1)
                sin_phi = math.sqrt(1 - cos_phi ** 2)
                tan_phi = sin_phi / cos_phi if cos_phi != 0 else 0
                reactive_power = power * tan_phi
            
            # 转换为W和Var
            power_w = power * 1000
            reactive_power_var = reactive_power * 1000
            
            # ΔUx = (PR + QX) / (√3 × U2)
            voltage_loss = (power_w * resistance + reactive_power_var * reactance) / (math.sqrt(3) * voltage)
            
            formula = f"ΔUx = (PR + QX) / (√3 × U) = ({power}×{resistance} + {reactive_power}×{reactance}) / (√3 × {voltage})"
            
        # 使用方法1
        elif current is not None and resistance is not None and reactance is not None and cos_phi is not None:
            sin_phi = math.sqrt(1 - cos_phi ** 2)
            # ΔUx = I (R cosφ + X sinφ)
            voltage_loss = current * (resistance * cos_phi + reactance * sin_phi)
            
            formula = f"ΔUx = I (R cosφ + X sinφ) = {current} × ({resistance}×{cos_phi} + {reactance}×{sin_phi:.4f})"
        else:
            raise ValueError("需要提供：方法1[电流、电阻、电抗、功率因数] 或 方法2[有功功率、电阻、电抗、电压、无功功率或功率因数]")
        
        return CurrentCalcResponse(
            result=round(voltage_loss, 4),
            unit="V",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["voltage_loss_end_load"]
        )
    
    def _calculate_voltage_loss_line_voltage(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """线电压的电压损失计算: △U1 = √3 × I (R cosφ + X sinφ) = (PR + QX) / U2"""
        # 方法1: 使用电流计算
        current = params.get("current")  # 电流(A)
        resistance = params.get("resistance")  # 线路电阻(Ω)
        reactance = params.get("reactance")  # 线路电抗(Ω)
        cos_phi = params.get("cos_phi")  # 功率因数
        
        # 方法2: 使用功率计算
        power = params.get("power")  # 有功功率(KW)
        reactive_power = params.get("reactive_power")  # 无功功率(KVar)
        voltage = params.get("voltage")  # 电压(V)，U2
        
        # 优先使用方法2（更常用）
        if power is not None and resistance is not None and reactance is not None and voltage is not None:
            # 如果没有提供无功功率，通过有功功率和功率因数计算
            if reactive_power is None:
                if cos_phi is None:
                    raise ValueError("需要提供无功功率或功率因数")
                sin_phi = math.sqrt(1 - cos_phi ** 2)
                tan_phi = sin_phi / cos_phi if cos_phi != 0 else 0
                reactive_power = power * tan_phi
            
            # 转换为W和Var
            power_w = power * 1000
            reactive_power_var = reactive_power * 1000
            
            # △U1 = (PR + QX) / U2
            voltage_loss = (power_w * resistance + reactive_power_var * reactance) / voltage
            
            formula = f"△U1 = (PR + QX) / U2 = ({power}×{resistance} + {reactive_power}×{reactance}) / {voltage}"
            
        # 使用方法1
        elif current is not None and resistance is not None and reactance is not None and cos_phi is not None:
            sin_phi = math.sqrt(1 - cos_phi ** 2)
            sqrt3 = math.sqrt(3)
            # △U1 = √3 × I (R cosφ + X sinφ)
            voltage_loss = sqrt3 * current * (resistance * cos_phi + reactance * sin_phi)
            
            formula = f"△U1 = √3 × I (R cosφ + X sinφ) = √3 × {current} × ({resistance}×{cos_phi} + {reactance}×{sin_phi:.4f})"
        else:
            raise ValueError("需要提供：方法1[电流、电阻、电抗、功率因数] 或 方法2[有功功率、电阻、电抗、电压、无功功率或功率因数]")
        
        return CurrentCalcResponse(
            result=round(voltage_loss, 4),
            unit="V",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["voltage_loss_line_voltage"]
        )
    
    def _calculate_voltage_loss_percent_formula(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电压损失率公式计算: △U% = P × (R cosφ + X sinφ) / (10 × Ue × cosφ)"""
        # 根据图片，公式为：△U% = P (R Cosφ + X Sinφ) / (10 Ue CosΦ)
        # 其中 Ue 单位是 KV
        power = params.get("power")  # 有功功率(KW)
        resistance = params.get("resistance")  # 线路电阻(Ω)
        reactance = params.get("reactance")  # 线路电抗(Ω)
        cos_phi = params.get("cos_phi")  # 功率因数
        ue = params.get("ue_kv") or params.get("ue")  # 线路额定电压(KV)，兼容ue参数
        
        if power is None or resistance is None or reactance is None or cos_phi is None or ue is None:
            raise ValueError("需要提供：有功功率、线路电阻、线路电抗、功率因数、线路额定电压")
        if ue == 0 or cos_phi == 0:
            raise ValueError("线路额定电压和功率因数不能为0")
        
        sin_phi = math.sqrt(1 - cos_phi ** 2)
        
        # △U% = P × (R cosφ + X sinφ) / (10 × Ue × cosφ)
        # 注意：Ue单位是KV，公式中直接使用KV
        numerator = power * (resistance * cos_phi + reactance * sin_phi)
        denominator = 10 * ue * cos_phi
        voltage_loss_percent = numerator / denominator  # 结果已经是百分比
        
        formula = f"△U% = P × (R cosφ + X sinφ) / (10 × Ue × cosφ) = {power} × ({resistance}×{cos_phi} + {reactance}×{sin_phi:.4f}) / (10 × {ue} × {cos_phi})"
        
        return CurrentCalcResponse(
            result=round(voltage_loss_percent, 4),
            unit="%",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["voltage_loss_percent_formula"]
        )

