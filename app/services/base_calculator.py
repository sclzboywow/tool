"""基础计算器基类，提供校验和日志钩子。"""
import logging
from typing import Any, Dict, Protocol

from app.models.schemas import CurrentCalcResponse


class SupportsCalculate(Protocol):
    """最小计算协议。"""

    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:  # pragma: no cover - 协议定义
        ...


class BaseCalculator:
    """为计算器调用提供统一的校验和日志钩子。"""

    def __init__(self, delegate: SupportsCalculate):
        self.delegate = delegate
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate(self, scenario: str, params: Dict[str, Any]) -> None:
        """基础参数校验，可在子类中扩展。"""

        if not scenario:
            raise ValueError("计算场景不能为空")
        if not isinstance(params, dict):
            raise ValueError("计算参数必须是字典类型")

    def before_calculate(self, scenario: str, params: Dict[str, Any]) -> None:
        """计算前日志钩子。"""

        self.logger.info("开始计算: scenario=%s, params=%s", scenario, params)

    def after_calculate(
        self, scenario: str, params: Dict[str, Any], response: CurrentCalcResponse
    ) -> None:
        """计算后日志钩子。"""

        self.logger.info(
            "计算完成: scenario=%s, result=%s %s",
            scenario,
            response.result,
            getattr(response, "unit", ""),
        )

    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """带有基础校验和日志的统一计算入口。"""

        self.validate(scenario, params)
        self.before_calculate(scenario, params)
        response = self.delegate.calculate(scenario, params)
        self.after_calculate(scenario, params, response)
        return response

