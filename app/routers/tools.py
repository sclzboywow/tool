"""
工具相关路由
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(prefix="/tools", tags=["tools"])

# 获取模板目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/current-calc", response_class=HTMLResponse)
async def current_calc_page(request: Request):
    """常用电流计算公式页面"""
    return templates.TemplateResponse("tools/current_calc.html", {"request": request})


@router.get("/inertia-calc", response_class=HTMLResponse)
async def inertia_calc_page(request: Request):
    """不同形状物体惯量计算页面"""
    return templates.TemplateResponse("tools/inertia_calc.html", {"request": request})


@router.get("/screw-horizontal", response_class=HTMLResponse)
async def screw_horizontal_page(request: Request):
    """丝杠水平运动选型计算页面"""
    return templates.TemplateResponse("tools/screw_horizontal.html", {"request": request})


@router.get("/screw-vertical", response_class=HTMLResponse)
async def screw_vertical_page(request: Request):
    """丝杠垂直运动选型计算页面"""
    return templates.TemplateResponse("tools/screw_vertical.html", {"request": request})


@router.get("/belt-intermittent", response_class=HTMLResponse)
async def belt_intermittent_page(request: Request):
    """皮带轮间歇运动选型计算页面"""
    return templates.TemplateResponse("tools/belt_intermittent.html", {"request": request})


@router.get("/belt-continuous", response_class=HTMLResponse)
async def belt_continuous_page(request: Request):
    """皮带轮连续运动选型计算页面"""
    return templates.TemplateResponse("tools/belt_continuous.html", {"request": request})


@router.get("/indexing-table", response_class=HTMLResponse)
async def indexing_table_page(request: Request):
    """分度盘机构选型计算页面"""
    return templates.TemplateResponse("tools/indexing_table.html", {"request": request})


@router.get("/motor-startup-voltage", response_class=HTMLResponse)
async def motor_startup_voltage_page(request: Request):
    """电动机启动时端电压计算页面"""
    return templates.TemplateResponse("tools/motor_startup_voltage.html", {"request": request})


@router.get("/cart-drive-power", response_class=HTMLResponse)
async def cart_drive_power_page(request: Request):
    """小车驱动电机功率计算页面"""
    return templates.TemplateResponse("tools/cart_drive_power.html", {"request": request})


@router.get("/crawler-robot-force", response_class=HTMLResponse)
async def crawler_robot_force_page(request: Request):
    """履带机器人驱动力计算页面"""
    return templates.TemplateResponse("tools/crawler_robot_force.html", {"request": request})


@router.get("/electronic-gear-ratio", response_class=HTMLResponse)
async def electronic_gear_ratio_page(request: Request):
    """伺服电机电子齿轮比计算页面"""
    return templates.TemplateResponse("tools/electronic_gear_ratio.html", {"request": request})


@router.get("/angular-acceleration", response_class=HTMLResponse)
async def angular_acceleration_page(request: Request):
    """角加速度计算页面"""
    return templates.TemplateResponse("tools/angular_acceleration.html", {"request": request})


@router.get("/stepper-motor-inertia", response_class=HTMLResponse)
async def stepper_motor_inertia_page(request: Request):
    """步进电机惯量计算页面"""
    return templates.TemplateResponse("tools/stepper_motor_inertia.html", {"request": request})


@router.get("/load-torque", response_class=HTMLResponse)
async def load_torque_page(request: Request):
    """不同驱动机构下负载转矩计算页面"""
    return templates.TemplateResponse("tools/load_torque.html", {"request": request})


@router.get("/fan-performance", response_class=HTMLResponse)
async def fan_performance_page(request: Request):
    """风机性能表计算页面"""
    return templates.TemplateResponse("tools/fan_performance.html", {"request": request})


@router.get("/blower-selection", response_class=HTMLResponse)
async def blower_selection_page(request: Request):
    """鼓风机选型计算页面"""
    return templates.TemplateResponse("tools/blower_selection.html", {"request": request})


@router.get("/fan-selection", response_class=HTMLResponse)
async def fan_selection_page(request: Request):
    """风机选型计算页面"""
    return templates.TemplateResponse("tools/fan_selection.html", {"request": request})


@router.get("/fan-selection-example", response_class=HTMLResponse)
async def fan_selection_example_page(request: Request):
    """风机选型计算举例页面"""
    return templates.TemplateResponse("tools/fan_selection_example.html", {"request": request})


@router.get("/servo-motor-inertia", response_class=HTMLResponse)
async def servo_motor_inertia_page(request: Request):
    """伺服电机惯量计算页面"""
    return templates.TemplateResponse("tools/servo_motor_inertia.html", {"request": request})


@router.get("/servo-motor-selection", response_class=HTMLResponse)
async def servo_motor_selection_page(request: Request):
    """伺服电机选型计算页面"""
    return templates.TemplateResponse("tools/servo_motor_selection.html", {"request": request})


@router.get("/servo-motor-params", response_class=HTMLResponse)
async def servo_motor_params_page(request: Request):
    """伺服电机参数计算页面"""
    return templates.TemplateResponse("tools/servo_motor_params.html", {"request": request})


@router.get("/servo-motor-selection-example", response_class=HTMLResponse)
async def servo_motor_selection_example_page(request: Request):
    """伺服电机选型举例页面"""
    return templates.TemplateResponse("tools/servo_motor_selection_example.html", {"request": request})


# API路由将在main.py中注册

