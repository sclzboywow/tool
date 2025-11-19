"""工具代码生成器

读取配置文件，根据工具定义生成/更新：
- app/models/<tool>_schemas.py
- templates/tools/<tool>.html 的表单段落
- static/js/tools/<tool>.js 的参数校验与请求封装骨架

使用方式：
    python scripts/gen_tool_artifacts.py            # 根据配置生成/覆盖文件
    python scripts/gen_tool_artifacts.py --check    # 生成后检查是否有未提交的变更
"""
from __future__ import annotations

import argparse
import json
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config/tools.json"
MODELS_DIR = PROJECT_ROOT / "app/models"
TEMPLATES_DIR = PROJECT_ROOT / "templates/tools"
JS_DIR = PROJECT_ROOT / "static/js/tools"


@dataclass
class ToolField:
    name: str
    label: str
    type: str
    required: bool = False
    min: Optional[float] = None
    max: Optional[float] = None
    options: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolField":
        return cls(
            name=data["name"],
            label=data.get("label", data["name"]),
            type=data.get("type", "text"),
            required=data.get("required", False),
            min=data.get("min"),
            max=data.get("max"),
            options=list(data.get("options", [])),
        )


@dataclass
class ToolConfig:
    name: str
    title: str
    description: str
    endpoint: str
    scenario: str = "default"
    fields: List[ToolField] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ToolConfig":
        fields = [ToolField.from_dict(item) for item in data.get("fields", [])]
        return cls(
            name=data["name"],
            title=data.get("title", data["name"]),
            description=data.get("description", ""),
            endpoint=data["endpoint"],
            scenario=data.get("scenario", "default"),
            fields=fields,
        )


def load_configs() -> List[ToolConfig]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"找不到配置文件: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    tools = [ToolConfig.from_dict(item) for item in raw.get("tools", [])]
    return tools


def _pydantic_field(field_cfg: ToolField) -> str:
    constraints = []
    if field_cfg.min is not None:
        constraints.append(f"ge={field_cfg.min}")
    if field_cfg.max is not None:
        constraints.append(f"le={field_cfg.max}")

    description = f"\"{field_cfg.label}\""
    constraint_part = ", " + ", ".join(constraints) if constraints else ""

    if field_cfg.type == "number":
        py_type = "float"
    else:
        py_type = "str"

    return f"{field_cfg.name}: Optional[{py_type}] = Field(None{constraint_part}, description={description})"


def generate_schema(tool: ToolConfig) -> str:
    field_lines = [_pydantic_field(f) for f in tool.fields]
    fields_block = "\n".join(field_lines)
    fields_section = textwrap.indent(fields_block if fields_block else "pass", " " * 4)
    class_name = "".join(part.capitalize() for part in tool.name.split("_")) + "Request"

    raw = f'''"""
自动生成的 {tool.title} 请求模型
请勿手动编辑；如需修改请更新配置文件并重新生成。
"""
from typing import Optional
from pydantic import BaseModel, Field
from app.models.schemas import CurrentCalcResponse


class {class_name}(BaseModel):
    """{tool.title} 请求模型"""
    scenario: str = Field(default="{tool.scenario}", description="计算场景")
{fields_section}


class {class_name.replace('Request', 'Response')}(CurrentCalcResponse):
    """沿用通用响应结构，保留自定义扩展空间"""
    pass
'''
    content = textwrap.dedent(raw)
    return content


