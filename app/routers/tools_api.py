"""
工具API接口
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.calculator import CurrentCalculator, InertiaCalculator, ScrewHorizontalCalculator, ScrewVerticalCalculator, BeltIntermittentCalculator
from app.services.belt_continuous_calculator import BeltContinuousCalculator
from app.services.indexing_table_calculator import IndexingTableCalculator
from app.services.motor_startup_voltage_calculator import MotorStartupVoltageCalculator
from app.services.cart_drive_power_calculator import CartDrivePowerCalculator
from app.services.crawler_robot_force_calculator import CrawlerRobotForceCalculator
from app.services.angular_acceleration_calculator import AngularAccelerationCalculator
from app.services.stepper_motor_inertia_calculator import StepperMotorInertiaCalculator
from app.services.load_torque_calculator import LoadTorqueCalculator
from app.services.fan_performance_calculator import FanPerformanceCalculator
from app.services.blower_selection_calculator import BlowerSelectionCalculator
from app.services.fan_selection_calculator import FanSelectionCalculator
from app.services.fan_selection_example_calculator import FanSelectionExampleCalculator
from app.services.servo_motor_inertia_calculator import ServoMotorInertiaCalculator
from app.services.servo_motor_selection_calculator import ServoMotorSelectionCalculator
from app.services.servo_motor_params_calculator import ServoMotorParamsCalculator
from app.services.servo_motor_selection_example_calculator import ServoMotorSelectionExampleCalculator
from app.models.schemas import CurrentCalcResponse

router = APIRouter(prefix="/api/tools", tags=["api"])


class CurrentCalcRequest(BaseModel):
    """电流计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 电流计算参数
    power: Optional[float] = Field(None, ge=0, description="功率(W或KW)")
    voltage: Optional[float] = Field(None, gt=0, description="电压(V)")
    cos_phi: Optional[float] = Field(None, ge=0, le=1, description="功率因数")
    efficiency: Optional[float] = Field(None, ge=0, le=1, description="效率")
    kc: Optional[float] = Field(None, ge=0, le=1, description="同期系数")
    total_power: Optional[float] = Field(None, ge=0, description="总功率(W)")
    apparent_power: Optional[float] = Field(None, ge=0, description="视在功率(KVA)")
    # 电阻计算参数
    rho: Optional[float] = Field(None, gt=0, description="电阻率(Ω·mm²/km)")
    area: Optional[float] = Field(None, gt=0, description="截面积(mm²)")
    r20: Optional[float] = Field(None, gt=0, description="20℃时的电阻(Ω/km)")
    a20: Optional[float] = Field(None, description="温度系数")
    temperature: Optional[float] = Field(None, description="温度(℃)")
    conductivity: Optional[float] = Field(None, gt=0, description="电导率(铜54,铝32)")
    # 电压损失参数
    u1: Optional[float] = Field(None, description="送电端电压(V)")
    u2: Optional[float] = Field(None, description="受电端电压(V)")
    ue: Optional[float] = Field(None, gt=0, description="线路额定电压(V)")
    # 电能表倍率参数
    kta: Optional[float] = Field(None, gt=0, description="实际电流互感器变比")
    ktae: Optional[float] = Field(None, gt=0, description="电能表铭牌电流互感器变比")
    ktv: Optional[float] = Field(None, gt=0, description="实际电压互感器变比")
    ktve: Optional[float] = Field(None, gt=0, description="电能表铭牌电压互感器变比")
    kj: Optional[float] = Field(None, gt=0, description="计能器倍率")
    # 反向功率计算参数
    current: Optional[float] = Field(None, gt=0, description="电流(A)")
    # 空调器容量计算参数
    unit_capacity: Optional[float] = Field(None, gt=0, description="单位面积制冷量(W/m²)")
    k: Optional[float] = Field(None, gt=0, description="容量裕量系数")
    # 较大场所空调器容量计算参数
    q: Optional[float] = Field(None, gt=0, description="房间所需冷量(105~143)")
    volume: Optional[float] = Field(None, gt=0, description="房间总容积(m³)")
    people_count: Optional[float] = Field(None, ge=0, description="房间总人数")
    x: Optional[float] = Field(None, gt=0, description="人体排热量(KJ/h，坐时432，活动时1591)")
    u: Optional[float] = Field(None, ge=0, le=0.6, description="设备同时使用率和利用率之积(0~0.6)")
    qz: Optional[float] = Field(None, ge=0, description="房间设备总发热量(KJ)")
    # 制冷量单位换算参数
    from_unit: Optional[str] = Field(None, description="从单位(W, Kcal/h, BTU/h, KJ/H)")
    to_unit: Optional[str] = Field(None, description="到单位(W, Kcal/h, BTU/h, KJ/H)")
    value: Optional[float] = Field(None, ge=0, description="数值")
    # 负荷在末端的线路电压损失计算参数
    resistance: Optional[float] = Field(None, gt=0, description="线路电阻(Ω)")
    reactance: Optional[float] = Field(None, description="线路电抗(Ω)")
    reactive_power: Optional[float] = Field(None, ge=0, description="无功功率(KVar)")
    # 线电压的电压损失计算参数（ue单位是KV）
    ue_kv: Optional[float] = Field(None, gt=0, description="线路额定电压(KV)")




