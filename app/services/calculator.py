"""计算器注册表和统一入口。"""
import logging
from typing import Any, Dict, Type

from app.models.schemas import CurrentCalcResponse
from app.services.angular_acceleration_calculator import AngularAccelerationCalculator
from app.services.base_calculator import BaseCalculator
from app.services.belt_continuous_calculator import BeltContinuousCalculator
from app.services.belt_intermittent_calculator import BeltIntermittentCalculator
from app.services.blower_selection_calculator import BlowerSelectionCalculator
from app.services.cart_drive_power_calculator import CartDrivePowerCalculator
from app.services.crawler_robot_force_calculator import CrawlerRobotForceCalculator
from app.services.current_calculator import CurrentCalculator
from app.services.electronic_gear_ratio_calculator import ElectronicGearRatioCalculator
from app.services.fan_performance_calculator import FanPerformanceCalculator
from app.services.fan_selection_calculator import FanSelectionCalculator
from app.services.fan_selection_example_calculator import FanSelectionExampleCalculator
from app.services.indexing_table_calculator import IndexingTableCalculator
from app.services.inertia_calculator import InertiaCalculator
from app.services.load_torque_calculator import LoadTorqueCalculator
from app.services.motor_startup_voltage_calculator import MotorStartupVoltageCalculator
from app.services.screw_horizontal_calculator import ScrewHorizontalCalculator
from app.services.screw_vertical_calculator import ScrewVerticalCalculator
from app.services.servo_motor_inertia_calculator import ServoMotorInertiaCalculator
from app.services.servo_motor_params_calculator import ServoMotorParamsCalculator
from app.services.servo_motor_selection_calculator import ServoMotorSelectionCalculator
from app.services.servo_motor_selection_example_calculator import (
    ServoMotorSelectionExampleCalculator,
)
from app.services.stepper_motor_inertia_calculator import StepperMotorInertiaCalculator

CalculatorType = Type[Any]


CALCULATOR_REGISTRY: Dict[str, CalculatorType] = {
    "current": CurrentCalculator,
    "inertia": InertiaCalculator,
    "screw_horizontal": ScrewHorizontalCalculator,
    "screw_vertical": ScrewVerticalCalculator,
    "belt_intermittent": BeltIntermittentCalculator,
    "belt_continuous": BeltContinuousCalculator,
    "indexing_table": IndexingTableCalculator,
    "motor_startup_voltage": MotorStartupVoltageCalculator,
    "cart_drive_power": CartDrivePowerCalculator,
    "crawler_robot_force": CrawlerRobotForceCalculator,
    "electronic_gear_ratio": ElectronicGearRatioCalculator,
    "angular_acceleration": AngularAccelerationCalculator,
    "stepper_motor_inertia": StepperMotorInertiaCalculator,
    "load_torque": LoadTorqueCalculator,
    "fan_performance": FanPerformanceCalculator,
    "blower_selection": BlowerSelectionCalculator,
    "fan_selection": FanSelectionCalculator,
    "fan_selection_example": FanSelectionExampleCalculator,
    "servo_motor_inertia": ServoMotorInertiaCalculator,
    "servo_motor_selection": ServoMotorSelectionCalculator,
    "servo_motor_params": ServoMotorParamsCalculator,
    "servo_motor_selection_example": ServoMotorSelectionExampleCalculator,
}


SCENARIO_TO_TOOL: Dict[str, str] = {}
for tool_name, calculator_cls in CALCULATOR_REGISTRY.items():
    scenario_names = getattr(calculator_cls, "SCENARIO_NAMES", {})
    for scenario in scenario_names:
        SCENARIO_TO_TOOL[scenario] = tool_name


logger = logging.getLogger(__name__)


def get_calculator(tool: str | None = None, scenario: str | None = None) -> Any:
    """根据工具名或场景名获取对应的计算器实例。"""

    if tool and tool in CALCULATOR_REGISTRY:
        calculator_cls = CALCULATOR_REGISTRY[tool]
    elif scenario and scenario in SCENARIO_TO_TOOL:
        calculator_cls = CALCULATOR_REGISTRY[SCENARIO_TO_TOOL[scenario]]
    else:
        raise ValueError(f"未知的计算器或场景: tool={tool}, scenario={scenario}")

    logger.debug("选择计算器: %s", calculator_cls.__name__)
    return calculator_cls()


def calculate(tool: str, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
    """统一计算入口，带有日志和校验钩子。"""

    calculator = get_calculator(tool, scenario)
    runner = BaseCalculator(calculator)
    return runner.calculate(scenario, params)


__all__ = ["calculate", "get_calculator", "CALCULATOR_REGISTRY", "SCENARIO_TO_TOOL"]
