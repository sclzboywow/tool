"""工具脚手架生成脚本。

一条命令生成配置、后端、前端和模板样板文件，方便快速搭建新工具。
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

CONFIG_TEMPLATE = """{{
  "id": "{slug}",
  "name": "{name}",
  "description": "{description}",
  "page": "/{slug}",
  "api": "/api/tools/{slug}"
}}
"""

SERVICE_TEMPLATE = '''"""
{name} 计算逻辑样板。
"""
from typing import Any, Dict


class {class_name}Calculator:
    """{description}"""

    def calculate(self, scenario: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """根据场景执行计算。"""
        _ = scenario
        _ = params
        raise NotImplementedError("请在此处实现计算逻辑")
'''

FRONTEND_TEMPLATE = '''/**
 * {name} 前端交互样板。
 */

async function submit{class_name}() {{
  const payload = {{ scenario: "default" }};

  try {{
    const response = await fetch('/api/tools/{slug}', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(payload),
    }});

    if (!response.ok) {{
      throw new Error(`请求失败: ${{response.status}}`);
    }}

    const data = await response.json();
    render{class_name}Result(data);
  }} catch (error) {{
    console.error('调用接口失败', error);
    const resultBox = document.getElementById('{slug}-result');
    if (resultBox) {{
      resultBox.style.display = 'block';
      resultBox.textContent = `请求失败: ${{error}}`;
    }}
  }}
}}

function render{class_name}Result(data) {{
  const resultBox = document.getElementById('{slug}-result');
  if (!resultBox) return;

  resultBox.style.display = 'block';
  resultBox.textContent = JSON.stringify(data, null, 2);
}}

document.addEventListener('DOMContentLoaded', () => {{
  console.info('{name} 脚手架已准备就绪');
}});
'''

HTML_TEMPLATE = '''{{% extends "base.html" %}}

{{% block title %}}{name} - 电机电力电气计算工具站{{% endblock %}}

{{% block content %}}
<div class="page-header">
    <h1>{name}</h1>
    <p class="subtitle">{description}</p>
</div>

<div class="tool-form">
    <p>该页面由 <code>scripts/create_tool.py</code> 自动生成，请根据实际计算需求补充内容。</p>
    <button class="btn btn-primary" onclick="submit{class_name}()">调用示例接口</button>
    <pre id="{slug}-result" class="result-box" style="display: none;"></pre>
</div>
{{% endblock %}}

{{% block extra_js %}}
<script src="{{{{ static_asset('js/tools/{slug}.js') }}}}"></script>
{{% endblock %}}
'''


@dataclass
class Scaffold:
    """描述单个脚手架产物。"""

    path: Path
    content: str


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="生成新工具的脚手架文件")
    parser.add_argument("--slug", required=True, help="URL 友好的工具标识，例如: servo-motor-demo")
    parser.add_argument("--name", required=True, help="工具展示名称")
    parser.add_argument("--description", required=True, help="工具描述")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="生成内容写入的根目录，默认是项目根目录",
    )
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只展示将要生成的文件，而不写入磁盘",
    )
    return parser.parse_args()


def slug_to_class_name(slug: str) -> str:
    """将 slug 转换为类名。"""
    parts = slug.replace("-", " ").replace("_", " ").split()
    return "".join(word.capitalize() for word in parts if word)


def build_scaffolds(base_dir: Path, slug: str, name: str, description: str) -> List[Scaffold]:
    """构建所有需要生成的脚手架文件列表。"""
    class_name = slug_to_class_name(slug)

    return [
        Scaffold(base_dir / "app" / "config" / f"{slug}.json", CONFIG_TEMPLATE.format(slug=slug, name=name, description=description)),
        Scaffold(
            base_dir / "app" / "services" / f"{slug}_calculator.py",
            SERVICE_TEMPLATE.format(class_name=class_name, name=name, description=description),
        ),
        Scaffold(
            base_dir / "static" / "js" / "tools" / f"{slug}.js",
            FRONTEND_TEMPLATE.format(class_name=class_name, name=name, description=description, slug=slug),
        ),
        Scaffold(
            base_dir / "templates" / "tools" / f"{slug}.html",
            HTML_TEMPLATE.format(class_name=class_name, name=name, description=description, slug=slug),
        ),
    ]


def ensure_parent(path: Path) -> None:
    """确保父级目录存在。"""
    path.parent.mkdir(parents=True, exist_ok=True)


def write_scaffolds(scaffolds: Iterable[Scaffold], *, force: bool, dry_run: bool) -> None:
    """将脚手架内容写入磁盘。"""
    for scaffold in scaffolds:
        if scaffold.path.exists() and not force:
            raise FileExistsError(f"文件已存在: {scaffold.path}. 使用 --force 覆盖")

        ensure_parent(scaffold.path)

        if dry_run:
            print(f"[DRY-RUN] 将生成: {scaffold.path}")
            continue

        scaffold.path.write_text(scaffold.content, encoding="utf-8")
        print(f"已生成: {scaffold.path}")


def main() -> None:
    args = parse_args()

    normalized_slug = args.slug.strip().lower().replace(" ", "-")
    class_name = slug_to_class_name(normalized_slug)
    if not class_name:
        raise ValueError("slug 不能为空")

    scaffolds = build_scaffolds(args.output_dir, normalized_slug, args.name.strip(), args.description.strip())
    write_scaffolds(scaffolds, force=args.force, dry_run=args.dry_run)

    summary = {
        "slug": normalized_slug,
        "name": args.name,
        "description": args.description,
        "generated": [str(item.path) for item in scaffolds],
        "dry_run": args.dry_run,
    }
    print("生成摘要:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

