"""
验证伺服电机选型举例计算公式的正确性
参考Excel表格：伺服电机选型举例
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.servo_motor_selection_example_calculator import ServoMotorSelectionExampleCalculator

def test_complete_calculation():
    """测试完整计算流程"""
    print("=" * 60)
    print("测试：完整计算流程")
    print("=" * 60)
    
    calculator = ServoMotorSelectionExampleCalculator()
    
    # Excel表格中的测试数据
    params = {
        "M": 10,          # 负载质量 (kg)
        "P": 5,           # 滚珠丝杠节距 (mm)
        "D": 10,          # 滚珠丝杠直径 (mm)
        "MB": 1,          # 滚珠丝杠质量 (kg)
        "mu": 0.1,        # 滚珠丝杠摩擦系数
        "G": 1,           # 减速比（无减速器时为1）
        "eta": 1,         # 效率（无减速器时为1）
        "V": 200,         # 负载移动速度 (mm/s)
        "L": 400,         # 行程 (mm)
        "tS": 1.4,        # 行程时间 (s)
        "tA": 0.2,        # 加减速时间 (s)
        "AP": 0.01,       # 定位精度 (mm)
        "JM": 1.23e-05,   # 电机转子惯量 (kg·m²)
        "TM": 0.637,      # 电机额定转矩 (N·m)
        "Tmax_motor": 1.91,  # 电机瞬时最大转矩 (N·m)
        "Nmax_motor": 3000   # 电机额定转数 (r/min)
    }
    
    result = calculator.calculate(params)
    
    print(f"输入参数：")
    print(f"  负载质量 M: {params['M']} kg")
    print(f"  滚珠丝杠节距 P: {params['P']} mm")
    print(f"  滚珠丝杠直径 D: {params['D']} mm")
    print(f"  滚珠丝杠质量 MB: {params['MB']} kg")
    print(f"  摩擦系数 μ: {params['mu']}")
    print(f"  减速比 G: {params['G']}")
    print(f"  效率 η: {params['eta']}")
    print(f"  负载移动速度 V: {params['V']} mm/s")
    print(f"  行程 L: {params['L']} mm")
    print(f"  行程时间 tS: {params['tS']} s")
    print(f"  加减速时间 tA: {params['tA']} s")
    print(f"  定位精度 AP: {params['AP']} mm")
    print()
    
    print(f"计算结果：")
    print(f"  有效转矩 Trms: {result.result:.6f} {result.unit}")
    print(f"  场景名称: {result.scenario_name}")
    print()
    
    # 验证中间结果
    extra = result.extra
    print(f"中间结果：")
    print(f"  滚珠丝杠惯量 JB: {extra.get('JB', 0):.8e} kg·m²")
    print(f"  负载惯量 JW: {extra.get('JW', 0):.8e} kg·m²")
    print(f"  换算到电机轴负载惯量 JL: {extra.get('JL', 0):.8e} kg·m²")
    print(f"  摩擦力转矩 Tw: {extra.get('Tw', 0):.6f} N·m")
    print(f"  换算到电机轴负载转矩 TL: {extra.get('TL', 0):.6f} N·m")
    print(f"  转数 N: {extra.get('N', 0):.2f} r/min")
    print(f"  加减速转矩 TA: {extra.get('TA', 0):.6f} N·m")
    print(f"  瞬时最大转矩 T1: {extra.get('T1', 0):.6f} N·m")
    print(f"  瞬时最大转矩 T2: {extra.get('T2', 0):.6f} N·m")
    print(f"  瞬时最大转矩 T3: {extra.get('T3', 0):.6f} N·m")
    print()
    
    # Excel期望值
    expected_JB = 1.25e-05
    expected_JW = 1.88389995537344e-05
    expected_JL = 1.88389995537344e-05
    expected_Tw = 0.0156050955414013
    expected_TL = 0.0156050955414013
    expected_N = 2400
    expected_TA = 0.0391105834394904
    expected_T1 = 0.0547156789808917
    expected_T2 = 0.0156050955414013
    expected_T3 = -0.0235054878980892
    expected_Trms = 0.0301884681176466
    
    print(f"验证：")
    print(f"  滚珠丝杠惯量 JB: 期望={expected_JB:.8e}, 实际={extra.get('JB', 0):.8e}, 误差={abs(extra.get('JB', 0) - expected_JB):.10e}")
    print(f"  负载惯量 JW: 期望={expected_JW:.8e}, 实际={extra.get('JW', 0):.8e}, 误差={abs(extra.get('JW', 0) - expected_JW):.10e}")
    print(f"  换算到电机轴负载惯量 JL: 期望={expected_JL:.8e}, 实际={extra.get('JL', 0):.8e}, 误差={abs(extra.get('JL', 0) - expected_JL):.10e}")
    print(f"  摩擦力转矩 Tw: 期望={expected_Tw:.6f}, 实际={extra.get('Tw', 0):.6f}, 误差={abs(extra.get('Tw', 0) - expected_Tw):.10f}")
    print(f"  换算到电机轴负载转矩 TL: 期望={expected_TL:.6f}, 实际={extra.get('TL', 0):.6f}, 误差={abs(extra.get('TL', 0) - expected_TL):.10f}")
    print(f"  转数 N: 期望={expected_N:.2f}, 实际={extra.get('N', 0):.2f}, 误差={abs(extra.get('N', 0) - expected_N):.10f}")
    print(f"  加减速转矩 TA: 期望={expected_TA:.6f}, 实际={extra.get('TA', 0):.6f}, 误差={abs(extra.get('TA', 0) - expected_TA):.10f}")
    print(f"  瞬时最大转矩 T1: 期望={expected_T1:.6f}, 实际={extra.get('T1', 0):.6f}, 误差={abs(extra.get('T1', 0) - expected_T1):.10f}")
    print(f"  瞬时最大转矩 T2: 期望={expected_T2:.6f}, 实际={extra.get('T2', 0):.6f}, 误差={abs(extra.get('T2', 0) - expected_T2):.10f}")
    print(f"  瞬时最大转矩 T3: 期望={expected_T3:.6f}, 实际={extra.get('T3', 0):.6f}, 误差={abs(extra.get('T3', 0) - expected_T3):.10f}")
    print(f"  有效转矩 Trms: 期望={expected_Trms:.6f}, 实际={result.result:.6f}, 误差={abs(result.result - expected_Trms):.10f}")
    print()
    
    # 验证（允许小的浮点误差）
    tolerance = 0.0001
    errors = [
        abs(extra.get('JB', 0) - expected_JB),
        abs(extra.get('JW', 0) - expected_JW),
        abs(extra.get('JL', 0) - expected_JL),
        abs(extra.get('Tw', 0) - expected_Tw),
        abs(extra.get('TL', 0) - expected_TL),
        abs(extra.get('N', 0) - expected_N),
        abs(extra.get('TA', 0) - expected_TA),
        abs(extra.get('T1', 0) - expected_T1),
        abs(extra.get('T2', 0) - expected_T2),
        abs(extra.get('T3', 0) - expected_T3),
        abs(result.result - expected_Trms)
    ]
    
    max_error = max(errors)
    if max_error < tolerance:
        print(f"✓ 所有测试通过！最大误差: {max_error:.10f}")
        return True
    else:
        print(f"✗ 测试失败！最大误差: {max_error:.10f}，超过容差 {tolerance}")
        return False


if __name__ == "__main__":
    try:
        success = test_complete_calculation()
        print("\n" + "=" * 60)
        if success:
            print("所有测试通过！✓")
        else:
            print("测试失败！✗")
        print("=" * 60)
        sys.exit(0 if success else 1)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

