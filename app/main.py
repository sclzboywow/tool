"""
FastAPI应用主文件
Excel工具转Web在线工具站
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

# 创建FastAPI应用实例
app = FastAPI(
    title="电机电力电气计算工具站",
    description="Excel工具转Web在线工具站",
    version="1.0.0"
)

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置模板引擎
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 配置静态文件服务
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 导入路由
from app.routers import tools
from app.routers import tools_api

# 注册路由
app.include_router(tools.router, tags=["tools"])
app.include_router(tools_api.router, tags=["api"])


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    from app.db.database import init_db
    init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页 - 显示工具列表"""
    # 工具列表（从Excel分析得出，先列出前几个）
    tools_list = [
        {"id": "current-calc", "name": "常用电流计算公式", "description": "包含纯电阻、感性负荷、单相/三相电动机、住宅总负荷等电流计算"},
        {"id": "inertia-calc", "name": "不同形状物体惯量计算", "description": "计算不同形状物体的转动惯量"},
        {"id": "screw-horizontal", "name": "丝杠水平运动选型计算", "description": "计算丝杠水平运动系统的电机选型参数，包括必须转矩、惯量比等"},
        {"id": "screw-vertical", "name": "丝杠垂直运动选型计算", "description": "计算丝杠垂直运动系统的电机选型参数，包括必须转矩、惯量比等"},
        {"id": "belt-intermittent", "name": "皮带轮间歇运动选型计算", "description": "计算皮带轮间歇运动系统的电机选型参数，包括必须转矩、惯量比等"},
        {"id": "belt-continuous", "name": "皮带轮连续运动选型计算", "description": "计算皮带轮连续运动系统的电机选型参数，包括必须转矩、惯量比等"},
        {"id": "indexing-table", "name": "分度盘机构选型计算", "description": "计算分度盘机构的电机选型参数，包括加减速时间、电机转速、负载转矩、加速转矩、必须转矩和惯量比等"},
        {"id": "motor-startup-voltage", "name": "电动机启动时端电压计算", "description": "计算电动机启动时的端电压降，包括变压器低压母线上的三相短路容量和电动机启动电压计算"},
        {"id": "cart-drive-power", "name": "小车驱动电机功率计算", "description": "计算小车驱动系统的电机功率，包括牵引力计算、电机功率计算和功率提升版本"},
        {"id": "crawler-robot-force", "name": "履带机器人驱动力计算", "description": "计算履带机器人的驱动力、功率、扭矩等参数，包括功率计算、扭矩计算、加速扭矩计算、越障计算、原地回转计算、减速器校验和速度计算"},
        {"id": "electronic-gear-ratio", "name": "伺服电机电子齿轮比计算", "description": "计算伺服电机的电子齿轮比，包括正向计算（已知负载移动距离和电机转数）和反向计算（已知脉冲当量）两种方式"},
        {"id": "angular-acceleration", "name": "角加速度计算", "description": "根据运动要求计算最大转速和角加速度，包括加速时间、减速机输出轴角加速度、电机输出轴角加速度、转速和扭矩计算"},
        {"id": "stepper-motor-inertia", "name": "步进电机惯量计算", "description": "计算步进电机的惯量、角加速度和力矩，包括滚珠丝杠、齿条和小齿轮、旋转体、角加速度和电机力矩计算"},
        {"id": "load-torque", "name": "不同驱动机构下负载转矩计算", "description": "计算不同驱动机构下的负载转矩，包括滚珠丝杠驱动、滑轮驱动、金属线/皮带/齿轮/齿条驱动和实际测试计算方法"},
        {"id": "fan-performance", "name": "风机性能表", "description": "计算风机性能参数，包括压力、流量、内功率，并绘制流量-压力曲线和流量-效率曲线"},
        {"id": "blower-selection", "name": "鼓风机选型计算", "description": "计算高炉鼓风机选型所需的各项参数，包括风压、风量、修正系数和轴功率"},
        {"id": "fan-selection", "name": "风机选型计算", "description": "根据流量、全压等参数进行风机选型计算，计算比转数、工况密度、性能点等参数"},
        {"id": "fan-selection-example", "name": "风机选型计算举例", "description": "锅炉送风机选型计算，包括煤质分析、燃烧空气量、烟气量、送风机风量和阻力、电动机功率计算"},
        {"id": "servo-motor-inertia", "name": "伺服电机惯量计算", "description": "齿轮齿条传动的伺服电机惯量计算，包括快速移动、切削和惯量匹配计算"},
        {"id": "servo-motor-selection", "name": "伺服电机选型计算", "description": "计算直线电机和旋转电机的选型参数，包括推力、扭矩、转速、惯量等"},
        {"id": "servo-motor-params", "name": "伺服电机参数计算", "description": "基于FANUC伺服电机选型要求，计算伺服电机选型所需的各项参数，包括惯量、扭矩、转速等"},
        {"id": "servo-motor-selection-example", "name": "伺服电机选型举例", "description": "基于滚珠丝杠传动的伺服电机选型计算举例，包括惯量计算、转矩计算、转数计算和电机选型验证等完整流程"},
        # 后续可以添加更多工具
    ]
    return templates.TemplateResponse("index.html", {"request": request, "tools": tools_list})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

