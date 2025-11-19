"""Validate tool configuration YAML files and optionally generate docs."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from jinja2 import Template

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from tool_config_models import ToolConfig, dump_schema, load_tool_config

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "configs" / "tools"
SCHEMA_PATH = ROOT / "configs" / "tool_config.schema.json"
DOC_MD_PATH = ROOT / "docs" / "tool_index.md"
DOC_HTML_PATH = ROOT / "docs" / "tool_index.html"


def iter_config_files() -> List[Path]:
    return sorted(CONFIG_DIR.glob("*.yaml"))


def validate_configs() -> List[ToolConfig]:
    errors = []
    configs: List[ToolConfig] = []
    for path in iter_config_files():
        try:
            config = load_tool_config(path)
            configs.append(config)
        except Exception as exc:  # pragma: no cover - simple CLI utility
            errors.append((path, exc))
    if errors:
        for path, exc in errors:
            print(f"[ERROR] {path}: {exc}")
        raise SystemExit(1)
    return configs


def render_markdown(configs: List[ToolConfig]) -> str:
    template = Template(
        """# 工具索引

共收录 {{ configs|length }} 个工具配置。生成时间：{{ now }}。
{% for tool in configs %}
## {{ tool.title }} ({{ tool.id }})

{{ tool.summary }}

{% if tool.category %}领域：`{{ tool.category }}`

{% endif %}### 参数列表
| 参数名 | 显示名 | 类型 | 单位 | 必填 | 约束 | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
{% for param in tool.parameters %}| `{{ param.name }}` | {{ param.label }} | {{ param.type }} | {{ param.unit or '' }} | {{ '是' if param.required else '否' }} |{% if param.enum %} 枚举: {{ param.enum|join(', ') }}{% elif param.minimum or param.maximum %} 范围: {{ param.minimum or '-' }} ~ {{ param.maximum or '-' }}{% else %} - {% endif %} | {{ param.description }} |
{% endfor %}

### 计算场景
{% for scenario in tool.scenarios %}- **{{ scenario.title }}** (`{{ scenario.id }}`)
  - 描述：{{ scenario.summary }}
  - 公式：{{ scenario.formula }}
  - 输入参数：{{ scenario.parameters | join(', ') }}
{% if scenario.outputs %}  - 输出：{{ scenario.outputs | join(', ') }}
{% endif %}

{% endfor %}

{% if tool.examples %}### 示例用例
{% for example in tool.examples %}- **{{ example.title }}** (场景：`{{ example.scenario }}`)
  - 输入：{{ example.inputs | tojson }}
  - 预期：{{ example.expected | tojson if example.expected else '—' }}
{% if example.notes %}  - 备注：{{ example.notes }}{% endif %}

{% endfor %}
{% endif %}

{% if tool.physics %}### 物理公式说明
- 原理：{{ tool.physics.principle }}
{% if tool.physics.assumptions %}- 假设/适用范围：{{ tool.physics.assumptions }}
{% endif %}{% if tool.physics.references %}- 参考：{{ tool.physics.references | join('; ') }}
{% endif %}
{% endif %}
{% endfor %}
""",
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return template.render(configs=configs, now="自动生成")


def render_html(markdown_text: str) -> str:
    # Simple HTML wrapper; markdown stays preformatted for reviewers
    template = Template(
        """<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <title>工具索引</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 960px; margin: auto; padding: 2rem; background: #f7f7f7; }
    pre, code { background: #f0f0f0; padding: 0.15rem 0.35rem; border-radius: 3px; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    h1, h2, h3 { color: #333; }
  </style>
</head>
<body>
  <article>
  {{ content }}
  </article>
</body>
</html>
""",
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return template.render(content=markdown_text.replace("\n", "<br/>"))


def generate_docs(configs: List[ToolConfig]) -> None:
    markdown = render_markdown(configs)
    DOC_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_MD_PATH.write_text(markdown, encoding="utf-8")
    html = render_html(markdown)
    DOC_HTML_PATH.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate tool config YAML files")
    parser.add_argument(
        "--generate-index",
        action="store_true",
        help="Generate Markdown and HTML index files after validation",
    )
    parser.add_argument(
        "--schema-only",
        action="store_true",
        help="Only regenerate the JSON schema without validating configs",
    )
    args = parser.parse_args()

    if args.schema_only:
        SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
        dump_schema(SCHEMA_PATH)
        print(f"Schema written to {SCHEMA_PATH}")
        return

    SCHEMA_PATH.parent.mkdir(parents=True, exist_ok=True)
    dump_schema(SCHEMA_PATH)
    configs = validate_configs()
    print(f"Validated {len(configs)} config file(s).")

    if args.generate_index:
        generate_docs(configs)
        print(f"Generated docs: {DOC_MD_PATH} and {DOC_HTML_PATH}")


if __name__ == "__main__":  # pragma: no cover
    main()

