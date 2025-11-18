"""
Pydantic数据模型
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Union, List


class CurrentCalcResponse(BaseModel):
    """电流计算响应模型"""
    result: Union[float, List[Dict[str, Any]], Dict[str, Any]] = Field(..., description="计算结果（可以是单个数值、列表或字典）")
    unit: str = Field(default="A", description="单位")
    formula: str = Field(..., description="使用的公式")
    scenario_name: str = Field(..., description="场景名称")
    mass: Optional[float] = Field(None, description="质量(kg)，仅惯量计算时返回")
    extra: Optional[Dict[str, Any]] = Field(None, description="额外计算结果")
    
    class Config:
        extra = "allow"  # 允许额外字段

