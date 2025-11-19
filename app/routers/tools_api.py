"""
工具API接口路由工厂
"""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.schemas import CurrentCalcResponse
from app.services.registry import ToolSpec


def _build_handler(spec: ToolSpec, request_model: BaseModel):
    async def handler(payload: request_model):  # type: ignore[valid-type]
        calculator = spec.create_calculator()
        params: Dict[str, Any] = payload.dict(exclude_none=True)
        scenario = params.pop("scenario", None)
        
        # 检查计算器的 calculate 方法签名
        import inspect
        sig = inspect.signature(calculator.calculate)
        param_count = len(sig.parameters)
        
        try:
            if param_count == 1:
                # 只需要 params，不需要 scenario（如 electronic-gear-ratio）
                return calculator.calculate(params)
            elif param_count == 2:
                # 需要 scenario 和 params
                if not scenario:
                    raise HTTPException(status_code=400, detail="缺少scenario字段")
                return calculator.calculate(scenario, params)
            else:
                raise HTTPException(status_code=500, detail=f"不支持的 calculate 方法签名: {param_count} 个参数")
        except HTTPException:
            raise
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # pragma: no cover - 防御性兜底
            raise HTTPException(status_code=500, detail=f"计算错误: {exc}") from exc

    return handler


def build_tools_api_router(tool_specs: Dict[str, ToolSpec]) -> APIRouter:
    """根据注册表生成API路由"""
    router = APIRouter(prefix="/api/tools", tags=["api"])

    for spec in tool_specs.values():
        request_model = spec.build_request_model()
        endpoint = _build_handler(spec, request_model)
        router.add_api_route(
            f"/{spec.id}/calculate",
            endpoint,
            methods=["POST"],
            response_model=CurrentCalcResponse,
        )

    return router