def generate_template(tool: ToolConfig) -> str:
    input_fields = []
    for field_cfg in tool.fields:
        if field_cfg.type == "select":
            options = "\n".join(
                [f"                <option value=\"{opt}\">{opt}</option>" for opt in field_cfg.options]
            )
            control = textwrap.dedent(
                f"""
                <select id=\"{tool.name}-{field_cfg.name}\" name=\"{field_cfg.name}\" required={'"true"' if field_cfg.required else '"false"'}>
{options}
                </select>
                """
            ).strip()
        else:
            number_attrs = []
            if field_cfg.min is not None:
                number_attrs.append(f"min=\"{field_cfg.min}\"")
            if field_cfg.max is not None:
                number_attrs.append(f"max=\"{field_cfg.max}\"")
            attrs = " ".join(number_attrs)
            control = (
                f"<input type=\"{ 'number' if field_cfg.type == 'number' else 'text'}\" "
                f"id=\"{tool.name}-{field_cfg.name}\" name=\"{field_cfg.name}\" {attrs} "
                f"placeholder=\"请输入{field_cfg.label}\" {'required' if field_cfg.required else ''}>"
            ).strip()

        input_fields.append(
            textwrap.dedent(
                f"""
                <div class=\"form-group\">
                    <label for=\"{tool.name}-{field_cfg.name}\">{field_cfg.label}</label>
                    {control}
                </div>
                """
            ).strip()
        )

    form_body = "\n".join(input_fields)

    return f"""\
{{% extends "base.html" %}}

{{% block title %}}{tool.title} - 电机电力电气计算工具站{{% endblock %}}

{{% block content %}}
<div class=\"page-header\">
    <h1>{tool.title}</h1>
    <p class=\"subtitle\">{tool.description}</p>
</div>

<div class=\"form-card\">
    <form id=\"{tool.name}-form\">
{form_body}
        <div class=\"form-actions\">
            <button type=\"submit\" class=\"btn-primary\">开始计算</button>
            <button type=\"reset\" class=\"btn-secondary\">重置</button>
        </div>
    </form>
</div>

<div id=\"{tool.name}-result\" class=\"result-card\" style=\"display:none;\">
    <h3>计算结果</h3>
    <div class=\"result-content\"></div>
</div>
{{% endblock %}}

{{% block extra_js %}}
<script src=\"{{{{ static_asset('js/common.js') }}}}\"></script>
<script src=\"{{{{ static_asset('js/tools/{tool.name}.js') }}}}\"></script>
{{% endblock %}}
"""


def generate_js(tool: ToolConfig) -> str:
    field_defs = []
    for field_cfg in tool.fields:
        field_defs.append(
            {
                "name": field_cfg.name,
                "label": field_cfg.label,
                "type": field_cfg.type,
                "required": field_cfg.required,
                "min": field_cfg.min,
                "max": field_cfg.max,
            }
        )
    fields_json = json.dumps(field_defs, ensure_ascii=False, indent=4)

    return f"""\
// 自动生成的 {tool.title} 前端交互骨架
// 更新请修改 config/tools.json 并重新运行生成脚本

const {tool.name}Fields = {fields_json};
const {tool.name}Endpoint = "{tool.endpoint}";
const {tool.name}Form = document.getElementById("{tool.name}-form");
const {tool.name}Result = document.getElementById("{tool.name}-result");
const {tool.name}ResultContent = document.querySelector("#{tool.name}-result .result-content");

if ({tool.name}Form) {{
    {tool.name}Form.addEventListener("submit", async (event) => {{
        event.preventDefault();
        const payload = collectFormData({tool.name}Form);
        const validation = validateFields({tool.name}Fields, payload);
        if (!validation.valid) {{
            showError(validation.message);
            return;
        }}

        try {{
            const response = await apiRequest({tool.name}Endpoint, "POST", payload);
            renderResult({tool.name}Result, {tool.name}ResultContent, response);
        }} catch (error) {{
            showError(error.message || "请求失败");
        }}
    }});
}}
"""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def generate_files(tools: List[ToolConfig]) -> None:
    for tool in tools:
        schema_path = MODELS_DIR / f"{tool.name}_schemas.py"
        template_path = TEMPLATES_DIR / f"{tool.name}.html"
        js_path = JS_DIR / f"{tool.name}.js"

        write_file(schema_path, generate_schema(tool))
        write_file(template_path, generate_template(tool))
        write_file(js_path, generate_js(tool))


def run_check() -> int:
    """运行生成并检测是否有未提交变更。"""
    tools = load_configs()
    generate_files(tools)
    result = subprocess.run(["git", "diff", "--quiet"], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("检测到未提交的差异，请提交生成后的文件。", file=sys.stderr)
        return 1
    print("生成成功，仓库状态干净。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="根据工具配置生成代码骨架")
    parser.add_argument("--check", action="store_true", help="生成后校验仓库是否干净")
    args = parser.parse_args()

    tools = load_configs()
    generate_files(tools)

    if args.check:
        return run_check()

    print(f"已生成 {len(tools)} 个工具的代码骨架。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

