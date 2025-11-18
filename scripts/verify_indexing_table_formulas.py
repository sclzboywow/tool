#!/usr/bin/env python3
"""
验证分度盘机构选型计算公式
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.indexing_table_calculator import IndexingTableCalculator

def test_speed_curve():
    """测试速度曲线 - 加减速时间计算"""
    print("="*80)
    print("测试1: 速度曲线 - 加减速时间计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {
        "t": 1.5,  # 定位时间 (s)
        "A": 0.5   # 加减速时间比
    }
    result = calculator.calculate("speed_curve", params)
    expected_t0 = 1.5 * 0.5  # 0.75
    print(f"输入: t={params['t']}, A={params['A']}")
    print(f"计算结果: t0 = {result.result} s")
    print(f"期望结果: t0 = {expected_t0} s")
    assert abs(result.result - expected_t0) < 0.0001, f"测试失败: 期望 {expected_t0}, 实际 {result.result}"
    print("✓ 测试通过\n")


def test_motor_speed():
    """测试电机转速计算"""
    print("="*80)
    print("测试2: 电机转速计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {
        "theta": 15,  # 定位角度 (°)
        "t": 1.5,     # 定位时间 (s)
        "t0": 0.75,   # 加减速时间 (s)
        "i": 5        # 减速比
    }
    result = calculator.calculate("motor_speed", params)
    # Excel公式验证
    # F24 = ((F11*K6)/180)/(F20*(F12-F20))
    # F24 = ((15*3.1416)/180)/(0.75*(1.5-0.75))
    # F24 = (47.124/180)/(0.75*0.75)
    # F24 = 0.2618/0.5625 = 0.4656 rad/s²
    PI_EXCEL = 3.1416
    betaG_expected = ((15 * PI_EXCEL) / 180) / (0.75 * (1.5 - 0.75))
    # F29 = (F24*F20*60)/(2*K6)
    # F29 = (0.4656*0.75*60)/(2*3.1416)
    # F29 = 20.952/6.2832 = 3.334 rpm
    N_expected = (betaG_expected * 0.75 * 60) / (2 * PI_EXCEL)
    # F32 = F24*F14 = 0.4656*5 = 2.328 rad/s²
    betaM_expected = betaG_expected * 5
    # F35 = F29*F14 = 3.334*5 = 16.67 rpm
    NM_expected = N_expected * 5
    
    print(f"输入: θ={params['theta']}°, t={params['t']}s, t0={params['t0']}s, i={params['i']}")
    print(f"计算结果: βG={result.extra['betaG']:.6f} rad/s², N={result.extra['N']:.2f} rpm")
    print(f"          βm={result.extra['betaM']:.6f} rad/s², NM={result.result:.2f} rpm")
    print(f"期望结果: βG={betaG_expected:.6f} rad/s², N={N_expected:.2f} rpm")
    print(f"          βm={betaM_expected:.6f} rad/s², NM={NM_expected:.2f} rpm")
    assert abs(result.extra['betaG'] - betaG_expected) < 0.01, f"βG测试失败"
    assert abs(result.extra['N'] - N_expected) < 0.1, f"N测试失败"
    assert abs(result.extra['betaM'] - betaM_expected) < 0.01, f"βm测试失败"
    assert abs(result.result - NM_expected) < 0.1, f"NM测试失败"
    print("✓ 测试通过\n")


def test_load_torque():
    """测试负载转矩计算"""
    print("="*80)
    print("测试3: 负载转矩计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {}
    result = calculator.calculate("load_torque", params)
    print(f"计算结果: TL = {result.result} Nm")
    assert result.result == 0.0, f"测试失败: 期望 0.0, 实际 {result.result}"
    print("✓ 测试通过\n")


def test_acceleration_torque():
    """测试加速转矩计算"""
    print("="*80)
    print("测试4: 加速转矩计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {
        "DT": 0.48,      # 分度盘直径 (m)
        "LT": 0.03,      # 分度盘厚度 (m)
        "DW": 0.04,      # 工作物直径 (m)
        "LW": 0.4,       # 工作物厚度 (m)
        "rho": 900,      # 工作台材质密度 (kg/m³)
        "n": 24,         # 工作物数量
        "l": 0.41,       # 由分度盘中心至工作物中心的距离 (m)
        "i": 5,          # 减速比
        "JM": 0.00014,   # 电机惯量 (kg·m²)
        "betaM": 2.328,  # 电机轴角加速度 (rad/s²) - 从测试2获得
        "etaG": 0.7      # 减速机效率
    }
    result = calculator.calculate("acceleration_torque", params)
    # Excel公式验证
    PI_EXCEL = 3.1416
    # F46 = (K6*F8*F5*F4^4)/32 = (3.1416*900*0.03*0.48^4)/32
    JT_expected = (PI_EXCEL * 900 * 0.03 * (0.48 ** 4)) / 32
    # F51 = (K6*F8*F7*F6^4)/32 = (3.1416*900*0.4*0.04^4)/32
    JW1_expected = (PI_EXCEL * 900 * 0.4 * (0.04 ** 4)) / 32
    # F55 = (K6*F8*F7*F6^2)/4 = (3.1416*900*0.4*0.04^2)/4
    mw_expected = (PI_EXCEL * 900 * 0.4 * (0.04 ** 2)) / 4
    # F58 = F9*(F51+F55*F10^2) = 24*(JW1_expected + mw_expected*0.41^2)
    JW_expected = 24 * (JW1_expected + mw_expected * (0.41 ** 2))
    # F61 = F46+F58
    JL_expected = JT_expected + JW_expected
    # F67 = F61/(F14^2) = JL_expected/25
    JLM_expected = JL_expected / (5 ** 2)
    # F70 = ((F67+K55)*F32)/F15 = ((JLM_expected+0.00014)*2.328)/0.7
    TS_expected = ((JLM_expected + 0.00014) * 2.328) / 0.7
    
    print(f"输入: DT={params['DT']}m, LT={params['LT']}m, DW={params['DW']}m, LW={params['LW']}m")
    print(f"      ρ={params['rho']}kg/m³, n={params['n']}, l={params['l']}m, i={params['i']}")
    print(f"      JM={params['JM']}kg·m², βm={params['betaM']}rad/s², ηG={params['etaG']}")
    print(f"计算结果: JT={result.extra['JT']:.6f} kg·m²")
    print(f"          JW1={result.extra['JW1']:.6f} kg·m²")
    print(f"          mw={result.extra['mw']:.6f} kg")
    print(f"          JW={result.extra['JW']:.6f} kg·m²")
    print(f"          JL={result.extra['JL']:.6f} kg·m²")
    print(f"          JLM={result.extra['JLM']:.6f} kg·m²")
    print(f"          TS={result.result:.6f} Nm")
    print(f"期望结果: JT={JT_expected:.6f} kg·m²")
    print(f"          JW1={JW1_expected:.6f} kg·m²")
    print(f"          mw={mw_expected:.6f} kg")
    print(f"          JW={JW_expected:.6f} kg·m²")
    print(f"          JL={JL_expected:.6f} kg·m²")
    print(f"          JLM={JLM_expected:.6f} kg·m²")
    print(f"          TS={TS_expected:.6f} Nm")
    assert abs(result.extra['JT'] - JT_expected) < 0.0001, f"JT测试失败"
    assert abs(result.extra['JW1'] - JW1_expected) < 0.0001, f"JW1测试失败"
    assert abs(result.extra['mw'] - mw_expected) < 0.0001, f"mw测试失败"
    assert abs(result.extra['JW'] - JW_expected) < 0.01, f"JW测试失败"
    assert abs(result.extra['JL'] - JL_expected) < 0.01, f"JL测试失败"
    assert abs(result.extra['JLM'] - JLM_expected) < 0.001, f"JLM测试失败"
    assert abs(result.result - TS_expected) < 0.01, f"TS测试失败"
    print("✓ 测试通过\n")


def test_required_torque():
    """测试必须转矩计算"""
    print("="*80)
    print("测试5: 必须转矩计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {
        "TS": 0.5,  # 电机轴加速转矩 (Nm)
        "TL": 0,    # 负载转矩 (Nm)
        "S": 2      # 安全系数
    }
    result = calculator.calculate("required_torque", params)
    expected_TM = (0.5 + 0) * 2  # 1.0
    print(f"输入: TS={params['TS']}Nm, TL={params['TL']}Nm, S={params['S']}")
    print(f"计算结果: T = {result.result:.6f} Nm")
    print(f"期望结果: T = {expected_TM:.6f} Nm")
    assert abs(result.result - expected_TM) < 0.0001, f"测试失败: 期望 {expected_TM}, 实际 {result.result}"
    print("✓ 测试通过\n")


def test_inertia_ratio():
    """测试惯量比计算"""
    print("="*80)
    print("测试6: 惯量比计算")
    print("="*80)
    calculator = IndexingTableCalculator()
    params = {
        "JL": 0.1,      # 全负载惯量 (kg·m²)
        "i": 5,         # 减速比
        "JM": 0.00014   # 电机惯量 (kg·m²)
    }
    result = calculator.calculate("inertia_ratio", params)
    # Excel公式: F79 = (F61/(F14^2))/K55 = (0.1/25)/0.00014 = 0.004/0.00014 = 28.57
    expected_N1 = (0.1 / (5 ** 2)) / 0.00014
    print(f"输入: JL={params['JL']}kg·m², i={params['i']}, JM={params['JM']}kg·m²")
    print(f"计算结果: N1 = {result.result:.2f}")
    print(f"期望结果: N1 = {expected_N1:.2f}")
    assert abs(result.result - expected_N1) < 0.1, f"测试失败: 期望 {expected_N1:.2f}, 实际 {result.result:.2f}"
    print("✓ 测试通过\n")


if __name__ == "__main__":
    try:
        test_speed_curve()
        test_motor_speed()
        test_load_torque()
        test_acceleration_torque()
        test_required_torque()
        test_inertia_ratio()
        print("="*80)
        print("所有测试通过！✓")
        print("="*80)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

