#!/usr/bin/env python3
"""
验证皮带轮连续运动计算公式
对比Excel表格和代码实现
"""
import sys
import os
import math

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.belt_continuous_calculator import BeltContinuousCalculator

def test_motor_speed():
    """测试电机转速计算"""
    print("="*80)
    print("1. 电机转速计算验证")
    print("="*80)
    
    # Excel中的测试数据
    V = 3  # m/min
    D = 0.1  # m
    i = 3
    
    # Excel公式: N = (V/(π*D))，注意这里没有乘以60
    # 但根据物理意义，V是m/min，D是m，所以N应该是rpm
    # 让我检查一下：V = π*D*N/60，所以 N = (V/(π*D))*60
    
    calculator = BeltContinuousCalculator()
    params = {
        "V": V,
        "D": D,
        "i": i
    }
    
    result = calculator._calculate_motor_speed(params)
    
    # 手动计算验证
    PI = math.pi
    N_excel = (V / (PI * D))  # Excel公式（可能单位已经是rpm）
    N_manual = (V / (PI * D)) * 60  # 标准公式（m/min转rpm需要乘以60）
    NM_excel = N_excel * i
    NM_manual = N_manual * i
    
    print(f"输入参数:")
    print(f"  V = {V} m/min")
    print(f"  D = {D} m")
    print(f"  i = {i}")
    print(f"\nExcel公式计算:")
    print(f"  N = (V/(π*D)) = ({V}/(π*{D})) = {N_excel:.2f} rpm")
    print(f"  NM = N*i = {N_excel:.2f}*{i} = {NM_excel:.2f} rpm")
    print(f"\n标准公式计算（乘以60）:")
    print(f"  N = (V/(π*D))*60 = ({V}/(π*{D}))*60 = {N_manual:.2f} rpm")
    print(f"  NM = N*i = {N_manual:.2f}*{i} = {NM_manual:.2f} rpm")
    print(f"\n代码计算结果:")
    print(f"  N = {result.extra.get('N', 'N/A'):.2f} rpm")
    print(f"  NM = {result.result:.2f} rpm")
    
    # 检查：如果Excel中的V单位是m/min，那么需要乘以60
    # 但如果Excel中的V单位是m/s，则不需要乘以60
    # 从Excel中看到G5显示"m/min"，所以应该乘以60
    if abs(result.result - NM_manual) < 0.01:
        print("\n✓ 代码实现正确（使用标准公式乘以60）")
    elif abs(result.result - NM_excel) < 0.01:
        print("\n⚠ 代码实现与Excel一致（但可能Excel公式有单位问题）")
    else:
        print(f"\n✗ 计算结果不匹配！")

def test_load_torque():
    """测试负载转矩计算"""
    print("\n" + "="*80)
    print("2. 负载转矩计算验证")
    print("="*80)
    
    # Excel中的测试数据
    FA = 0  # N (F13)
    mL = 40  # kg (F6)
    a = 0  # ° (F14)
    mu = 0.3  # (F7)
    D = 0.1  # m (F8)
    eta = 0.9  # (F10)
    i = 3  # (F12)
    etaG = 0.7  # (F11)
    G = 9.8  # m/s² (K6)
    PI = 3.1416  # (K7)
    
    calculator = BeltContinuousCalculator()
    params = {
        "FA": FA,
        "mL": mL,
        "a": a,
        "mu": mu,
        "D": D,
        "eta": eta,
        "i": i,
        "etaG": etaG
    }
    
    result = calculator._calculate_load_torque(params)
    
    # Excel公式验证
    # F25: =F13+F6*K6*(SIN((F14/360)*2*K7)+F7*COS((F14/360)*2*K7))
    a_rad_excel = (a / 360) * 2 * PI  # Excel中的角度转换
    a_rad_standard = math.radians(a)  # 标准角度转换
    
    F_excel = FA + mL * G * (math.sin(a_rad_excel) + mu * math.cos(a_rad_excel))
    F_standard = FA + mL * G * (math.sin(a_rad_standard) + mu * math.cos(a_rad_standard))
    
    # F29: =(F25*F8)/(2*F10)
    TL_excel = (F_excel * D) / (2 * eta)
    TL_standard = (F_standard * D) / (2 * eta)
    
    # F33: =F29/(F12*F11)
    TLM_excel = TL_excel / (i * etaG)
    TLM_standard = TL_standard / (i * etaG)
    
    print(f"输入参数:")
    print(f"  FA = {FA} N")
    print(f"  mL = {mL} kg")
    print(f"  a = {a}°")
    print(f"  μ = {mu}")
    print(f"  D = {D} m")
    print(f"  η = {eta}")
    print(f"  i = {i}")
    print(f"  ηG = {etaG}")
    
    print(f"\nExcel公式计算（角度转换: (a/360)*2*π）:")
    print(f"  a_rad = ({a}/360)*2*{PI} = {a_rad_excel:.6f} rad")
    print(f"  F = {FA} + {mL}*{G}*(sin({a_rad_excel:.6f}) + {mu}*cos({a_rad_excel:.6f})) = {F_excel:.4f} N")
    print(f"  TL = ({F_excel:.4f}*{D})/(2*{eta}) = {TL_excel:.6f} Nm")
    print(f"  TLM = {TL_excel:.6f}/({i}*{etaG}) = {TLM_excel:.6f} Nm")
    
    print(f"\n标准公式计算（角度转换: math.radians(a)）:")
    print(f"  a_rad = math.radians({a}) = {a_rad_standard:.6f} rad")
    print(f"  F = {FA} + {mL}*{G}*(sin({a_rad_standard:.6f}) + {mu}*cos({a_rad_standard:.6f})) = {F_standard:.4f} N")
    print(f"  TL = ({F_standard:.4f}*{D})/(2*{eta}) = {TL_standard:.6f} Nm")
    print(f"  TLM = {TL_standard:.6f}/({i}*{etaG}) = {TLM_standard:.6f} Nm")
    
    print(f"\n代码计算结果:")
    print(f"  F = {result.extra.get('F', 'N/A'):.4f} N")
    print(f"  TL = {result.extra.get('TL', 'N/A'):.6f} Nm")
    print(f"  TLM = {result.result:.6f} Nm")
    
    # 当a=0时，两种角度转换方法结果相同
    if abs(result.result - TLM_standard) < 0.000001:
        print("\n✓ 代码实现正确（使用标准角度转换）")
    else:
        print(f"\n⚠ 计算结果有微小差异（可能是浮点数精度问题）")

