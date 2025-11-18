"""
验证伺服电机电子齿轮比计算公式的正确性
参考Excel表格：伺服电机电子齿轮比计算公式
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.electronic_gear_ratio_calculator import ElectronicGearRatioCalculator

def test_forward_calculation():
    """测试正向计算（已知负载移动距离和电机转数）"""
    print("=" * 60)
    print("测试1：正向计算（已知负载移动距离和电机转数）")
    print("=" * 60)
    
    calculator = ElectronicGearRatioCalculator()
    
    # 测试用例1：参考Excel表格
    # 编码器分辨率：10000 p/r
    # 机械减速比：1/4 = 0.25（分母4，分子1）
    # 机械部分每圈位移量：235 mm
    # 电机转数：1转
    # 负载移动距离：235 mm
    
    params = {
        "encoder_resolution": 10000,  # 编码器分辨率 (脉冲/转)
        "mechanical_ratio": 0.25,    # 机械减速比 = 1/4
        "load_distance": 235,         # 负载移动距离 (mm)
        "motor_revolutions": 1        # 电机转数 (转)
    }
    
    result = calculator.calculate(params)
    
    print(f"输入参数：")
    print(f"  编码器分辨率: {params['encoder_resolution']} p/r")
    print(f"  机械减速比: {params['mechanical_ratio']}")
    print(f"  负载移动距离: {params['load_distance']} mm")
    print(f"  电机转数: {params['motor_revolutions']} 转")
    print(f"\n计算结果：")
    print(f"  电子齿轮比: {result.result:.6f}")
    print(f"  脉冲当量: {result.extra.get('pulse_equivalent_calc', 'N/A'):.6f} mm/脉冲")
    print(f"  场景名称: {result.scenario_name}")
    
    # 验证公式：电子齿轮比 = (编码器分辨率 × 机械减速比 × 电机转数) / 负载移动距离
    expected_ratio = (10000 * 0.25 * 1) / 235
    print(f"\n验证：")
    print(f"  期望电子齿轮比: {expected_ratio:.6f}")
    print(f"  实际电子齿轮比: {result.result:.6f}")
    print(f"  误差: {abs(result.result - expected_ratio):.10f}")
    
    # 验证脉冲当量：脉冲当量 = 负载移动距离 / (编码器分辨率 × 电子齿轮比 × 机械减速比)
    expected_pulse_equiv = 235 / (10000 * result.result * 0.25)
    actual_pulse_equiv = result.extra.get('pulse_equivalent_calc', 0)
    print(f"  期望脉冲当量: {expected_pulse_equiv:.6f} mm/脉冲")
    print(f"  实际脉冲当量: {actual_pulse_equiv:.6f} mm/脉冲")
    print(f"  误差: {abs(actual_pulse_equiv - expected_pulse_equiv):.10f}")
    
    assert abs(result.result - expected_ratio) < 0.0001, "电子齿轮比计算错误"
    assert abs(actual_pulse_equiv - expected_pulse_equiv) < 0.0001, "脉冲当量计算错误"
    print("  ✓ 测试通过")
    
    # 测试用例2：Excel表格中的CMX/CDV计算方式
    # CMX = 编码器分辨率 × 脉冲当量 × 10^3 × 减速比分母 / 减速比分子
    # CDV = 机械部分每圈位移量 × 10^3
    # 电子齿轮比 = CMX / CDV
    
    print("\n" + "-" * 60)
    print("测试2：Excel表格CMX/CDV计算方式")
    print("-" * 60)
    
    # 从Excel表格：
    # 编码器分辨率：10000
    # 脉冲当量：0.01 mm/p
    # 减速比分母：4
    # 减速比分子：1
    # 机械部分每圈位移量：235 mm
    
    pulse_equivalent_excel = 0.01  # mm/p
    encoder_res = 10000
    reduction_denominator = 4
    reduction_numerator = 1
    displacement_per_rev = 235  # mm
    
    # CMX = 编码器分辨率 × 脉冲当量 × 10^3 × 减速比分母 / 减速比分子
    CMX = encoder_res * pulse_equivalent_excel * 1000 * reduction_denominator / reduction_numerator
    print(f"CMX = {encoder_res} × {pulse_equivalent_excel} × 10^3 × {reduction_denominator} / {reduction_numerator}")
    print(f"CMX = {CMX}")
    
    # CDV = 机械部分每圈位移量 × 10^3
    CDV = displacement_per_rev * 1000
    print(f"CDV = {displacement_per_rev} × 10^3")
    print(f"CDV = {CDV}")
    
    # 电子齿轮比 = CMX / CDV
    gear_ratio_excel = CMX / CDV
    print(f"电子齿轮比 = CMX / CDV = {CMX} / {CDV} = {gear_ratio_excel:.6f}")
    
    # 验证：使用反向计算
    # 根据Excel公式，反向计算需要机械部分每圈位移量
    # 机械部分每圈位移量 = 负载移动距离 / 电机转数
    # 从Excel数据：机械部分每圈位移量 = 235mm，如果电机转1圈，负载移动距离 = 235mm
    params2 = {
        "encoder_resolution": encoder_res,
        "mechanical_ratio": reduction_numerator / reduction_denominator,  # 1/4 = 0.25
        "pulse_equivalent": pulse_equivalent_excel,
        "load_distance": displacement_per_rev,  # 235mm
        "motor_revolutions": 1  # 电机转1圈
    }
    
    result2 = calculator.calculate(params2)
    print(f"\n反向计算结果：")
    print(f"  电子齿轮比: {result2.result:.6f}")
    print(f"  期望电子齿轮比（CMX/CDV）: {gear_ratio_excel:.6f}")
    print(f"  误差: {abs(result2.result - gear_ratio_excel):.10f}")
    
    assert abs(result2.result - gear_ratio_excel) < 0.0001, "反向计算电子齿轮比错误"
    print("  ✓ 测试通过")


def test_reverse_calculation():
    """测试反向计算（已知脉冲当量）"""
    print("\n" + "=" * 60)
    print("测试3：反向计算（已知脉冲当量）")
    print("=" * 60)
    
    calculator = ElectronicGearRatioCalculator()
    
    # 测试用例：Excel表格数据
    params = {
        "encoder_resolution": 10000,  # 编码器分辨率 (脉冲/转)
        "mechanical_ratio": 0.25,     # 机械减速比 = 1/4
        "pulse_equivalent": 0.01      # 脉冲当量 (mm/脉冲)
    }
    
    result = calculator.calculate(params)
    
    print(f"输入参数：")
    print(f"  编码器分辨率: {params['encoder_resolution']} p/r")
    print(f"  机械减速比: {params['mechanical_ratio']}")
    print(f"  脉冲当量: {params['pulse_equivalent']} mm/脉冲")
    print(f"\n计算结果：")
    print(f"  电子齿轮比: {result.result:.6f}")
    print(f"  场景名称: {result.scenario_name}")
    
    # 验证公式：电子齿轮比 = 编码器分辨率 / (脉冲当量 × 机械减速比)
    expected_ratio = 10000 / (0.01 * 0.25)
    print(f"\n验证：")
    print(f"  期望电子齿轮比: {expected_ratio:.6f}")
    print(f"  实际电子齿轮比: {result.result:.6f}")
    print(f"  误差: {abs(result.result - expected_ratio):.10f}")
    
    assert abs(result.result - expected_ratio) < 0.0001, "反向计算电子齿轮比错误"
    print("  ✓ 测试通过")
    
    # 测试带负载移动距离的情况
    print("\n" + "-" * 60)
    print("测试4：反向计算（已知脉冲当量 + 负载移动距离）")
    print("-" * 60)
    
    params2 = {
        "encoder_resolution": 10000,
        "mechanical_ratio": 0.25,
        "pulse_equivalent": 0.01,
        "load_distance": 235  # 如果提供，将计算电机转数
    }
    
    result2 = calculator.calculate(params2)
    
    print(f"输入参数：")
    print(f"  编码器分辨率: {params2['encoder_resolution']} p/r")
    print(f"  机械减速比: {params2['mechanical_ratio']}")
    print(f"  脉冲当量: {params2['pulse_equivalent']} mm/脉冲")
    print(f"  负载移动距离: {params2['load_distance']} mm")
    print(f"\n计算结果：")
    print(f"  电子齿轮比: {result2.result:.6f}")
    if 'motor_revolutions_calc' in result2.extra:
        print(f"  电机转数: {result2.extra['motor_revolutions_calc']:.6f} 转")
        
        # 验证电机转数计算
        # 电机转数 = 负载移动距离 / (编码器分辨率 × 电子齿轮比 × 机械减速比 × 脉冲当量)
        expected_rev = 235 / (10000 * result2.result * 0.25 * 0.01)
        print(f"  期望电机转数: {expected_rev:.6f} 转")
        print(f"  实际电机转数: {result2.extra['motor_revolutions_calc']:.6f} 转")
        print(f"  误差: {abs(result2.extra['motor_revolutions_calc'] - expected_rev):.10f}")
        
        assert abs(result2.extra['motor_revolutions_calc'] - expected_rev) < 0.0001, "电机转数计算错误"
        print("  ✓ 电机转数计算正确")


if __name__ == "__main__":
    try:
        test_forward_calculation()
        test_reverse_calculation()
        print("\n" + "=" * 60)
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


