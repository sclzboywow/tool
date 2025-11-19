"""
Pydantic models and helpers for tool configuration YAML files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, root_validator, validator


ParameterType = Literal["number", "integer", "string", "boolean", "enum"]


class ParameterSpec(BaseModel):
    """Define a single input parameter for a tool."""

    name: str = Field(..., description="Unique parameter key used by calculators and APIs")
    label: str = Field(..., description="Human readable display name")
    description: str = Field(..., description="Short explanation of the parameter")
    type: ParameterType = Field(..., description="Data type used for validation and UI rendering")
    unit: Optional[str] = Field(None, description="Measurement unit (if applicable)")
    required: bool = Field(True, description="Whether the parameter must be provided")
    minimum: Optional[float] = Field(None, description="Minimum accepted value for numeric parameters")
    maximum: Optional[float] = Field(None, description="Maximum accepted value for numeric parameters")
    enum: Optional[List[str]] = Field(None, description="Allowed values when type is 'enum'")

    @validator("enum", always=True)
    def ensure_enum_for_enum_type(cls, value: Optional[List[str]], values: Dict[str, object]) -> Optional[List[str]]:
        if values.get("type") == "enum" and not value:
            raise ValueError("enum values must be provided when type is 'enum'")
        return value

    @validator("minimum", "maximum")
    def numeric_bounds_only_for_number(cls, value: Optional[float], values: Dict[str, object]) -> Optional[float]:
        if value is not None and values.get("type") not in {"number", "integer"}:
            raise ValueError("minimum/maximum are only valid for numeric parameter types")
        return value


class ScenarioSpec(BaseModel):
    """Describe a calculation scenario."""

    id: str = Field(..., description="Scenario identifier used by the API")
    title: str = Field(..., description="Display title")
    summary: str = Field(..., description="Short description of what is being calculated")
    formula: str = Field(..., description="Key physical equation or derivation notes")
    parameters: List[str] = Field(..., description="Parameters required for this scenario")
    outputs: Optional[List[str]] = Field(None, description="Names of expected outputs (for documentation only)")


class ExampleCase(BaseModel):
    """Concrete example for a scenario."""

    title: str
    scenario: str = Field(..., description="Scenario identifier this example belongs to")
    inputs: Dict[str, object] = Field(..., description="Input parameter values")
    expected: Optional[Dict[str, object]] = Field(None, description="Expected outputs or remarks")
    notes: Optional[str] = Field(None, description="Any additional commentary")


class PhysicsNote(BaseModel):
    """Physics background or reference for the tool."""

    principle: str = Field(..., description="Core physics principle")
    assumptions: Optional[str] = Field(None, description="Assumptions or applicable range")
    references: Optional[List[str]] = Field(None, description="Reference documents or standards")


class ToolConfig(BaseModel):
    """Structured metadata for each tool configuration file."""

    schema_version: str = Field("1.0", description="Schema version for compatibility checks")
    id: str = Field(..., description="Unique tool identifier, typically matching route/calculator name")
    title: str = Field(..., description="Display title for the tool")
    summary: str = Field(..., description="One sentence description")
    category: Optional[str] = Field(None, description="Logical grouping or domain")
    parameters: List[ParameterSpec]
    scenarios: List[ScenarioSpec]
    examples: Optional[List[ExampleCase]] = None
    physics: Optional[PhysicsNote] = None

    @root_validator(skip_on_failure=True)
    def validate_references(cls, values: Dict[str, object]) -> Dict[str, object]:
        parameters: List[ParameterSpec] = values.get("parameters") or []
        scenarios: List[ScenarioSpec] = values.get("scenarios") or []
        examples: List[ExampleCase] = values.get("examples") or []

        parameter_names = {param.name for param in parameters}
        duplicate_names = len(parameter_names) != len(parameters)
        if duplicate_names:
            raise ValueError("parameter names must be unique")

        for scenario in scenarios:
            missing = set(scenario.parameters) - parameter_names
            if missing:
                raise ValueError(f"scenario '{scenario.id}' references undefined parameters: {sorted(missing)}")

        for example in examples:
            if example.scenario not in {scenario.id for scenario in scenarios}:
                raise ValueError(f"example '{example.title}' references unknown scenario '{example.scenario}'")
            extra_inputs = set(example.inputs) - parameter_names
            if extra_inputs:
                raise ValueError(
                    f"example '{example.title}' supplies parameters not defined globally: {sorted(extra_inputs)}"
                )

        return values


def load_tool_config(path: Path) -> ToolConfig:
    """Load a YAML config file into a ToolConfig instance."""
    import yaml

    with path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return ToolConfig.parse_obj(raw)


def dump_schema(path: Path) -> None:
    """Write the JSON schema for ToolConfig to disk."""
    import json

    schema = ToolConfig.schema()
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

