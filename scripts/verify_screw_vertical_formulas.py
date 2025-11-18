#!/usr/bin/env python3
"""
验证丝杠垂直运动选型计算公式的正确性
"""
import sys
import os
import math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.screw_vertical_calculator import ScrewVerticalCalculator

def verify_speed_curve():
    """验证速度曲线 - 加速时间计算"""
    print("="*80)
    print("1. 速度曲线 - 加速时间计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    test_cases = [
        {"t": 3.0, "A": 0.25, "expected": 0.75},
        {"t": 1.0, "A": 0.25, "expected": 0.25},
        {"t": 2.0, "A": 0.5, "expected": 1.0},
        {"t": 0.5, "A": 0.3, "expected": 0.15},
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_speed_curve(case)
        expected = case["expected"]
        actual = result.result
        diff = abs(actual - expected)
        passed = diff < 0.0001
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        print(f"  测试 {i}: t={case['t']}s, A={case['A']}")
        print(f"    期望: {expected}s, 实际: {actual}s, 差异: {diff:.6f}, 状态: {status}")
    
    print(f"\n  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_motor_speed():
    """验证电机转速计算"""
    print("="*80)
    print("2. 电机转速计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    test_cases = [
        {"Vl": 24.0, "PB": 0.025, "expected": 960.0},  # Excel示例
        {"Vl": 10.0, "PB": 0.01, "expected": 1000.0},
        {"Vl": 5.0, "PB": 0.005, "expected": 1000.0},
        {"Vl": 20.0, "PB": 0.02, "expected": 1000.0},
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_motor_speed(case)
        expected = case["expected"]
        actual = result.result
        diff = abs(actual - expected)
        passed = diff < 0.01
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        print(f"  测试 {i}: Vl={case['Vl']} m/min, PB={case['PB']} m")
        print(f"    期望: {expected} rpm, 实际: {actual} rpm, 差异: {diff:.4f}, 状态: {status}")
    
    # 单位验证
    print(f"\n  单位验证: (m/min) / m = 1/min = rpm ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_load_torque():
    """验证负荷转矩计算"""
    print("="*80)
    print("3. 负荷转矩计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    # Excel示例数据：Vl=24, M=30, a=90°, μ=0.1, PB=0.025, η=0.9, FA=0
    # F = FA + M×G×(sin(90°) + μ×cos(90°)) = 0 + 30×9.8×(1 + 0.1×0) = 294 N
    # TL = (F × PB) / (2π × η) = (294 × 0.025) / (2π × 0.9) ≈ 1.300 Nm
    
    test_cases = [
        {
            "FA": 0, "M": 30, "a": 90, "mu": 0.1, "PB": 0.025, "eta": 0.9,
            "expected_F": 294.0,  # 30 × 9.8 × sin(90°) = 294
            "expected_TL": 1.300  # (294 × 0.025) / (2π × 0.9) ≈ 1.300
        },
        {
            "FA": 0, "M": 10, "a": 0, "mu": 0.1, "PB": 0.01, "eta": 0.9,
            "expected_F": 9.8,  # 10 × 9.8 × (0 + 0.1×1) = 9.8
            "expected_TL": 0.0173  # (9.8 × 0.01) / (2π × 0.9) ≈ 0.0173
        },
        {
            "FA": 50, "M": 20, "a": 90, "mu": 0.1, "PB": 0.02, "eta": 0.9,
            "expected_F": 246.0,  # 50 + 20 × 9.8 × 1 = 246
            "expected_TL": 0.869  # (246 × 0.02) / (2π × 0.9) ≈ 0.869
        },
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_load_torque(case)
        expected_F = case["expected_F"]
        expected_TL = case["expected_TL"]
        actual_F = result.extra.get('F') if result.extra else None
        actual_TL = result.result
        
        F_passed = abs(actual_F - expected_F) < 0.1 if actual_F else False
        TL_passed = abs(actual_TL - expected_TL) < 0.01
        passed = F_passed and TL_passed
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        
        print(f"  测试 {i}: FA={case['FA']}N, M={case['M']}kg, a={case['a']}°, μ={case['mu']}, PB={case['PB']}m, η={case['eta']}")
        if actual_F:
            print(f"    轴向负载F: 期望={expected_F}N, 实际={actual_F:.4f}N, 差异={abs(actual_F - expected_F):.4f}, 状态={'✓' if F_passed else '✗'}")
        print(f"    负载转矩TL: 期望={expected_TL}Nm, 实际={actual_TL:.6f}Nm, 差异={abs(actual_TL - expected_TL):.6f}, 状态={'✓' if TL_passed else '✗'}")
    
    print(f"\n  物理原理验证:")
    print(f"    - 轴向负载F = FA + M×G×(sin a + μ×cos a) ✓")
    print(f"    - 负载转矩TL = (F × PB) / (2π × η) ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_acceleration_torque():
    """验证加速转矩计算"""
    print("="*80)
    print("4. 加速转矩计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    # Excel示例数据：
    # M=30, PB=0.025, LB=1.4, DB=0.035, MC=0.5, DC=0.05, NM=960, JM=0.0002, t0=0.75
    # JL1 = 30 × (0.025/(2π))² = 30 × (0.0039789)² = 30 × 0.00001583 = 0.0004749 kg·m²
    # JB = π × 7900 × 1.4 × 0.035⁴ / 32 = π × 7900 × 1.4 × 0.0000015 / 32 ≈ 0.000163 kg·m²
    # JC = 0.5 × 0.05² / 8 = 0.5 × 0.0025 / 8 = 0.00015625 kg·m²
    # JL = 0.0004749 + 0.000163 + 0.00015625 ≈ 0.000794 kg·m²
    # TS = 2π × 960 × (0.0002 + 0.000794) / (60 × 0.75) = 2π × 960 × 0.000994 / 45 ≈ 0.133 Nm
    
    test_cases = [
        {
            "M": 30, "PB": 0.025, "LB": 1.4, "DB": 0.035, "MC": 0.5, "DC": 0.05,
            "NM": 960, "JM": 0.0002, "t0": 0.75,
            "expected_JL1": 0.000475,
            "expected_JB": 0.001629,  # 修正：π × 7900 × 1.4 × 0.035⁴ / 32 = 0.001629
            "expected_JC": 0.000156,
            "expected_JL": 0.002261,  # 修正：0.000475 + 0.001629 + 0.000156 = 0.002260
            "expected_TS": 0.330  # 修正：2π × 960 × (0.0002 + 0.002261) / (60 × 0.75) ≈ 0.330
        },
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_acceleration_torque(case)
        extra = result.extra if result.extra else {}
        
        JL1 = extra.get('JL1', 0)
        JB = extra.get('JB', 0)
        JC = extra.get('JC', 0)
        JL = extra.get('JL', 0)
        TS = result.result
        
        JL1_passed = abs(JL1 - case["expected_JL1"]) < 0.0001
        JB_passed = abs(JB - case["expected_JB"]) < 0.0001
        JC_passed = abs(JC - case["expected_JC"]) < 0.0001
        JL_passed = abs(JL - case["expected_JL"]) < 0.0001
        TS_passed = abs(TS - case["expected_TS"]) < 0.01
        
        passed = JL1_passed and JB_passed and JC_passed and JL_passed and TS_passed
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        
        print(f"  测试 {i}: M={case['M']}kg, PB={case['PB']}m, LB={case['LB']}m, DB={case['DB']}m")
        print(f"    MC={case['MC']}kg, DC={case['DC']}m, NM={case['NM']}rpm, JM={case['JM']}kg·m², t0={case['t0']}s")
        print(f"    JL1: 期望={case['expected_JL1']:.6f}, 实际={JL1:.6f}, 状态={'✓' if JL1_passed else '✗'}")
        print(f"    JB: 期望={case['expected_JB']:.6f}, 实际={JB:.6f}, 状态={'✓' if JB_passed else '✗'}")
        print(f"    JC: 期望={case['expected_JC']:.6f}, 实际={JC:.6f}, 状态={'✓' if JC_passed else '✗'}")
        print(f"    JL: 期望={case['expected_JL']:.6f}, 实际={JL:.6f}, 状态={'✓' if JL_passed else '✗'}")
        print(f"    TS: 期望={case['expected_TS']:.6f}, 实际={TS:.6f}, 状态={'✓' if TS_passed else '✗'}")
    
    print(f"\n  物理原理验证:")
    print(f"    - JL1 = M × (PB/(2π))² (直线运动质量等效为旋转惯量) ✓")
    print(f"    - JB = (π/32) × ρ × LB × DB⁴ (实心圆柱体转动惯量) ✓")
    print(f"    - JC = MC × DC² / 8 (薄圆盘转动惯量) ✓")
    print(f"    - JL = JL1 + JB + JC (转动惯量叠加) ✓")
    print(f"    - TS = (2π × NM × (JM + JL)) / (60 × t0) (角加速度关系) ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_required_torque():
    """验证必须转矩计算"""
    print("="*80)
    print("5. 必须转矩计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    test_cases = [
        {"TL": 1.300, "TS": 0.133, "S": 2, "expected": 2.866},  # Excel示例
        {"TL": 0.5, "TS": 0.3, "S": 1, "expected": 0.8},
        {"TL": 1.0, "TS": 0.5, "S": 1.5, "expected": 2.25},
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_required_torque(case)
        expected = case["expected"]
        actual = result.result
        diff = abs(actual - expected)
        passed = diff < 0.01
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        print(f"  测试 {i}: TL={case['TL']}Nm, TS={case['TS']}Nm, S={case['S']}")
        print(f"    期望: {expected}Nm, 实际: {actual}Nm, 差异: {diff:.6f}, 状态: {status}")
    
    print(f"\n  物理原理验证:")
    print(f"    - TM = (TL + TS) × S (转矩叠加和安全系数) ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_inertia_ratio_motor():
    """验证负荷与电机惯量比计算"""
    print("="*80)
    print("6. 负荷与电机惯量比计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    test_cases = [
        {"JL": 0.000794, "JM": 0.0002, "expected": 3.97},  # Excel示例
        {"JL": 0.001, "JM": 0.0002, "expected": 5.0},
        {"JL": 0.002, "JM": 0.0005, "expected": 4.0},
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_inertia_ratio_motor(case)
        expected = case["expected"]
        actual = result.result
        diff = abs(actual - expected)
        passed = diff < 0.01
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        print(f"  测试 {i}: JL={case['JL']}kg·m², JM={case['JM']}kg·m²")
        print(f"    期望: {expected}, 实际: {actual}, 差异: {diff:.4f}, 状态: {status}")
    
    print(f"\n  物理原理验证:")
    print(f"    - I1 = JL / JM (惯量比，用于评估动态响应) ✓")
    print(f"    - 通常建议 I1 ≤ 5 ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def verify_inertia_ratio_reducer():
    """验证负荷与减速机惯量比计算"""
    print("="*80)
    print("7. 负荷与减速机惯量比计算")
    print("="*80)
    calculator = ScrewVerticalCalculator()
    
    test_cases = [
        {"JL": 0.000794, "JM": 0.0002, "i": 4, "expected": 0.248},  # Excel示例: 0.000794 / (0.0002 × 16) = 0.248
        {"JL": 0.001, "JM": 0.0002, "i": 4, "expected": 0.3125},  # 0.001 / (0.0002 × 16) = 0.3125
        {"JL": 0.002, "JM": 0.0005, "i": 2, "expected": 1.0},  # 0.002 / (0.0005 × 4) = 1.0
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_inertia_ratio_reducer(case)
        expected = case["expected"]
        actual = result.result
        diff = abs(actual - expected)
        passed = diff < 0.01
        status = "✓" if passed else "✗"
        if not passed:
            all_passed = False
        print(f"  测试 {i}: JL={case['JL']}kg·m², JM={case['JM']}kg·m², i={case['i']}")
        print(f"    期望: {expected}, 实际: {actual}, 差异: {diff:.4f}, 状态: {status}")
    
    print(f"\n  物理原理验证:")
    print(f"    - I2 = JL / (JM × i²) (减速机折算后的惯量比) ✓")
    print(f"    - 减速机将负载惯量按i²比例折算到电机轴 ✓")
    print(f"  结果: {'所有测试通过 ✓' if all_passed else '部分测试失败 ✗'}\n")
    return all_passed

def main():
    """主函数"""
    print("\n" + "="*80)
    print("丝杠垂直运动选型计算公式验证报告")
    print("="*80 + "\n")
    
    results = []
    results.append(("速度曲线 - 加速时间", verify_speed_curve()))
    results.append(("电机转速", verify_motor_speed()))
    results.append(("负荷转矩", verify_load_torque()))
    results.append(("加速转矩", verify_acceleration_torque()))
    results.append(("必须转矩", verify_required_torque()))
    results.append(("惯量比(电机)", verify_inertia_ratio_motor()))
    results.append(("惯量比(减速机)", verify_inertia_ratio_reducer()))
    
    print("="*80)
    print("验证结果总结")
    print("="*80)
    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"  {name:20s}: {status}")
        if not passed:
            all_passed = False
    
    print("="*80)
    if all_passed:
        print("✅ 所有7个公式验证通过")
    else:
        print("❌ 部分公式验证失败，请检查")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()

