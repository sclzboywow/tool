"""
电动机启动时端电压计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse


class MotorStartupVoltageCalculator:
    """电动机启动时端电压计算器"""
    
    SCENARIO_NAMES = {
        "motor_startup_voltage": "电动机启动时端电压计算",
        "short_circuit_capacity": "变压器低压母线上的三相短路容量计算",
        "voltage_drop": "电动机启动电压计算"
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """
        根据场景计算电动机启动时端电压
        
        Args:
            scenario: 计算场景
            params: 参数字典
            
        Returns:
            CurrentCalcResponse: 计算结果
        """
        if scenario == "motor_startup_voltage":
            return self._calculate_motor_startup_voltage(params)
        elif scenario == "short_circuit_capacity":
            return self._calculate_short_circuit_capacity(params)
        elif scenario == "voltage_drop":
            return self._calculate_voltage_drop(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_short_circuit_capacity(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """变压器低压母线上的三相短路容量计算"""
        Seb = params.get("Seb")  # 变压器额定容量 (kVA)
        uk = params.get("uk")    # 变压器阻抗电压 (%)
        
        if Seb is None or Seb <= 0:
            raise ValueError("变压器额定容量Seb必须大于0")
        if uk is None or uk <= 0:
            raise ValueError("变压器阻抗电压uk必须大于0")
        
        # Sdm = 100×Seb/uk
        # Excel公式：F6 = 100*D6/E6
        Sdm = 100 * Seb / uk
        
        formula = f"S<sub>dm</sub> = 100 × S<sub>eb</sub> / u<sub>k</sub><br>"
        formula += f"  = 100 × {Seb} / {uk}<br>"
        formula += f"  = {Sdm:.2f} kVA"
        
        return CurrentCalcResponse(
            result=round(Sdm, 2),
            unit="kVA",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["short_circuit_capacity"]
        )
    
    def _calculate_voltage_drop(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电动机启动电压计算"""
        Kiq = params.get("Kiq")      # 启动电流倍数
        Sed = params.get("Sed")      # 启动电动机额定容量 (kVA)
        Sjh = params.get("Sjh")      # 变压器低压侧其他负荷容量 (kVA)
        Seb = params.get("Seb")      # 变压器额定容量 (kVA)
        uk = params.get("uk")        # 变压器阻抗电压 (%)
        Ped = params.get("Ped")      # 电动机额定功率 (kW)
        L = params.get("L")          # 线路长度 (km)
        deltaUx = params.get("deltaUx")  # 每千瓦公里单位电压损失 (%)
        
        # 验证必需参数
        required_params = ["Kiq", "Sed", "Sjh", "Seb", "uk", "Ped", "L", "deltaUx"]
        missing = [p for p in required_params if params.get(p) is None]
        if missing:
            raise ValueError(f"缺少必需参数: {', '.join(missing)}")
        
        if Kiq <= 0:
            raise ValueError("启动电流倍数Kiq必须大于0")
        if Sed <= 0:
            raise ValueError("启动电动机额定容量Sed必须大于0")
        if Sjh < 0:
            raise ValueError("变压器低压侧其他负荷容量Sjh必须大于等于0")
        if Seb <= 0:
            raise ValueError("变压器额定容量Seb必须大于0")
        if uk <= 0:
            raise ValueError("变压器阻抗电压uk必须大于0")
        if Ped <= 0:
            raise ValueError("电动机额定功率Ped必须大于0")
        if L <= 0:
            raise ValueError("线路长度L必须大于0")
        if deltaUx < 0:
            raise ValueError("每千瓦公里单位电压损失⊿Ux必须大于等于0")
        
        # 先计算Sdm
        Sdm = 100 * Seb / uk
        
        # ⊿Uqm = 100(Kiq×Sed + Sjh) / Sdm + Kiq×Ped×L×⊿Ux
        # Excel公式：G6 = (A6*B6+C6)*100/(D6*100/E6)+A6*A9*B9*C9
        # 简化：G6 = (Kiq*Sed+Sjh)*100/Sdm + Kiq*Ped*L*deltaUx
        deltaUqm = 100 * (Kiq * Sed + Sjh) / Sdm + Kiq * Ped * L * deltaUx
        
        formula = f"⊿U<sub>qm</sub> = 100(K<sub>iq</sub>×S<sub>ed</sub> + S<sub>jh</sub>) / S<sub>dm</sub> + K<sub>iq</sub>×P<sub>ed</sub>×L×⊿U<sub>x</sub><br>"
        formula += f"其中：S<sub>dm</sub> = 100 × S<sub>eb</sub> / u<sub>k</sub> = 100 × {Seb} / {uk} = {Sdm:.2f} kVA<br>"
        formula += f"⊿U<sub>qm</sub> = 100({Kiq}×{Sed} + {Sjh}) / {Sdm:.2f} + {Kiq}×{Ped}×{L}×{deltaUx}<br>"
        formula += f"  = 100 × {Kiq * Sed + Sjh:.2f} / {Sdm:.2f} + {Kiq * Ped * L * deltaUx:.4f}<br>"
        formula += f"  = {100 * (Kiq * Sed + Sjh) / Sdm:.4f} + {Kiq * Ped * L * deltaUx:.4f}<br>"
        formula += f"  = {deltaUqm:.4f} %"
        
        return CurrentCalcResponse(
            result=round(deltaUqm, 4),
            unit="%",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["voltage_drop"],
            extra={'Sdm': Sdm}
        )
    
    def _calculate_motor_startup_voltage(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """电动机启动时端电压计算（完整计算）"""
        # 直接调用电压降计算
        return self._calculate_voltage_drop(params)

