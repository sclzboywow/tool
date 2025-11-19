"""
工具页面路由工厂
"""
from typing import Dict

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.registry import ToolSpec


def build_tools_router(tool_specs: Dict[str, ToolSpec], templates: Jinja2Templates) -> APIRouter:
    """根据注册表生成页面路由"""
    router = APIRouter(prefix="/tools", tags=["tools"])

    for spec in tool_specs.values():
        # 使用闭包捕获当前 spec 的值
        def make_page_handler(s: ToolSpec):
            async def page(request: Request):
                return templates.TemplateResponse(s.template, {"request": request, "tool": s})
            return page

        router.add_api_route(f"/{spec.id}", make_page_handler(spec), response_class=HTMLResponse)

    return router
