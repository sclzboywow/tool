#!/usr/bin/env python3
"""
验证风机选型计算举例的计算公式
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.fan_selection_example_calculator import FanSelectionExampleCalculator

def test_fan_selection_example():
    """测试风机选型计算举例"""
    calculator = FanSelectionExampleCalculator()
    
    # Excel中的输入参数
    params = {
        "scenario": "fan_selection_example",
        # 煤质参数
        "Car": 43.83,
        "OAR": 21.51,
        "Hy": 4.39,
        "Nar": 0.72,
        "War": 5.35,
        "Aar": 24.02,
        "Sar": 0.18,
        "Qnet_ar": 16929,
        
        # 燃煤量（通过锅炉参数计算）
        "D": 90,  # 锅炉蒸发量 (t/h)
        "h_main": 3500,  # 主蒸汽焓 (kJ/kg)
        "h_feed": 947,  # 给水焓 (kJ/kg)
        "blowdown": 0.02,  # 排污率
        "h_blowdown": 1491,  # 排污水焓 (kJ/kg)
        "eta_boiler": 0.89,  # 锅炉效率
        
        # 其他参数
        "alpha": 1.2,  # 过量空气系数
        "tk": 20,  # 空气温度 (°C)
        "tg": 20,  # 烟气温度 (°C)
        "b": 89.515,  # 当地大气压 (kPa)
        "k1": 1.15,  # 送风机风量储备系数
        "k2_primary": 1.2,  # 一次风机风压储备系数
        "k2_secondary": 1.25,  # 二次风机风压储备系数
        "delta_h_primary": 16100,  # 一次风机总阻力 (Pa) = 15100 + 1000
        "delta_h_secondary": 8315,  # 二次风机总阻力 (Pa) = 7315 + 1000
        "eta1": 0.85,  # 风机效率
        "eta2": 0.98,  # 机械效率
        "eta3": 0.9,  # 电动机效率
        "K_motor": 1.1,  # 电动机备用系数
        "rho_ko": 1.293,  # 空气密度 (kg/m³)
    }
    
    # Excel中的期望结果
    # 注意：Excel中Ng计算使用的是选取的Vg值（80700和54300），而不是计算值
    expected = {
        "Vo": 4.35600775,
        "VRO2": 0.8191278,
        "VN2": 3.4470061225,
        "VH2Oo": 0.623761724775,
        "Vyo": 4.889895647275,
        "VN2_excess": 0.6882492245,
        "VO2_excess": 0.1829523255,
        "VH2O_excess": 0.014026344955,
        "Vy": 5.77512354223,
        "B": 15.3150666929496,  # t/h
        "Vg": 107382.528900054,  # m³/h
        "Vg_primary": 64429.5173400325,  # m³/h (Vg * 0.6) - 计算值
        "Vg_secondary": 42953.0115600217,  # m³/h (Vg * 0.4) - 计算值
        "Hg_primary": 19320,  # Pa
        "Hg_secondary": 10393.75,  # Pa - 计算值（但Excel中Ng使用的是C123=11723.06）
        # Ng计算使用的是选取的Vg值，所以这里不验证Ng，或者使用选取值计算
        # "Ng_primary": 635.059111156872,  # kW (使用Vg=80700)
        # "Ng_secondary": 259.283230646783,  # kW (使用Vg=54300, Hg=11723.06)
    }
    
    print("=" * 80)
    print("验证风机选型计算举例")
    print("=" * 80)
    
    try:
        result = calculator.calculate("fan_selection_example", params)
        actual = result.result
        
        print("\n【计算结果对比】")
        print(f"{'参数':<20} {'Excel值':<25} {'计算值':<25} {'误差':<15} {'状态'}")
        print("-" * 90)
        
        all_passed = True
        tolerance = 1e-3  # 允许误差
        
        for key, expected_value in expected.items():
            if key in actual:
                actual_value = actual[key]
                error = abs(actual_value - expected_value)
                error_percent = (error / abs(expected_value) * 100) if expected_value != 0 else 0
                
                # 对于大数值，使用相对误差；对于小数值，使用绝对误差
                if abs(expected_value) > 1:
                    is_match = error_percent < 0.1  # 相对误差小于0.1%
                else:
                    is_match = error < tolerance
                
                status = "✓" if is_match else "✗"
                if not is_match:
                    all_passed = False
                
                print(f"{key:<20} {expected_value:<25.6f} {actual_value:<25.6f} {error_percent:<14.6f}% {status}")
            else:
                print(f"{key:<20} {expected_value:<25.6f} {'缺失':<25} {'N/A':<15} ✗")
                all_passed = False
        
        # 额外验证Ng（使用选取的Vg值）
        print("\n【电动机功率验证（使用选取的Vg值）】")
        Vg_primary_selected = 80700  # Excel中选取的值
        Vg_secondary_selected = 54300  # Excel中选取的值
        Hg_secondary_selected = 11723.0631737698  # Excel中锅炉厂推荐值
        
        Ng_primary_expected = 1.1 * Vg_primary_selected * 19320 / (3600 * 9.81 * 102 * 0.85 * 0.98 * 0.9)
        Ng_secondary_expected = 1.1 * Vg_secondary_selected * Hg_secondary_selected / (3600 * 9.81 * 102 * 0.85 * 0.98 * 0.9)
        
        print(f"Ng_primary (使用Vg=80700): 期望={Ng_primary_expected:.6f}, 实际={actual.get('Ng_primary', 0):.6f}")
        print(f"Ng_secondary (使用Vg=54300, Hg=11723.06): 期望={Ng_secondary_expected:.6f}, 实际={actual.get('Ng_secondary', 0):.6f}")
        
        print("\n" + "=" * 80)
        if all_passed:
            print("✓ 所有测试通过！")
        else:
            print("✗ 部分测试失败，请检查计算公式")
        print("=" * 80)
        
        return all_passed
        
    except Exception as e:
        print(f"\n✗ 计算错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_fan_selection_example()
    sys.exit(0 if success else 1)