class InertiaCalcRequest(BaseModel):
    """惯量计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 圆柱体参数（平行和垂直）
    d0: Optional[float] = Field(None, gt=0, description="外径(mm)")
    d1: Optional[float] = Field(None, ge=0, description="内径(mm)，0表示实心")
    L: Optional[float] = Field(None, gt=0, description="长度(mm)")
    rho: Optional[float] = Field(None, gt=0, description="密度(kg/m³)")
    e: Optional[float] = Field(None, ge=0, description="重心线与旋转轴线距离(mm)")
    # 方形物体参数
    x: Optional[float] = Field(None, gt=0, description="长度(mm)")
    y: Optional[float] = Field(None, gt=0, description="宽度(mm)")
    z: Optional[float] = Field(None, gt=0, description="高度(mm)")
    # 饼状物体参数
    d: Optional[float] = Field(None, gt=0, description="直径(mm)")
    h: Optional[float] = Field(None, gt=0, description="厚度(mm)")
    # 直线运动参数
    A: Optional[float] = Field(None, gt=0, description="电机每转1圈物体直线运动量(mm)")
    m: Optional[float] = Field(None, gt=0, description="物体质量(kg)")
    # 直接惯量参数
    J0: Optional[float] = Field(None, gt=0, description="惯量(kg·cm²)")


@router.post("/current-calc/calculate", response_model=CurrentCalcResponse)
async def calculate_current(request: CurrentCalcRequest):
    """电流计算API"""
    try:
        calculator = CurrentCalculator()
        result = calculator.calculate(request.scenario, request.dict(exclude_none=True))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ScrewHorizontalRequest(BaseModel):
    """丝杠水平运动选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    Vl: Optional[float] = Field(None, gt=0, description="速度(m/min)")
    M: Optional[float] = Field(None, gt=0, description="滑动部分质量(kg)")
    LB: Optional[float] = Field(None, gt=0, description="丝杠长度(m)")
    DB: Optional[float] = Field(None, gt=0, description="丝杠直径(m)")
    PB: Optional[float] = Field(None, gt=0, description="丝杠导程(m)")
    MC: Optional[float] = Field(None, gt=0, description="连轴器质量(kg)")
    DC: Optional[float] = Field(None, gt=0, description="连轴器直径(m)")
    mu: Optional[float] = Field(None, ge=0, description="摩擦系数")
    eta: Optional[float] = Field(None, gt=0, le=1, description="机械效率")
    t: Optional[float] = Field(None, gt=0, description="定位时间(s)")
    A: Optional[float] = Field(None, ge=0, le=1, description="加减速时间比")
    FA: Optional[float] = Field(None, ge=0, description="外力(N)")
    a: Optional[float] = Field(None, ge=-90, le=90, description="移动方向与水平轴夹角(°)")
    # 可选参数
    S: Optional[float] = Field(None, gt=0, description="安全系数")
    JM: Optional[float] = Field(None, gt=0, description="电机惯量(kg·m²)")
    i: Optional[float] = Field(None, gt=0, description="减速机减速比")
    # 分步计算参数
    JL: Optional[float] = Field(None, gt=0, description="总负荷惯量(kg·m²)")
    TL: Optional[float] = Field(None, ge=0, description="负载转矩(Nm)")
    TS: Optional[float] = Field(None, ge=0, description="启动转矩(Nm)")
    NM: Optional[float] = Field(None, gt=0, description="电机转速(rpm)")
    t0: Optional[float] = Field(None, gt=0, description="加速时间(s)")


@router.post("/inertia-calc/calculate", response_model=CurrentCalcResponse)
async def calculate_inertia(request: InertiaCalcRequest):
    """惯量计算API"""
    try:
        calculator = InertiaCalculator()
        result = calculator.calculate(request.scenario, request.dict(exclude_none=True))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


