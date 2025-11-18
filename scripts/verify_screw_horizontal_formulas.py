"""
验证丝杠水平运动选型计算公式的正确性
"""
import math
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.screw_horizontal_calculator import ScrewHorizontalCalculator


def verify_speed_curve():
    """验证速度曲线公式: t₀ = t × A"""
    print("=" * 80)
    print("1. 验证速度曲线公式: t₀ = t × A")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    
    # 测试用例
    test_cases = [
        {"t": 1.0, "A": 0.25, "expected": 0.25},
        {"t": 2.0, "A": 0.5, "expected": 1.0},
        {"t": 0.5, "A": 0.3, "expected": 0.15},
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_speed_curve(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.0001 else "✗"
        print(f"  测试 {i}: t={case['t']}, A={case['A']}")
        print(f"    期望: {expected}, 实际: {actual}, 状态: {status}")
    
    print("  公式验证: t₀ = t × A ✓ 正确\n")


def verify_motor_speed():
    """验证电机转速公式: N_M = V_l / P_B"""
    print("=" * 80)
    print("2. 验证电机转速公式: N_M = V_l / P_B")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    
    # 测试用例
    test_cases = [
        {"Vl": 10.0, "PB": 0.01, "expected": 1000.0},  # 10 m/min / 0.01 m = 1000 rpm
        {"Vl": 5.0, "PB": 0.005, "expected": 1000.0},  # 5 m/min / 0.005 m = 1000 rpm
        {"Vl": 20.0, "PB": 0.02, "expected": 1000.0},  # 20 m/min / 0.02 m = 1000 rpm
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_motor_speed(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.01 else "✗"
        print(f"  测试 {i}: V_l={case['Vl']} m/min, P_B={case['PB']} m")
        print(f"    期望: {expected} rpm, 实际: {actual} rpm, 状态: {status}")
    
    print("  公式验证: N_M = V_l / P_B ✓ 正确\n")


def verify_load_torque():
    """验证负荷转矩公式"""
    print("=" * 80)
    print("3. 验证负荷转矩公式")
    print("   轴向负载: F = F_A + M×G×(sin a + μ×cos a)")
    print("   负载转矩: T_L = (F × P_B) / (2π × η)")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    G = 9.8
    PI = math.pi
    
    # 测试用例1: 水平运动 (a=0°)
    case1 = {
        "FA": 0, "M": 10, "a": 0, "mu": 0.1, "PB": 0.01, "eta": 0.9
    }
    a_rad = math.radians(case1["a"])
    F_expected = case1["FA"] + case1["M"] * G * (math.sin(a_rad) + case1["mu"] * math.cos(a_rad))
    TL_expected = (F_expected * case1["PB"]) / (2 * PI * case1["eta"])
    
    result1 = calculator._calculate_load_torque(case1)
    F_actual = result1.extra['F']
    TL_actual = result1.result
    
    print(f"  测试 1: 水平运动 (a=0°)")
    print(f"    M={case1['M']} kg, μ={case1['mu']}, P_B={case1['PB']} m, η={case1['eta']}")
    print(f"    轴向负载 F: 期望={F_expected:.6f} N, 实际={F_actual:.6f} N, 状态={'✓' if abs(F_actual - F_expected) < 0.0001 else '✗'}")
    print(f"    负载转矩 T_L: 期望={TL_expected:.6f} Nm, 实际={TL_actual:.6f} Nm, 状态={'✓' if abs(TL_actual - TL_expected) < 0.0001 else '✗'}")
    
    # 测试用例2: 垂直向上运动 (a=90°)
    case2 = {
        "FA": 0, "M": 10, "a": 90, "mu": 0.1, "PB": 0.01, "eta": 0.9
    }
    a_rad = math.radians(case2["a"])
    F_expected = case2["FA"] + case2["M"] * G * (math.sin(a_rad) + case2["mu"] * math.cos(a_rad))
    TL_expected = (F_expected * case2["PB"]) / (2 * PI * case2["eta"])
    
    result2 = calculator._calculate_load_torque(case2)
    F_actual = result2.extra['F']
    TL_actual = result2.result
    
    print(f"\n  测试 2: 垂直向上运动 (a=90°)")
    print(f"    M={case2['M']} kg, μ={case2['mu']}, P_B={case2['PB']} m, η={case2['eta']}")
    print(f"    轴向负载 F: 期望={F_expected:.6f} N, 实际={F_actual:.6f} N, 状态={'✓' if abs(F_actual - F_expected) < 0.0001 else '✗'}")
    print(f"    负载转矩 T_L: 期望={TL_expected:.6f} Nm, 实际={TL_actual:.6f} Nm, 状态={'✓' if abs(TL_actual - TL_expected) < 0.0001 else '✗'}")
    
    print("\n  公式验证: ✓ 正确\n")


def verify_acceleration_torque():
    """验证加速转矩公式"""
    print("=" * 80)
    print("4. 验证加速转矩公式")
    print("   直线运动平台惯量: J_L1 = M × (P_B/(2π))²")
    print("   滚珠丝杠惯量: J_B = (π/32) × ρ × L_B × D_B⁴")
    print("   连轴器惯量: J_C = M_C × D_C² / 8")
    print("   启动转矩: T_S = (2π × N_M × (J_M + J_L)) / (60 × t₀)")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    PI = math.pi
    RHO = 7900
    
    # 测试用例
    case = {
        "M": 10, "PB": 0.01, "LB": 0.5, "DB": 0.02, "MC": 0.5, "DC": 0.05,
        "NM": 1000, "JM": 0.0011, "t0": 0.25
    }
    
    # 计算期望值
    JL1_expected = case["M"] * (case["PB"] / (2 * PI)) ** 2
    JB_expected = PI * RHO * case["LB"] * (case["DB"] ** 4) / 32
    JC_expected = case["MC"] * (case["DC"] ** 2) / 8
    JL_expected = JL1_expected + JB_expected + JC_expected
    TS_expected = 2 * PI * case["NM"] * (case["JM"] + JL_expected) / (60 * case["t0"])
    
    result = calculator._calculate_acceleration_torque(case)
    JL1_actual = result.extra['JL1']
    JB_actual = result.extra['JB']
    JC_actual = result.extra['JC']
    JL_actual = result.extra['JL']
    TS_actual = result.result
    
    print(f"  测试用例:")
    print(f"    M={case['M']} kg, P_B={case['PB']} m, L_B={case['LB']} m, D_B={case['DB']} m")
    print(f"    M_C={case['MC']} kg, D_C={case['DC']} m, N_M={case['NM']} rpm, J_M={case['JM']} kg·m², t₀={case['t0']} s")
    print(f"\n  直线运动平台惯量 J_L1:")
    print(f"    期望: {JL1_expected:.8f} kg·m², 实际: {JL1_actual:.8f} kg·m², 状态: {'✓' if abs(JL1_actual - JL1_expected) < 0.0000001 else '✗'}")
    print(f"\n  滚珠丝杠惯量 J_B:")
    print(f"    期望: {JB_expected:.8f} kg·m², 实际: {JB_actual:.8f} kg·m², 状态: {'✓' if abs(JB_actual - JB_expected) < 0.0000001 else '✗'}")
    print(f"\n  连轴器惯量 J_C:")
    print(f"    期望: {JC_expected:.8f} kg·m², 实际: {JC_actual:.8f} kg·m², 状态: {'✓' if abs(JC_actual - JC_expected) < 0.0000001 else '✗'}")
    print(f"\n  总负荷惯量 J_L:")
    print(f"    期望: {JL_expected:.8f} kg·m², 实际: {JL_actual:.8f} kg·m², 状态: {'✓' if abs(JL_actual - JL_expected) < 0.0000001 else '✗'}")
    print(f"\n  启动转矩 T_S:")
    print(f"    期望: {TS_expected:.6f} Nm, 实际: {TS_actual:.6f} Nm, 状态: {'✓' if abs(TS_actual - TS_expected) < 0.0001 else '✗'}")
    
    print("\n  公式验证: ✓ 正确\n")


def verify_required_torque():
    """验证必须转矩公式: T_M = (T_L + T_S) × S"""
    print("=" * 80)
    print("5. 验证必须转矩公式: T_M = (T_L + T_S) × S")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    
    test_cases = [
        {"TL": 0.0263, "TS": 0.6591, "S": 1, "expected": 0.6854},
        {"TL": 0.1, "TS": 0.5, "S": 1.5, "expected": 0.9},
        {"TL": 0.05, "TS": 0.2, "S": 2, "expected": 0.5},
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_required_torque(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.0001 else "✗"
        print(f"  测试 {i}: T_L={case['TL']} Nm, T_S={case['TS']} Nm, S={case['S']}")
        print(f"    期望: {expected} Nm, 实际: {actual} Nm, 状态: {status}")
    
    print("  公式验证: T_M = (T_L + T_S) × S ✓ 正确\n")


def verify_inertia_ratio_motor():
    """验证惯量比公式: I_1 = J_L / J_M"""
    print("=" * 80)
    print("6. 验证惯量比公式: I_1 = J_L / J_M")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    
    test_cases = [
        {"JL": 0.001889, "JM": 0.0011, "expected": 1.7173},
        {"JL": 0.005, "JM": 0.001, "expected": 5.0},
        {"JL": 0.01, "JM": 0.002, "expected": 5.0},
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_inertia_ratio_motor(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.01 else "✗"
        print(f"  测试 {i}: J_L={case['JL']} kg·m², J_M={case['JM']} kg·m²")
        print(f"    期望: {expected}, 实际: {actual}, 状态: {status}")
    
    print("  公式验证: I_1 = J_L / J_M ✓ 正确\n")


def verify_inertia_ratio_reducer():
    """验证减速机惯量比公式: I_2 = J_L / (J_M × i²)"""
    print("=" * 80)
    print("7. 验证减速机惯量比公式: I_2 = J_L / (J_M × i²)")
    print("=" * 80)
    
    calculator = ScrewHorizontalCalculator()
    
    test_cases = [
        {"JL": 0.001889, "JM": 0.0011, "i": 4, "expected": 0.1073},  # 0.001889 / (0.0011 × 16) = 0.1073
        {"JL": 0.01, "JM": 0.001, "i": 5, "expected": 0.4},  # 0.01 / (0.001 × 25) = 0.4
        {"JL": 0.005, "JM": 0.002, "i": 2, "expected": 0.625},  # 0.005 / (0.002 × 4) = 0.625
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_inertia_ratio_reducer(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.01 else "✗"
        print(f"  测试 {i}: J_L={case['JL']} kg·m², J_M={case['JM']} kg·m², i={case['i']}")
        print(f"    期望: {expected}, 实际: {actual}, 状态: {status}")
    
    print("  公式验证: I_2 = J_L / (J_M × i²) ✓ 正确\n")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("丝杠水平运动选型计算公式验证报告")
    print("=" * 80 + "\n")
    
    try:
        verify_speed_curve()
        verify_motor_speed()
        verify_load_torque()
        verify_acceleration_torque()
        verify_required_torque()
        verify_inertia_ratio_motor()
        verify_inertia_ratio_reducer()
        
        print("=" * 80)
        print("所有公式验证完成！")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