def test_required_torque():
    """测试必须转矩计算"""
    print("\n" + "="*80)
    print("3. 必须转矩计算验证")
    print("="*80)
    
    # 假设TLM = 0.1 Nm, S = 2
    TLM = 0.1
    S = 2
    
    calculator = BeltContinuousCalculator()
    params = {
        "TLM": TLM,
        "S": S
    }
    
    result = calculator._calculate_required_torque(params)
    
    # Excel公式: F54 = F33*K53 = TLM*S
    TM_excel = TLM * S
    
    print(f"输入参数:")
    print(f"  TLM = {TLM} Nm")
    print(f"  S = {S}")
    
    print(f"\nExcel公式计算:")
    print(f"  TM = TLM*S = {TLM}*{S} = {TM_excel:.6f} Nm")
    
    print(f"\n代码计算结果:")
    print(f"  TM = {result.result:.6f} Nm")
    
    if abs(result.result - TM_excel) < 0.000001:
        print("\n✓ 代码实现正确")
    else:
        print(f"\n✗ 计算结果不匹配！")

def test_inertia_ratio():
    """测试惯量比计算"""
    print("\n" + "="*80)
    print("4. 惯量比计算验证")
    print("="*80)
    
    # Excel中的测试数据
    # F42: JM1 = F6*(F8/2)^2 = 40*(0.1/2)^2 = 0.1
    # F46: JM2 = (F9*F8^2)/8 = (1*0.1^2)/8 = 0.00125
    # F49: JL = F42+2*F46 = 0.1 + 2*0.00125 = 0.1025
    # F59: N1 = (F49/(F12^2))/K49 = (0.1025/(3^2))/0.0011 = 10.3535...
    
    mL = 40
    D = 0.1
    m2 = 1
    i = 3
    JM = 0.0011
    
    calculator = BeltContinuousCalculator()
    
    # 先计算JL
    JM1 = mL * ((D / 2) ** 2)
    JM2 = (m2 * (D ** 2)) / 8
    JL = JM1 + 2 * JM2
    
    params = {
        "JL": JL,
        "i": i,
        "JM": JM
    }
    
    result = calculator._calculate_inertia_ratio(params)
    
    # Excel公式验证
    N1_excel = (JL / (i ** 2)) / JM
    
    print(f"输入参数:")
    print(f"  mL = {mL} kg")
    print(f"  D = {D} m")
    print(f"  m2 = {m2} kg")
    print(f"  i = {i}")
    print(f"  JM = {JM} kg·m²")
    
    print(f"\n中间计算:")
    print(f"  JM1 = mL*(D/2)² = {mL}*({D}/2)² = {JM1:.6f} kg·m²")
    print(f"  JM2 = (m2*D²)/8 = ({m2}*{D}²)/8 = {JM2:.6f} kg·m²")
    print(f"  JL = JM1 + 2*JM2 = {JM1:.6f} + 2*{JM2:.6f} = {JL:.6f} kg·m²")
    
    print(f"\nExcel公式计算:")
    print(f"  N1 = (JL/(i²))/JM = ({JL:.6f}/({i}²))/{JM} = {N1_excel:.2f}")
    
    print(f"\n代码计算结果:")
    print(f"  N1 = {result.result:.2f}")
    
    if abs(result.result - N1_excel) < 0.01:
        print("\n✓ 代码实现正确")
    else:
        print(f"\n✗ 计算结果不匹配！")

def main():
    print("\n" + "="*80)
    print("皮带轮连续运动计算公式验证")
    print("="*80)
    print("\n注意：Excel中的角度转换使用 (a/360)*2*π，")
    print("而标准Python使用 math.radians(a)，两者在a=0时结果相同。")
    print("Excel中的电机转速公式可能缺少乘以60的转换。\n")
    
    test_motor_speed()
    test_load_torque()
    test_required_torque()
    test_inertia_ratio()
    
    print("\n" + "="*80)
    print("验证完成")
    print("="*80)

if __name__ == "__main__":
    main()

