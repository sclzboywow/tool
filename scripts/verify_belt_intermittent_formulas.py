#!/usr/bin/env python3
"""
验证皮带轮间歇运动选型计算公式的正确性
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.belt_intermittent_calculator import BeltIntermittentCalculator

def test_speed_curve():
    """测试速度曲线 - 加速时间计算"""
    print("=" * 60)
    print("1. 速度曲线 - 加速时间计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：t=0.07s, A=0.5
    params = {
        't': 0.07,
        'A': 0.5
    }
    
    result = calculator.calculate('speed_curve', params)
    
    # 手动计算验证
    # t0 = t × A = 0.07 × 0.5 = 0.035
    expected_t0 = 0.07 * 0.5
    
    print(f"输入参数: t={params['t']}s, A={params['A']}")
    print(f"计算结果: t₀ = {result.result:.6f} s")
    print(f"期望结果: t₀ = {expected_t0:.6f} s")
    print(f"公式: t₀ = t × A = {params['t']} × {params['A']} = {expected_t0:.6f}")
    
    assert abs(result.result - expected_t0) < 1e-6, f"计算结果不匹配: {result.result} != {expected_t0}"
    print("✓ 测试通过\n")


def test_motor_speed():
    """测试电机转速计算"""
    print("=" * 60)
    print("2. 电机转速计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：L=0.09m, D=0.052m, t=0.07s, t0=0.035s, i=1
    params = {
        'L': 0.09,
        'D': 0.052,
        't': 0.07,
        't0': 0.035,
        'i': 1
    }
    
    result = calculator.calculate('motor_speed', params)
    
    # 手动计算验证
    # β = 2×(L/D)/(t₀×(t-t₀)) = 2×(0.09/0.052)/(0.035×(0.07-0.035))
    #   = 2×1.7308/(0.035×0.035) = 3.4616/0.001225 = 2825.8 rad/s²
    beta = 2 * (params['L'] / params['D']) / (params['t0'] * (params['t'] - params['t0']))
    # N = (β×t₀/(2π))×60 = (2825.8×0.035/(2π))×60
    N = (beta * params['t0'] / (2 * 3.1416)) * 60
    # βM = i×β = 1×2825.8 = 2825.8 rad/s²
    betaM = params['i'] * beta
    # NM = N×i = 943.8×1 = 943.8 rpm
    NM = N * params['i']
    
    print(f"输入参数: L={params['L']}m, D={params['D']}m, t={params['t']}s, t₀={params['t0']}s, i={params['i']}")
    print(f"计算结果:")
    print(f"  β = {result.extra['beta']:.4f} rad/s²")
    print(f"  N = {result.extra['N']:.2f} rpm")
    print(f"  βM = {result.extra['betaM']:.4f} rad/s²")
    print(f"  NM = {result.result:.2f} rpm")
    print(f"期望结果:")
    print(f"  β = {beta:.4f} rad/s²")
    print(f"  N = {N:.2f} rpm")
    print(f"  βM = {betaM:.4f} rad/s²")
    print(f"  NM = {NM:.2f} rpm")
    
    assert abs(result.extra['beta'] - beta) < 1, f"β计算不匹配"
    assert abs(result.extra['N'] - N) < 1, f"N计算不匹配"
    assert abs(result.extra['betaM'] - betaM) < 1, f"βM计算不匹配"
    assert abs(result.result - NM) < 1, f"NM计算不匹配"
    print("✓ 测试通过\n")


def test_load_torque():
    """测试负载转矩计算"""
    print("=" * 60)
    print("3. 负载转矩计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：FA=0N, mL=0.5kg, a=0°, μ=0.3, D=0.052m, η=0.9, i=1, ηG=0.7
    params = {
        'FA': 0,
        'mL': 0.5,
        'a': 0,
        'mu': 0.3,
        'D': 0.052,
        'eta': 0.9,
        'i': 1,
        'etaG': 0.7
    }
    
    result = calculator.calculate('load_torque', params)
    
    # 手动计算验证
    import math
    G = 9.8
    # F = FA + mL×g×(sin a + μ×cos a) = 0 + 0.5×9.8×(sin 0° + 0.3×cos 0°)
    #   = 0 + 0.5×9.8×(0 + 0.3×1) = 0.5×9.8×0.3 = 1.47 N
    F = params['FA'] + params['mL'] * G * (math.sin(math.radians(params['a'])) + params['mu'] * math.cos(math.radians(params['a'])))
    # TL = (F × D) / (2 × η) = (1.47 × 0.052) / (2 × 0.9) = 0.07644 / 1.8 = 0.04247 Nm
    TL = (F * params['D']) / (2 * params['eta'])
    # TLM = TL / (i × ηG) = 0.04247 / (1 × 0.7) = 0.06067 Nm
    TLM = TL / (params['i'] * params['etaG'])
    
    print(f"输入参数: FA={params['FA']}N, mL={params['mL']}kg, a={params['a']}°, μ={params['mu']}, D={params['D']}m, η={params['eta']}, i={params['i']}, ηG={params['etaG']}")
    print(f"计算结果:")
    print(f"  F = {result.extra['F']:.4f} N")
    print(f"  TL = {result.extra['TL']:.6f} Nm")
    print(f"  TLM = {result.result:.6f} Nm")
    print(f"期望结果:")
    print(f"  F = {F:.4f} N")
    print(f"  TL = {TL:.6f} Nm")
    print(f"  TLM = {TLM:.6f} Nm")
    
    assert abs(result.extra['F'] - F) < 0.01, f"F计算不匹配"
    assert abs(result.extra['TL'] - TL) < 0.001, f"TL计算不匹配"
    assert abs(result.result - TLM) < 0.001, f"TLM计算不匹配"
    print("✓ 测试通过\n")


def test_acceleration_torque():
    """测试电机轴加速转矩计算"""
    print("=" * 60)
    print("4. 电机轴加速转矩计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：mL=0.5kg, D=0.052m, m2=1kg, i=1, JM=0.00027kg·m², βM=2825.8rad/s², ηG=0.7
    params = {
        'mL': 0.5,
        'D': 0.052,
        'm2': 1,
        'i': 1,
        'JM': 0.00027,
        'betaM': 2825.8,
        'etaG': 0.7
    }
    
    result = calculator.calculate('acceleration_torque', params)
    
    # 手动计算验证
    # JM1 = mL × (D/2)² = 0.5 × (0.052/2)² = 0.5 × 0.000676 = 0.000338 kg·m²
    JM1 = params['mL'] * ((params['D'] / 2) ** 2)
    # JM2 = (m2 × D²) / 8 = (1 × 0.052²) / 8 = 0.002704 / 8 = 0.000338 kg·m²
    JM2 = (params['m2'] * (params['D'] ** 2)) / 8
    # JL = JM1 + 2×JM2 = 0.000338 + 2×0.000338 = 0.001014 kg·m²
    JL = JM1 + 2 * JM2
    # J = JL/(i²) + JM = 0.001014/(1²) + 0.00027 = 0.001284 kg·m²
    J = JL / (params['i'] ** 2) + params['JM']
    # TS = J × βM / ηG = 0.001284 × 2825.8 / 0.7 = 3.628 / 0.7 = 5.183 Nm
    TS = J * params['betaM'] / params['etaG']
    
    print(f"输入参数: mL={params['mL']}kg, D={params['D']}m, m2={params['m2']}kg, i={params['i']}, JM={params['JM']}kg·m², βM={params['betaM']}rad/s², ηG={params['etaG']}")
    print(f"计算结果:")
    print(f"  JM1 = {result.extra['JM1']:.6f} kg·m²")
    print(f"  JM2 = {result.extra['JM2']:.6f} kg·m²")
    print(f"  JL = {result.extra['JL']:.6f} kg·m²")
    print(f"  J = {result.extra['J']:.6f} kg·m²")
    print(f"  TS = {result.result:.6f} Nm")
    print(f"期望结果:")
    print(f"  JM1 = {JM1:.6f} kg·m²")
    print(f"  JM2 = {JM2:.6f} kg·m²")
    print(f"  JL = {JL:.6f} kg·m²")
    print(f"  J = {J:.6f} kg·m²")
    print(f"  TS = {TS:.6f} Nm")
    
    assert abs(result.extra['JM1'] - JM1) < 0.0001, f"JM1计算不匹配"
    assert abs(result.extra['JM2'] - JM2) < 0.0001, f"JM2计算不匹配"
    assert abs(result.extra['JL'] - JL) < 0.0001, f"JL计算不匹配"
    assert abs(result.extra['J'] - J) < 0.0001, f"J计算不匹配"
    assert abs(result.result - TS) < 0.01, f"TS计算不匹配"
    print("✓ 测试通过\n")


def test_required_torque():
    """测试必须转矩计算"""
    print("=" * 60)
    print("5. 必须转矩计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：TLM=0.06067Nm, TS=5.183Nm, S=2
    params = {
        'TLM': 0.06067,
        'TS': 5.183,
        'S': 2
    }
    
    result = calculator.calculate('required_torque', params)
    
    # 手动计算验证
    # TM = (TLM + TS) × S = (0.06067 + 5.183) × 2 = 5.24367 × 2 = 10.48734 Nm
    TM = (params['TLM'] + params['TS']) * params['S']
    
    print(f"输入参数: TLM={params['TLM']}Nm, TS={params['TS']}Nm, S={params['S']}")
    print(f"计算结果: TM = {result.result:.6f} Nm")
    print(f"期望结果: TM = {TM:.6f} Nm")
    print(f"公式: TM = (TLM + TS) × S = ({params['TLM']} + {params['TS']}) × {params['S']} = {TM:.6f}")
    
    assert abs(result.result - TM) < 0.001, f"计算结果不匹配: {result.result} != {TM}"
    print("✓ 测试通过\n")


def test_inertia_ratio():
    """测试惯量比计算"""
    print("=" * 60)
    print("6. 惯量比计算")
    print("=" * 60)
    
    calculator = BeltIntermittentCalculator()
    
    # 测试用例：JL=0.001014kg·m², i=1, JM=0.00027kg·m²
    params = {
        'JL': 0.001014,
        'i': 1,
        'JM': 0.00027
    }
    
    result = calculator.calculate('inertia_ratio', params)
    
    # 手动计算验证
    # N1 = (JL/(i²)) / JM = (0.001014/(1²)) / 0.00027 = 0.001014 / 0.00027 = 3.7556
    N1 = (params['JL'] / (params['i'] ** 2)) / params['JM']
    
    print(f"输入参数: JL={params['JL']}kg·m², i={params['i']}, JM={params['JM']}kg·m²")
    print(f"计算结果: N1 = {result.result:.2f}")
    print(f"期望结果: N1 = {N1:.2f}")
    print(f"公式: N1 = (JL/(i²)) / JM = ({params['JL']}/({params['i']}²)) / {params['JM']} = {N1:.2f}")
    
    assert abs(result.result - N1) < 0.1, f"计算结果不匹配: {result.result} != {N1}"
    print("✓ 测试通过\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("皮带轮间歇运动选型计算公式验证测试")
    print("=" * 60 + "\n")
    
    try:
        test_speed_curve()
        test_motor_speed()
        test_load_torque()
        test_acceleration_torque()
        test_required_torque()
        test_inertia_ratio()
        
        print("=" * 60)
        print("所有测试通过！✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

