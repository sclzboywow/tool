"""
FastAPI应用主文件
Excel工具转Web在线工具站
"""
import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers.tools import build_tools_router
from app.routers.tools_api import build_tools_api_router
from app.services.registry import load_configured_tools, ToolSpec

# 创建FastAPI应用实例
app = FastAPI(
    title="电机电力电气计算工具站",
    description="Excel工具转Web在线工具站",
    version="1.0.0",
)

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
TOOLS_CONFIG_DIR = BASE_DIR / "tools"
MANIFEST_PATH = STATIC_DIR / "manifest.json"


@lru_cache(maxsize=1)
def load_asset_manifest() -> dict:
    """加载构建时生成的静态资源指纹映射。"""
    if MANIFEST_PATH.exists():
        try:
            return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def static_asset(path: str) -> str:
    """返回带指纹的静态资源路径（若存在）。"""
    manifest = load_asset_manifest()
    return f"/static/{manifest.get(path, path)}"


# 加载工具配置
TOOL_SPECS: Dict[str, ToolSpec] = load_configured_tools(TOOLS_CONFIG_DIR)

# 配置模板引擎
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))
templates.env.globals["static_asset"] = static_asset

# 配置静态文件服务
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 注册路由
app.include_router(build_tools_router(TOOL_SPECS, templates))
app.include_router(build_tools_api_router(TOOL_SPECS))


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    from app.db.database import init_db

    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页 - 显示工具列表"""
    tools_list = [
        {
            "id": spec.id,
            "name": spec.display_name,
            "description": spec.description or "",
        }
        for spec in TOOL_SPECS.values()
    ]
    return templates.TemplateResponse("index.html", {"request": request, "tools": tools_list})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