@router.post("/screw-horizontal/calculate", response_model=CurrentCalcResponse)
async def calculate_screw_horizontal(request: ScrewHorizontalRequest):
    """丝杠水平运动选型计算API"""
    try:
        calculator = ScrewHorizontalCalculator()
        # 转换为字典，排除 None 值
        params = request.dict(exclude_none=True)
        # 调试：打印参数
        import logging
        logging.info(f"计算参数: scenario={request.scenario}, params={params}")
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ScrewVerticalRequest(BaseModel):
    """丝杠垂直运动选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    Vl: Optional[float] = Field(None, gt=0, description="速度(m/min)")
    M: Optional[float] = Field(None, gt=0, description="滑动部分质量(kg)")
    LB: Optional[float] = Field(None, gt=0, description="丝杠长度(m)")
    DB: Optional[float] = Field(None, gt=0, description="丝杠直径(m)")
    PB: Optional[float] = Field(None, gt=0, description="丝杠导程(m)")
    MC: Optional[float] = Field(None, gt=0, description="连轴器质量(kg)")
    DC: Optional[float] = Field(None, gt=0, description="连轴器直径(m)")
    mu: Optional[float] = Field(None, ge=0, description="摩擦系数")
    eta: Optional[float] = Field(None, gt=0, le=1, description="机械效率")
    t: Optional[float] = Field(None, gt=0, description="定位时间(s)")
    A: Optional[float] = Field(None, ge=0, le=1, description="加减速时间比")
    FA: Optional[float] = Field(None, ge=0, description="外力(N)")
    a: Optional[float] = Field(None, ge=-90, le=90, description="移动方向与水平轴夹角(°)")
    # 可选参数
    S: Optional[float] = Field(None, gt=0, description="安全系数")
    JM: Optional[float] = Field(None, gt=0, description="电机惯量(kg·m²)")
    i: Optional[float] = Field(None, gt=0, description="减速机减速比")
    # 分步计算参数
    JL: Optional[float] = Field(None, gt=0, description="总负荷惯量(kg·m²)")
    TL: Optional[float] = Field(None, ge=0, description="负载转矩(Nm)")
    TS: Optional[float] = Field(None, ge=0, description="启动转矩(Nm)")
    NM: Optional[float] = Field(None, gt=0, description="电机转速(rpm)")
    t0: Optional[float] = Field(None, gt=0, description="加速时间(s)")


@router.post("/screw-vertical/calculate", response_model=CurrentCalcResponse)
async def calculate_screw_vertical(request: ScrewVerticalRequest):
    """丝杠垂直运动选型计算API"""
    try:
        calculator = ScrewVerticalCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class BeltIntermittentRequest(BaseModel):
    """皮带轮间歇运动选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    mL: Optional[float] = Field(None, gt=0, description="皮带与工作物总质量(kg)")
    mu: Optional[float] = Field(None, ge=0, description="滑动面摩擦系数")
    D: Optional[float] = Field(None, gt=0, description="滚筒直径(m)")
    m2: Optional[float] = Field(None, gt=0, description="滚筒质量(kg)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="传送带和滚筒的机械效率")
    etaG: Optional[float] = Field(None, gt=0, le=1, description="减速机机械效率")
    i: Optional[float] = Field(None, gt=0, description="减速比")
    t: Optional[float] = Field(None, gt=0, description="每次定位时间(s)")
    L: Optional[float] = Field(None, gt=0, description="每次运动距离(m)")
    A: Optional[float] = Field(None, ge=0, le=1, description="加减速时间比")
    FA: Optional[float] = Field(None, ge=0, description="外力(N)")
    a: Optional[float] = Field(None, ge=-90, le=90, description="移动方向与水平轴夹角(°)")
    S: Optional[float] = Field(None, gt=0, description="安全系数")
    JM: Optional[float] = Field(None, gt=0, description="电机惯量(kg·m²)")
    # 分步计算参数
    t0: Optional[float] = Field(None, gt=0, description="加速时间(s)")
    betaM: Optional[float] = Field(None, gt=0, description="电机输出轴角加速度(rad/s²)")
    JL: Optional[float] = Field(None, gt=0, description="折算到减速机轴的负载惯量(kg·m²)")
    TLM: Optional[float] = Field(None, ge=0, description="电机轴负载转矩(Nm)")
    TS: Optional[float] = Field(None, ge=0, description="电机轴加速转矩(Nm)")


@router.post("/belt-intermittent/calculate", response_model=CurrentCalcResponse)
async def calculate_belt_intermittent(request: BeltIntermittentRequest):
    """皮带轮间歇运动选型计算API"""
    try:
        calculator = BeltIntermittentCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class BeltContinuousRequest(BaseModel):
    """皮带轮连续运动选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    V: Optional[float] = Field(None, gt=0, description="线速度(m/min)")
    mL: Optional[float] = Field(None, gt=0, description="皮带与工作物总质量(kg)")
    mu: Optional[float] = Field(None, ge=0, description="滑动面摩擦系数")
    D: Optional[float] = Field(None, gt=0, description="滚筒直径(m)")
    m2: Optional[float] = Field(None, gt=0, description="滚筒质量(kg)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="传送带和滚筒的机械效率")
    etaG: Optional[float] = Field(None, gt=0, le=1, description="减速机机械效率")
    i: Optional[float] = Field(None, gt=0, description="减速比")
    FA: Optional[float] = Field(None, ge=0, description="外力(N)")
    a: Optional[float] = Field(None, ge=-90, le=90, description="移动方向与水平轴夹角(°)")
    S: Optional[float] = Field(None, gt=0, description="安全系数")
    JM: Optional[float] = Field(None, gt=0, description="电机惯量(kg·m²)")
    # 分步计算参数
    m2: Optional[float] = Field(None, gt=0, description="滚筒质量(kg)")
    JL: Optional[float] = Field(None, gt=0, description="折算到减速机轴的负载惯量(kg·m²)")
    TLM: Optional[float] = Field(None, ge=0, description="电机轴负载转矩(Nm)")


@router.post("/belt-continuous/calculate", response_model=CurrentCalcResponse)
async def calculate_belt_continuous(request: BeltContinuousRequest):
    """皮带轮连续运动选型计算API"""
    try:
        calculator = BeltContinuousCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class IndexingTableRequest(BaseModel):
    """分度盘机构选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    DT: Optional[float] = Field(None, gt=0, description="分度盘直径(m)")
    LT: Optional[float] = Field(None, gt=0, description="分度盘厚度(m)")
    DW: Optional[float] = Field(None, gt=0, description="工作物直径(m)")
    LW: Optional[float] = Field(None, gt=0, description="工作物厚度(m)")
    rho: Optional[float] = Field(None, gt=0, description="工作台材质密度(kg/m³)")
    n: Optional[float] = Field(None, gt=0, description="工作物数量(个)")
    l: Optional[float] = Field(None, gt=0, description="由分度盘中心至工作物中心的距离(m)")
    theta: Optional[float] = Field(None, gt=0, description="定位角度(°)")
    t: Optional[float] = Field(None, gt=0, description="定位时间(s)")
    A: Optional[float] = Field(None, ge=0, le=1, description="加减速时间比")
    i: Optional[float] = Field(None, gt=0, description="减速机减速比")
    etaG: Optional[float] = Field(None, gt=0, le=1, description="减速机效率")
    JM: Optional[float] = Field(None, gt=0, description="电机惯量(kg·m²)")
    S: Optional[float] = Field(None, gt=0, description="安全系数")
    # 分步计算参数
    t0: Optional[float] = Field(None, gt=0, description="加减速时间(s)")
    betaM: Optional[float] = Field(None, gt=0, description="电机轴角加速度(rad/s²)")
    JL: Optional[float] = Field(None, gt=0, description="全负载惯量(kg·m²)")
    TS: Optional[float] = Field(None, ge=0, description="电机轴加速转矩(Nm)")
    TL: Optional[float] = Field(None, ge=0, description="负载转矩(Nm)")


@router.post("/indexing-table/calculate", response_model=CurrentCalcResponse)
async def calculate_indexing_table(request: IndexingTableRequest):
    """分度盘机构选型计算API"""
    try:
        calculator = IndexingTableCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class MotorStartupVoltageRequest(BaseModel):
    """电动机启动时端电压计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    Kiq: Optional[float] = Field(None, gt=0, description="启动电流倍数")
    Sed: Optional[float] = Field(None, gt=0, description="启动电动机额定容量(kVA)")
    Sjh: Optional[float] = Field(None, ge=0, description="变压器低压侧其他负荷容量(kVA)")
    Seb: Optional[float] = Field(None, gt=0, description="变压器额定容量(kVA)")
    uk: Optional[float] = Field(None, gt=0, description="变压器阻抗电压(%)")
    Ped: Optional[float] = Field(None, gt=0, description="电动机额定功率(kW)")
    L: Optional[float] = Field(None, gt=0, description="线路长度(km)")
    deltaUx: Optional[float] = Field(None, ge=0, description="每千瓦公里单位电压损失(%)")


@router.post("/motor-startup-voltage/calculate", response_model=CurrentCalcResponse)
async def calculate_motor_startup_voltage(request: MotorStartupVoltageRequest):
    """电动机启动时端电压计算API"""
    try:
        calculator = MotorStartupVoltageCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class CartDrivePowerRequest(BaseModel):
    """小车驱动电机功率计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 输入参数
    m: Optional[float] = Field(None, gt=0, description="质量(t)")
    v: Optional[float] = Field(None, gt=0, description="小车速度(m/min)")
    u: Optional[float] = Field(None, ge=0, description="摩擦系数(一般0.1)")
    K: Optional[float] = Field(None, gt=0, description="功率系数(1.2~2)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="传动效率(默认0.8)")
    # 分步计算参数
    F: Optional[float] = Field(None, gt=0, description="牵引力(kN)")
    P: Optional[float] = Field(None, gt=0, description="电机功率(kW)")


@router.post("/cart-drive-power/calculate", response_model=CurrentCalcResponse)
async def calculate_cart_drive_power(request: CartDrivePowerRequest):
    """小车驱动电机功率计算API"""
    try:
        calculator = CartDrivePowerCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class CrawlerRobotForceRequest(BaseModel):
    """履带机器人驱动力计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 道路参数
    f: Optional[float] = Field(None, ge=0, description="滚动摩擦系数")
    u: Optional[float] = Field(None, ge=0, description="滑动摩擦系数")
    peak_attachment: Optional[float] = Field(None, gt=0, description="地面峰值附着系数")
    slope_percent: Optional[float] = Field(None, ge=0, description="轨道坡度(%)")
    obstacle_height: Optional[float] = Field(None, ge=0, description="障碍高度(mm)")
    # 车体参数
    m1: Optional[float] = Field(None, gt=0, description="车体重量(kg)")
    m2: Optional[float] = Field(None, ge=0, description="负载重量(kg)")
    D: Optional[float] = Field(None, gt=0, description="履带轮子直径(mm)")
    D_drive: Optional[float] = Field(None, gt=0, description="履带驱动轮直径(mm)")
    B: Optional[float] = Field(None, gt=0, description="履带间距（左右）(mm)")
    L: Optional[float] = Field(None, gt=0, description="接地长度（前后）(mm)")
    # 运行参数
    v_rated: Optional[float] = Field(None, gt=0, description="平地车体额定速度(m/s)")
    v_max: Optional[float] = Field(None, gt=0, description="平地车体最大速度(m/s)")
    a: Optional[float] = Field(None, ge=0, description="运行加速度(m/s²)")
    a_slope: Optional[float] = Field(None, ge=0, description="坡道加速度(m/s²)")
    # 电机参数
    n_motor: Optional[float] = Field(None, gt=0, description="电机数量")
    n_effective: Optional[float] = Field(None, gt=0, description="有效电机数")
    P_motor: Optional[float] = Field(None, gt=0, description="电机功率(W)")
    I_no_load: Optional[float] = Field(None, ge=0, description="空转电流(A)")
    I_actual: Optional[float] = Field(None, gt=0, description="实际电流(平均)(A)")
    T_rated: Optional[float] = Field(None, gt=0, description="额定扭矩(Nm)")
    I_rated: Optional[float] = Field(None, gt=0, description="额定电流(A)")
    T_max: Optional[float] = Field(None, gt=0, description="最大扭矩(Nm)")
    n_rated: Optional[float] = Field(None, gt=0, description="额定转速(rpm)")
    n_max: Optional[float] = Field(None, gt=0, description="最高转速(rpm)")
    current_unevenness: Optional[float] = Field(None, gt=0, description="电流最大不均匀度")
    # 减速器参数
    i_total: Optional[float] = Field(None, gt=0, description="总减速比")
    i_custom: Optional[float] = Field(None, gt=0, description="自制减速比")
    i_reducer: Optional[float] = Field(None, gt=0, description="减速器减速比")
    gear_large: Optional[float] = Field(None, gt=0, description="大齿轮")
    gear_small: Optional[float] = Field(None, gt=0, description="小齿轮")
    T_gear_large: Optional[float] = Field(None, gt=0, description="大齿轮许用扭矩(Nm)")
    T_gear_small: Optional[float] = Field(None, gt=0, description="小齿轮许用扭矩(Nm)")
    n_reducer_rated: Optional[float] = Field(None, gt=0, description="减速器额定转速(rpm)")
    n_reducer_max: Optional[float] = Field(None, gt=0, description="减速器最高转速(rpm)")
    T_reducer_rated: Optional[float] = Field(None, gt=0, description="减速器额定扭矩(Nm)")


@router.post("/crawler-robot-force/calculate", response_model=CurrentCalcResponse)
async def calculate_crawler_robot_force(request: CrawlerRobotForceRequest):
    """履带机器人驱动力计算API"""
    try:
        calculator = CrawlerRobotForceCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ElectronicGearRatioRequest(BaseModel):
    """伺服电机电子齿轮比计算请求模型"""
    # 输入参数
    encoder_resolution: Optional[float] = Field(None, gt=0, description="编码器分辨率(脉冲/转)")
    mechanical_ratio: Optional[float] = Field(None, gt=0, description="机械减速比")
    load_distance: Optional[float] = Field(None, gt=0, description="负载移动距离(mm)")
    motor_revolutions: Optional[float] = Field(None, gt=0, description="电机转数(转)")
    pulse_equivalent: Optional[float] = Field(None, gt=0, description="脉冲当量(mm/脉冲)")


@router.post("/electronic-gear-ratio/calculate", response_model=CurrentCalcResponse)
async def calculate_electronic_gear_ratio(request: ElectronicGearRatioRequest):
    """伺服电机电子齿轮比计算API"""
    try:
        from app.services.electronic_gear_ratio_calculator import ElectronicGearRatioCalculator
        calculator = ElectronicGearRatioCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class AngularAccelerationRequest(BaseModel):
    """角加速度计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    i: Optional[float] = Field(None, gt=0, description="减速比")
    t: Optional[float] = Field(None, gt=0, description="每次定位时间(s)")
    L: Optional[float] = Field(None, gt=0, description="每次运动角度(°)")
    A: Optional[float] = Field(None, gt=0, lt=1, description="加减速时间比")
    J: Optional[float] = Field(None, gt=0, description="负载惯量(Kg.m²)")
    betaM: Optional[float] = Field(None, gt=0, description="电机输出轴角加速度(rad/s²)")


@router.post("/angular-acceleration/calculate", response_model=CurrentCalcResponse)
async def calculate_angular_acceleration(request: AngularAccelerationRequest):
    """角加速度计算API"""
    try:
        calculator = AngularAccelerationCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class StepperMotorInertiaRequest(BaseModel):
    """步进电机惯量计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 滚珠丝杠参数
    W: Optional[float] = Field(None, gt=0, description="可动部分总重量(kg)")
    BP: Optional[float] = Field(None, gt=0, description="丝杠螺距(mm)")
    # 齿条和小齿轮参数
    D: Optional[float] = Field(None, gt=0, description="小齿轮/链轮直径(mm)")
    # 旋转体参数
    J1: Optional[float] = Field(None, ge=0, description="转盘的惯性矩(kg·m²)")
    L: Optional[float] = Field(None, gt=0, description="物体与旋转轴的距离(mm)")
    # 通用参数
    GL: Optional[float] = Field(None, gt=0, description="减速比")
    # 角加速度参数
    n: Optional[float] = Field(None, gt=0, description="转速(n/s, 转/秒)")
    delta_t: Optional[float] = Field(None, gt=0, description="加速时间(s)")
    # 电机力矩参数
    J: Optional[float] = Field(None, gt=0, description="惯量(kg·m²)")
    epsilon: Optional[float] = Field(None, gt=0, description="角加速度(rad/s²)")
    T_L: Optional[float] = Field(None, ge=0, description="系统外力折算到电机上的力矩(Nm)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="传动系统的效率")


@router.post("/stepper-motor-inertia/calculate", response_model=CurrentCalcResponse)
async def calculate_stepper_motor_inertia(request: StepperMotorInertiaRequest):
    """步进电机惯量计算API"""
    try:
        calculator = StepperMotorInertiaCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class LoadTorqueRequest(BaseModel):
    """不同驱动机构下负载转矩计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 通用参数
    FA: Optional[float] = Field(None, description="外力(N)")
    m: Optional[float] = Field(None, gt=0, description="工作物与工作台的总质量(kg)")
    g: Optional[float] = Field(None, gt=0, description="重力加速度(m/s²)，默认9.807")
    alpha: Optional[float] = Field(None, description="倾斜角度(°)")
    mu: Optional[float] = Field(None, ge=0, description="滑动面的摩擦系数")
    D: Optional[float] = Field(None, gt=0, description="终段滑轮直径/小齿轮/链轮直径(m)")
    # 滚珠丝杠参数
    PB: Optional[float] = Field(None, gt=0, description="滚珠螺杆螺距(m/rev)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="机械效率")
    mu0: Optional[float] = Field(None, ge=0, description="预压螺帽的内部摩擦系数")
    F0: Optional[float] = Field(None, ge=0, description="预负载(N)")
    i: Optional[float] = Field(None, gt=0, description="减速比")
    # 实际测试方法参数
    FB: Optional[float] = Field(None, gt=0, description="主轴开始运动时的力(N)")


@router.post("/load-torque/calculate", response_model=CurrentCalcResponse)
async def calculate_load_torque(request: LoadTorqueRequest):
    """不同驱动机构下负载转矩计算API"""
    try:
        calculator = LoadTorqueCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class FanPerformanceRequest(BaseModel):
    """风机性能表计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 主要参数
    D: Optional[float] = Field(None, gt=0, description="叶轮直径(m)")
    n: Optional[float] = Field(None, gt=0, description="主轴转速(rpm)")
    T: Optional[float] = Field(None, description="介质温度(°C)")
    P_inlet: Optional[float] = Field(None, gt=0, description="进口大气压(Pa)")
    # 单个计算参数
    rho: Optional[float] = Field(None, gt=0, description="空气密度(kg/m³)")
    psi_p: Optional[float] = Field(None, description="压力系数")
    phi: Optional[float] = Field(None, description="流量系数")
    eta: Optional[float] = Field(None, gt=0, le=1, description="效率")
    P: Optional[float] = Field(None, description="压力(Pa)")
    Q: Optional[float] = Field(None, description="流量(m³/h)")
    # 性能点列表（用于完整计算）
    performance_points: Optional[list] = Field(None, description="性能点列表，每个点包含psi_p, phi, eta")


@router.post("/fan-performance/calculate", response_model=CurrentCalcResponse)
async def calculate_fan_performance(request: FanPerformanceRequest):
    """风机性能表计算API"""
    try:
        calculator = FanPerformanceCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class BlowerSelectionRequest(BaseModel):
    """鼓风机选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 压力参数
    Pd: Optional[float] = Field(None, ge=0, description="高炉炉顶压力(MPa)")
    delta_P1: Optional[float] = Field(None, ge=0, description="高炉送风系统阻力(MPa)")
    delta_Pf: Optional[float] = Field(None, ge=0, description="高炉送风管路阻力(MPa)")
    P0: Optional[float] = Field(None, gt=0, description="标准大气压(MPa)")
    delta_Px: Optional[float] = Field(None, ge=0, description="风机入口阻力(MPa)")
    # 风量参数
    Vu: Optional[float] = Field(None, gt=0, description="高炉有效容积(m³)")
    i: Optional[float] = Field(None, gt=0, description="高炉利用系数(t/m³.d)")
    q: Optional[float] = Field(None, gt=0, description="单位生铁耗风量(m³/t)")
    delta: Optional[float] = Field(None, ge=0, le=100, description="高炉漏风率(%)")
    Qf: Optional[float] = Field(None, ge=0, description="高炉送风管路漏风量(m³/h)")
    # 修正系数参数
    PX: Optional[float] = Field(None, gt=0, description="风机入口实际大气压(Pa)")
    T0: Optional[float] = Field(None, gt=0, description="标准温度(K)")
    Ta: Optional[float] = Field(None, gt=0, description="风机入口实际温度(K)")
    PZ: Optional[float] = Field(None, ge=0, description="风机入口水蒸气分压(Pa)")
    Pa: Optional[float] = Field(None, gt=0, description="风机入口大气压(Pa)")
    # 功率计算参数
    k: Optional[float] = Field(None, gt=1, description="绝热指数")
    eta_n: Optional[float] = Field(None, gt=0, le=1, description="内效率")
    eta_m: Optional[float] = Field(None, gt=0, le=1, description="机械效率")


@router.post("/blower-selection/calculate", response_model=CurrentCalcResponse)
async def calculate_blower_selection(request: BlowerSelectionRequest):
    """鼓风机选型计算API"""
    try:
        calculator = BlowerSelectionCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class FanSelectionRequest(BaseModel):
    """风机选型计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 基本参数
    Q: Optional[float] = Field(None, gt=0, description="流量(m³/h)")
    P: Optional[float] = Field(None, gt=0, description="全压(Pa)")
    H: Optional[float] = Field(None, ge=0, description="海拔高度(m)")
    P_inlet: Optional[float] = Field(None, ge=0, description="进口压力(Pa)")
    T: Optional[float] = Field(None, description="工作温度(℃)")
    k: Optional[float] = Field(None, gt=1, description="绝热指数")
    n: Optional[float] = Field(None, gt=0, description="工作转速(rpm)")
    fan_type: Optional[str] = Field(None, description="风机型号")
    D: Optional[float] = Field(None, gt=0, description="给定叶轮直径(m)")
    suction_type: Optional[str] = Field(None, description="单吸/双吸")
    rho_standard: Optional[float] = Field(None, gt=0, description="标准密度(kg/m³)")
    # 性能点列表（可选，如果不提供则从数据库查找）
    performance_points: Optional[list] = Field(None, description="性能点列表，每个点包含phi, psi_p, eta")


@router.post("/fan-selection/calculate", response_model=CurrentCalcResponse)
async def calculate_fan_selection(request: FanSelectionRequest):
    """风机选型计算API"""
    try:
        calculator = FanSelectionCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class FanSelectionExampleRequest(BaseModel):
    """风机选型计算举例请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 煤质参数
    Car: Optional[float] = Field(None, ge=0, le=100, description="应用基碳 (%)")
    OAR: Optional[float] = Field(None, ge=0, le=100, description="应用基氧 (%)")
    Hy: Optional[float] = Field(None, ge=0, le=100, description="应用基氢 (%)")
    Nar: Optional[float] = Field(None, ge=0, le=100, description="应用基氮 (%)")
    War: Optional[float] = Field(None, ge=0, le=100, description="全水 (%)")
    Aar: Optional[float] = Field(None, ge=0, le=100, description="应用基灰 (%)")
    Sar: Optional[float] = Field(None, ge=0, le=100, description="全硫 (%)")
    Vdaf: Optional[float] = Field(None, ge=0, le=100, description="挥发份 (%)")
    Qnet_ar: Optional[float] = Field(None, gt=0, description="低位发热量 (kJ/kg)")
    # 燃煤量（可直接提供或通过锅炉参数计算）
    B: Optional[float] = Field(None, gt=0, description="燃煤量 (kg/s)")
    # 锅炉参数（用于计算燃煤量）
    D: Optional[float] = Field(None, gt=0, description="锅炉蒸发量 (t/h)")
    h_main: Optional[float] = Field(None, description="主蒸汽焓 (kJ/kg)")
    h_feed: Optional[float] = Field(None, description="给水焓 (kJ/kg)")
    blowdown: Optional[float] = Field(None, ge=0, le=1, description="排污率")
    h_blowdown: Optional[float] = Field(None, description="排污水焓 (kJ/kg)")
    eta_boiler: Optional[float] = Field(None, gt=0, le=1, description="锅炉效率")
    # 其他参数
    alpha: Optional[float] = Field(None, gt=1, description="过量空气系数")
    tk: Optional[float] = Field(None, description="空气温度 (°C)")
    tg: Optional[float] = Field(None, description="烟气温度 (°C)")
    b: Optional[float] = Field(None, gt=0, description="当地大气压 (kPa)")
    k1: Optional[float] = Field(None, gt=0, description="送风机风量储备系数")
    k2_primary: Optional[float] = Field(None, gt=0, description="一次风机风压储备系数")
    k2_secondary: Optional[float] = Field(None, gt=0, description="二次风机风压储备系数")
    delta_h_primary: Optional[float] = Field(None, gt=0, description="一次风机总阻力 (Pa)")
    delta_h_secondary: Optional[float] = Field(None, gt=0, description="二次风机总阻力 (Pa)")
    eta1: Optional[float] = Field(None, gt=0, le=1, description="风机效率")
    eta2: Optional[float] = Field(None, gt=0, le=1, description="机械效率")
    eta3: Optional[float] = Field(None, gt=0, le=1, description="电动机效率")
    K_motor: Optional[float] = Field(None, gt=0, description="电动机备用系数")
    rho_ko: Optional[float] = Field(None, gt=0, description="空气密度 (kg/m³)")


@router.post("/fan-selection-example/calculate", response_model=CurrentCalcResponse)
async def calculate_fan_selection_example(request: FanSelectionExampleRequest):
    """风机选型计算举例API"""
    try:
        calculator = FanSelectionExampleCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ServoMotorInertiaRequest(BaseModel):
    """伺服电机惯量计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    # 基本参数
    M: Optional[float] = Field(None, gt=0, description="被移动件的质量 (kg)")
    v_fast: Optional[float] = Field(None, gt=0, description="快移速度 (m/min)")
    t_acc: Optional[float] = Field(None, gt=0, description="加速时间 (s)")
    a: Optional[float] = Field(None, description="加速度 (m/s²)")
    FC: Optional[float] = Field(None, ge=0, description="最大切削抗力 (N)")
    v_cut: Optional[float] = Field(None, ge=0, description="最大抗力时的速度 (m/min)")
    u: Optional[float] = Field(None, ge=0, le=1, description="摩擦系数")
    m_gear: Optional[float] = Field(None, gt=0, description="齿轮模数")
    Z: Optional[float] = Field(None, gt=0, description="齿轮齿数")
    alpha_gear: Optional[float] = Field(None, ge=0, description="齿轮斜角 (度)")
    D: Optional[float] = Field(None, gt=0, description="齿轮分度圆直径 (m)")
    eta: Optional[float] = Field(None, gt=0, le=1, description="传动效率")
    i: Optional[float] = Field(None, gt=0, description="减速比")
    eta_reducer: Optional[float] = Field(None, gt=0, le=1, description="减速机效率")
    Jm: Optional[float] = Field(None, gt=0, description="电机自身转动惯量 (kg·m²)")
    Jm_inertia: Optional[float] = Field(None, gt=0, description="用于惯量匹配的电机自身转动惯量 (kg·m²)，如果未提供则使用Jm")
    JG: Optional[float] = Field(None, ge=0, description="齿轮自身惯量 (kg·m²)")
    Jg: Optional[float] = Field(None, ge=0, description="减速机自身惯量 (kg·m²)")
    is_vertical: Optional[bool] = Field(None, description="是否垂直运动")
    g: Optional[float] = Field(None, gt=0, description="重力加速度 (m/s²)")
    # 侧倾力矩计算参数
    an: Optional[float] = Field(None, ge=0, le=90, description="齿轮端面压力角 (度)")
    a0: Optional[float] = Field(None, ge=0, le=90, description="斜角 (度)")
    Z2: Optional[float] = Field(None, gt=0, description="减速器输出端轴承的支撑跨度 (m)")
    X2: Optional[float] = Field(None, ge=0, description="齿轮受力X2 (mm)")
    y2: Optional[float] = Field(None, gt=0, description="轴向力的力臂长 (m)")


@router.post("/servo-motor-inertia/calculate", response_model=CurrentCalcResponse)
async def calculate_servo_motor_inertia(request: ServoMotorInertiaRequest):
    """伺服电机惯量计算API"""
    try:
        calculator = ServoMotorInertiaCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ServoMotorSelectionRequest(BaseModel):
    """伺服电机选型计算请求模型"""
    scenario: str = Field(..., description="计算场景: linear_motor 或 rotary_motor")
    # 直线电机参数
    a: Optional[float] = Field(None, gt=0, description="加速度 (m/s²)")
    V: Optional[float] = Field(None, gt=0, description="平台移动速度 (m/min)")
    S: Optional[float] = Field(None, gt=0, description="单一性行程移动距离 (mm)")
    Mt: Optional[float] = Field(None, gt=0, description="移动平台质量 (kg)")
    Mf: Optional[float] = Field(None, ge=0, description="负载质量 (kg)")
    mu: Optional[float] = Field(None, ge=0, le=1, description="导轨摩擦系数")
    # 旋转电机参数
    eta: Optional[float] = Field(None, gt=0, le=1, description="机械传动效率")
    PB: Optional[float] = Field(None, gt=0, description="导螺杆节距 (mm)")
    DB: Optional[float] = Field(None, gt=0, description="丝杆直径 (mm)")
    MB: Optional[float] = Field(None, ge=0, description="丝杆质量 (kg)")
    g: Optional[float] = Field(None, gt=0, description="重力加速度 (m/s²)")


@router.post("/servo-motor-selection/calculate", response_model=CurrentCalcResponse)
async def calculate_servo_motor_selection(request: ServoMotorSelectionRequest):
    """伺服电机选型计算API"""
    try:
        calculator = ServoMotorSelectionCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ServoMotorParamsRequest(BaseModel):
    """伺服电机参数计算请求模型"""
    scenario: str = Field(..., description="计算场景: servo_motor_params")
    # 基本参数
    axis_type: Optional[str] = Field("水平轴", description="轴类型: 水平轴、重力轴、倾斜轴")
    m: Optional[float] = Field(None, gt=0, description="质量 (kg)")
    mb: Optional[float] = Field(0, ge=0, description="平衡质量 (kg)")
    Fb: Optional[float] = Field(0, ge=0, description="平衡力 (N)")
    d: Optional[float] = Field(None, gt=0, description="丝杠直径 (mm)")
    Pb: Optional[float] = Field(None, gt=0, description="丝杠导程 (mm/rev)")
    l: Optional[float] = Field(None, gt=0, description="丝杠长度 (mm)")
    z: Optional[float] = Field(1, gt=0, description="减速比分母（减速比 = 1/z）")
    J13: Optional[float] = Field(0, ge=0, description="其他惯量 (kg·m²)")
    u: Optional[float] = Field(0.1, ge=0, le=1, description="摩擦系数")
    Fc: Optional[float] = Field(0, ge=0, description="切削力 (N)")
    eta: Optional[float] = Field(0.9, gt=0, le=1, description="机械效率")
    theta: Optional[float] = Field(0, ge=0, le=90, description="倾斜角 (°)")
    V: Optional[float] = Field(None, gt=0, description="最大进给速度 (m/min)")
    amax: Optional[float] = Field(None, gt=0, description="最大加速度 (m/s²)")
    # 电机参数（可选，用于选型确认）
    Jm: Optional[float] = Field(None, gt=0, description="电机惯量 (kg·m²)")
    Ts: Optional[float] = Field(None, gt=0, description="电机扭矩 (N·m)")
    Tmax_motor: Optional[float] = Field(None, gt=0, description="电机最大扭矩 (N·m)")
    Nmax_motor: Optional[float] = Field(None, gt=0, description="电机最高转速 (rev/min)")


@router.post("/servo-motor-params/calculate", response_model=CurrentCalcResponse)
async def calculate_servo_motor_params(request: ServoMotorParamsRequest):
    """伺服电机参数计算API"""
    try:
        calculator = ServoMotorParamsCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")


class ServoMotorSelectionExampleRequest(BaseModel):
    """伺服电机选型举例计算请求模型"""
    # ①机械系统的决定
    M: Optional[float] = Field(None, gt=0, description="负载质量 (kg)")
    P: Optional[float] = Field(None, gt=0, description="滚珠丝杠节距 (mm)")
    D: Optional[float] = Field(None, gt=0, description="滚珠丝杠直径 (mm)")
    MB: Optional[float] = Field(None, gt=0, description="滚珠丝杠质量 (kg)")
    mu: Optional[float] = Field(0.1, ge=0, description="滚珠丝杠摩擦系数")
    G: Optional[float] = Field(1, gt=0, description="减速比（无减速器时为1）")
    eta: Optional[float] = Field(1, gt=0, le=1, description="效率（无减速器时为1）")
    # ②动作模式的决定
    V: Optional[float] = Field(None, gt=0, description="负载移动速度 (mm/s)")
    L: Optional[float] = Field(None, gt=0, description="行程 (mm)")
    tS: Optional[float] = Field(None, gt=0, description="行程时间 (s)")
    tA: Optional[float] = Field(None, gt=0, description="加减速时间 (s)")
    AP: Optional[float] = Field(None, gt=0, description="定位精度 (mm)")
    # 电机参数（可选，用于验证）
    JM: Optional[float] = Field(None, gt=0, description="电机转子惯量 (kg·m²)")
    TM: Optional[float] = Field(None, gt=0, description="电机额定转矩 (N·m)")
    Tmax_motor: Optional[float] = Field(None, gt=0, description="电机瞬时最大转矩 (N·m)")
    Nmax_motor: Optional[float] = Field(None, gt=0, description="电机额定转数 (r/min)")


@router.post("/servo-motor-selection-example/calculate", response_model=CurrentCalcResponse)
async def calculate_servo_motor_selection_example(request: ServoMotorSelectionExampleRequest):
    """伺服电机选型举例计算API"""
    try:
        calculator = ServoMotorSelectionExampleCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")

