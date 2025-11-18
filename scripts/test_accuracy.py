#!/usr/bin/env python3
"""
准确性测试脚本 - 对比Excel和Web应用的计算结果
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.current_calculator import CurrentCalculator
import math

def test_scenarios():
    """测试各个计算场景"""
    calc = CurrentCalculator()
    
    print("=" * 60)
    print("准确性测试 - Excel vs Web应用")
    print("=" * 60)
    print()
    
    # 测试用例
    test_cases = [
        {
            "name": "纯电阻负荷",
            "scenario": "pure_resistor",
            "params": {"power": 1000, "voltage": 220},
            "expected": 1000 / 220,
            "excel_formula": "I = P / U"
        },
        {
            "name": "感性负荷",
            "scenario": "inductive",
            "params": {"power": 1000, "voltage": 220, "cos_phi": 0.85},
            "expected": 1000 / (220 * 0.85),
            "excel_formula": "I = P / (U × cosφ)"
        },
        {
            "name": "单相电动机",
            "scenario": "single_phase_motor",
            "params": {"power": 1000, "voltage": 220, "efficiency": 0.875, "cos_phi": 0.89},
            "expected": 1000 / (220 * 0.875 * 0.89),
            "excel_formula": "I = P / (U × η × cosφ)"
        },
        {
            "name": "三相电动机",
            "scenario": "three_phase_motor",
            "params": {"power": 11000, "voltage": 380, "efficiency": 0.875, "cos_phi": 0.89},
            "expected": 11000 / (math.sqrt(3) * 380 * 0.875 * 0.89),
            "excel_formula": "I = P / (√3 × U × η × cosφ)"
        },
        {
            "name": "住宅总负荷",
            "scenario": "residential",
            "params": {"total_power": 5000, "kc": 0.5, "voltage": 220, "cos_phi": 0.8},
            "expected": (0.5 * 5000) / (220 * 0.8),
            "excel_formula": "I = (Kc × PΣ) / (U × cosφ)"
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"测试 {i}: {test['name']}")
        print(f"  公式: {test['excel_formula']}")
        print(f"  参数: {test['params']}")
        
        try:
            result = calc.calculate(test['scenario'], test['params'])
            expected = test['expected']
            diff = abs(result.result - expected)
            diff_percent = (diff / expected * 100) if expected != 0 else 0
            
            print(f"  预期结果: {expected:.6f} A")
            print(f"  Web结果:  {result.result:.6f} A")
            print(f"  差异:     {diff:.6f} A ({diff_percent:.4f}%)")
            
            # 允许0.01%的误差
            if diff_percent < 0.01:
                print(f"  ✓ 通过")
            else:
                print(f"  ✗ 失败 (差异过大)")
                all_passed = False
        except Exception as e:
            print(f"  ✗ 错误: {str(e)}")
            all_passed = False
        
        print()
    
    print("=" * 60)
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = test_scenarios()
    sys.exit(0 if success else 1)

