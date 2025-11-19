from __future__ import annotations

"""
工具注册表定义与配置加载
"""
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type

import yaml
from pydantic import BaseModel, Field, ValidationError, create_model


class ToolSpec(BaseModel):
    """工具规格说明"""

    id: str = Field(..., description="工具唯一标识，用于路由")
    display_name: str = Field(..., description="展示名称")
    description: Optional[str] = Field(None, description="工具描述")
    scenarios: List[str] = Field(default_factory=list, description="支持的计算场景")
    parameter_schema: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="参数schema定义，用于生成请求模型"
    )
    calculator: str = Field(..., description="计算器类的导入路径，例如 app.services.xxx.ClassName")
    template: str = Field(..., description="模板相对路径，例如 tools/example.html")
    static_dir: Optional[str] = Field(None, description="静态资源目录")

    def get_calculator_class(self) -> Type[Any]:
        """根据配置的导入路径获取计算器类"""
        module_path, class_name = self.calculator.rsplit(".", 1)
        module = import_module(module_path)
        return getattr(module, class_name)

    def create_calculator(self) -> Any:
        """实例化计算器"""
        return self.get_calculator_class()()

    def build_request_model(self) -> Type[BaseModel]:
        """根据参数schema动态生成请求模型"""
        field_definitions: Dict[str, Any] = {"scenario": (str, ...)}
        type_mapping = {"float": float, "int": int, "str": str, "bool": bool}
        for name, spec in self.parameter_schema.items():
            raw_type = spec.get("type", "str")
            python_type = type_mapping.get(raw_type, str)
            default = spec.get("default", None)
            field_definitions[name] = (Optional[python_type], default)

        config = type("Config", (), {"extra": "allow"})
        model = create_model(
            f"{self.id.replace('-', '_').title()}Request", __config__=config, **field_definitions
        )
        return model


class ToolConfig(BaseModel):
    """整体配置模型"""

    tools: List[ToolSpec]


def load_tool_specs(config_dir: Path) -> Dict[str, ToolSpec]:
    """从目录加载所有工具配置"""
    specs: Dict[str, ToolSpec] = {}
    yaml_files = sorted(config_dir.glob("*.yml")) + sorted(config_dir.glob("*.yaml"))

    for file_path in yaml_files:
        with file_path.open("r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        try:
            tool_spec = ToolSpec(**raw)
        except ValidationError as exc:
            raise ValueError(f"配置文件 {file_path.name} 校验失败: {exc}") from exc

        specs[tool_spec.id] = tool_spec

    return specs


def load_configured_tools(config_dir: Path) -> Dict[str, ToolSpec]:
    """兼容入口：确保目录存在并加载配置"""
    if not config_dir.exists():
        raise FileNotFoundError(f"工具配置目录不存在: {config_dir}")
    return load_tool_specs(config_dir)

