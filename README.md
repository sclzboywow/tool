# Excel工具转Web在线工具站 - 通用开发指南

基于Excel工具转换的Web在线计算工具站通用开发框架，提供标准化的开发流程和代码组织方式。

## 技术栈

- **后端**: FastAPI + Python 3.12+
- **前端**: HTML5 + JavaScript (原生，无框架依赖)
- **模板引擎**: Jinja2
- **数据验证**: Pydantic
- **部署**: Uvicorn + Nginx
- **Excel解析**: openpyxl

## 项目结构

```
workspace/
├── app/                          # FastAPI应用主目录
│   ├── main.py                  # FastAPI应用入口，配置路由和静态文件
│   ├── models/                  # 数据模型
│   │   └── schemas.py          # Pydantic请求/响应模型
│   ├── routers/                 # 路由模块
│   │   ├── tools.py            # 页面路由（渲染HTML）
│   │   └── tools_api.py        # API路由（计算接口）
│   ├── services/                # 业务逻辑层（计算服务）
│   │   ├── calculator.py       # 计算器统一导出
│   │   ├── current_calculator.py      # 工具1的计算逻辑
│   │   ├── inertia_calculator.py      # 工具2的计算逻辑
│   │   └── screw_horizontal_calculator.py  # 工具3的计算逻辑
│   └── utils/                   # 工具函数
├── templates/                   # Jinja2模板
│   ├── base.html               # 基础模板（导航、样式）
│   ├── index.html              # 主页（工具列表）
│   └── tools/                  # 各工具页面
│       ├── current_calc.html   # 工具1页面
│       ├── inertia_calc.html   # 工具2页面
│       └── screw_horizontal.html  # 工具3页面
├── static/                      # 静态资源
│   ├── css/
│   │   └── style.css           # 全局样式
│   └── js/
│       ├── common.js           # 公共JavaScript函数
│       └── tools/              # 各工具的前端逻辑
│           ├── current_calc.js
│           ├── inertia_calc.js
│           └── screw_horizontal.js
├── scripts/                     # 开发辅助脚本
│   ├── analyze_excel.py        # Excel分析工具
│   ├── view_excel.py           # Excel查看工具
│   ├── compare_formulas.py     # 公式对比工具
│   └── verify_*.py             # 公式验证工具
├── data/                        # 数据目录
│   └── *.xlsx                  # Excel源文件
├── requirements.txt             # Python依赖
└── README.md                    # 本文档
```

## 开发流程

### 配置化工具元数据

- 在 `configs/tools/<tool>.yaml` 维护工具标识、标题、场景、输入参数、示例用例及物理公式说明，详见 `scripts/tool_config_models.py` 中的 JSONSchema。
- 使用 `python scripts/validate_tool_configs.py --generate-index` 进行校验并生成索引文档：
  - 校验所有 YAML 是否符合 Pydantic/JSONSchema 约束，并在 `configs/tool_config.schema.json` 生成最新 schema。
  - 将配置汇总为 `docs/tool_index.md`（Markdown）与 `docs/tool_index.html`（预览版）方便评审。
- CI 会自动执行上述脚本并确保生成文件已提交。

### 第一步：分析Excel文件

使用分析脚本了解Excel结构：

```bash
# 查看Excel工作表列表
python3 scripts/view_excel.py data/文件名.xlsx

# 分析特定工作表
python3 scripts/analyze_excel.py data/文件名.xlsx "工作表名"
```

**分析要点**：
- 识别所有计算模块
- 提取输入参数和输出结果
- 提取计算公式
- 记录参数说明和单位

### 第二步：创建后端计算服务

在 `app/services/` 目录创建新的计算器类：

```python
# app/services/your_calculator.py
"""
工具名称计算服务
"""
import math
from typing import Dict, Any
from app.models.schemas import CurrentCalcResponse

class YourCalculator:
    """工具名称计算器"""
    
    SCENARIO_NAMES = {
        "scenario1": "场景1名称",
        "scenario2": "场景2名称",
    }
    
    def calculate(self, scenario: str, params: Dict[str, Any]) -> CurrentCalcResponse:
        """根据场景计算"""
        if scenario == "scenario1":
            return self._calculate_scenario1(params)
        elif scenario == "scenario2":
            return self._calculate_scenario2(params)
        else:
            raise ValueError(f"未知的计算场景: {scenario}")
    
    def _calculate_scenario1(self, params: Dict[str, Any]) -> CurrentCalcResponse:
        """场景1计算"""
        # 1. 获取参数
        param1 = params.get("param1")
        param2 = params.get("param2")
        
        # 2. 验证参数
        if param1 is None or param1 <= 0:
            raise ValueError("参数1必须大于0")
        
        # 3. 执行计算
        result = param1 * param2  # 示例计算
        
        # 4. 构建公式字符串（多行格式，使用<br>换行）
        formula = f"公式: result = param1 × param2<br>"
        formula += f"  = {param1} × {param2}<br>"
        formula += f"  = {result:.4f}"
        
        # 5. 返回结果
        return CurrentCalcResponse(
            result=round(result, 4),
            unit="单位",
            formula=formula,
            scenario_name=self.SCENARIO_NAMES["scenario1"]
        )
```

**关键点**：
- 每个计算场景一个独立方法
- 参数验证要完整
- 公式字符串使用多行格式（`<br>`换行）
- 包含物理来源说明（在HTML中）

### 第三步：创建API路由

在 `app/routers/tools_api.py` 中添加新的请求模型和路由：

```python
# 1. 添加请求模型
class YourToolRequest(BaseModel):
    """工具名称计算请求模型"""
    scenario: str = Field(..., description="计算场景")
    param1: Optional[float] = Field(None, gt=0, description="参数1说明")
    param2: Optional[float] = Field(None, gt=0, description="参数2说明")

# 2. 添加API路由
@router.post("/your-tool/calculate", response_model=CurrentCalcResponse)
async def calculate_your_tool(request: YourToolRequest):
    """工具名称计算API"""
    try:
        calculator = YourCalculator()
        params = request.dict(exclude_none=True)
        result = calculator.calculate(request.scenario, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {str(e)}")
```

### 第四步：创建页面路由

在 `app/routers/tools.py` 中添加页面路由：

```python
@router.get("/your-tool", response_class=HTMLResponse)
async def your_tool_page(request: Request):
    """工具名称页面"""
    return templates.TemplateResponse("tools/your_tool.html", {"request": request})
```

### 第五步：创建前端HTML页面

在 `templates/tools/your_tool.html` 创建页面。**标准布局结构**（参考 belt-intermittent 样式）：

```html
{% extends "base.html" %}

{% block title %}工具名称 - 电机电力电气计算工具站{% endblock %}

{% block content %}
<!-- 1. 页面标题 -->
<div class="page-header">
    <h1>工具名称</h1>
    <p class="subtitle">工具描述，说明工具的主要功能和计算内容</p>
</div>

<!-- 2. 参数说明表格（3栏布局） -->
<div class="reference-table" style="background: #e8f5e9; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; border: 1px solid #c8e6c9;">
    <div style="display: grid; grid-template-columns: 1fr 4px 1fr 4px 1fr; gap: 1rem; align-items: start;">
        <!-- 第一列 -->
        <div>
            <h3 style="color: #2c3e50; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">参数说明</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <tr><td style="padding: 0.3rem 0;">参数1</td><td style="padding: 0.3rem 0;">参数1说明(单位)</td></tr>
                <tr><td style="padding: 0.3rem 0;">参数2</td><td style="padding: 0.3rem 0;">参数2说明(单位)</td></tr>
            </table>
        </div>
        <div style="background: #4caf50; width: 2px; height: 100%; border-radius: 1px;"></div>
        <!-- 第二列 -->
        <div>
            <h3 style="color: #2c3e50; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">参数说明</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <tr><td style="padding: 0.3rem 0;">参数3</td><td style="padding: 0.3rem 0;">参数3说明(单位)</td></tr>
                <tr><td style="padding: 0.3rem 0;">参数4</td><td style="padding: 0.3rem 0;">参数4说明(单位)</td></tr>
            </table>
        </div>
        <div style="background: #4caf50; width: 2px; height: 100%; border-radius: 1px;"></div>
        <!-- 第三列 -->
        <div>
            <h3 style="color: #2c3e50; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;">参数说明</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <tr><td style="padding: 0.3rem 0;">参数5</td><td style="padding: 0.3rem 0;">参数5说明(单位)</td></tr>
            </table>
        </div>
    </div>
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #c8e6c9; text-align: right;">
        <span style="color: #e74c3c; font-size: 0.9rem; font-weight: 500;">注: *为必填项</span>
    </div>
</div>

<!-- 3. 标签页导航（如果多个计算模块） -->
<div class="sub-tabs-container">
    <div id="sub-tabs-your-tool" class="sub-tabs active">
        <button class="sub-tab active" onclick="switchSubTab('scenario1')">1. 场景1名称</button>
        <button class="sub-tab" onclick="switchSubTab('scenario2')">2. 场景2名称</button>
    </div>
</div>

<!-- 4. 场景1计算表单 -->
<div id="scenario1" class="tab-content active">
    <div class="tool-form">
        <h2>场景1名称</h2>
        
        <!-- 公式说明（在输入表单之前） -->
        <p class="formula-info">公式: result = param1 × param2</p>
        <p class="formula-info">其他公式说明...</p>
        
        <!-- 物理来源和适用范围说明（在输入表单之前） -->
        <p style="color: #7f8c8d; font-size: 0.9rem; margin-bottom: 1rem; padding: 0.75rem; background: #e8f4f8; border-left: 4px solid #3498db; border-radius: 4px;">
            <strong>物理来源：</strong>公式的物理原理说明，解释公式的来源和理论基础。<br>
            <strong>适用范围：</strong>公式的适用范围，说明在什么情况下可以使用这个公式。
        </p>
        
        <!-- 输入表单 -->
        <div class="form-group">
            <label for="param1">参数1 <span class="required">*</span></label>
            <input type="number" id="param1" step="any" min="0.000001" placeholder="例如: 100">
            <small>参数1的说明或提示</small>
        </div>
        
        <div class="form-group">
            <label for="param2">参数2 <span class="required">*</span></label>
            <input type="number" id="param2" step="any" min="0.000001" placeholder="例如: 10">
            <small>参数2的说明或提示</small>
        </div>
        
        <!-- 计算按钮 -->
        <button class="btn btn-primary" onclick="calculateScenario1()">计算</button>
        
        <!-- 结果显示 -->
        <div id="scenario1_result" class="result-box" style="display: none;">
            <h3>计算结果</h3>
            <div class="result-value">结果名称: <span id="scenario1_result_value"></span> <span id="scenario1_result_unit"></span></div>
            <div class="result-formula" id="scenario1_result_formula"></div>
        </div>
    </div>
</div>

<!-- 场景2计算表单（类似结构） -->
<div id="scenario2" class="tab-content">
    <div class="tool-form">
        <h2>场景2名称</h2>
        <!-- 类似结构... -->
    </div>
</div>

<script src="{{ static_asset('js/tools/your_tool.js') }}"></script>
{% endblock %}
```

**标准布局顺序**（必须遵循）：
1. **页面标题**：`page-header` 包含标题和描述
2. **参数说明表格**：3栏布局，使用绿色分隔线，底部有必填项说明
3. **标签页导航**：如果有多于1个计算模块，使用标签页组织
4. **每个标签页内容**：
   - 标题（h2）
   - 公式说明（`formula-info` 类）
   - 物理来源和适用范围说明（蓝色边框框）
   - 输入表单（`form-group`）
   - 计算按钮
   - 结果显示区域

**关键点**：
- 使用 `base.html` 作为基础模板
- 参数说明表格使用3栏布局，绿色分隔线（`#4caf50`）
- 公式说明在输入表单之前
- 物理来源和适用范围说明在输入表单之前，使用蓝色边框框样式
- 输入框使用 `step="any"` 避免精度限制
- 必填项使用红色星号 `<span class="required">*</span>`
- 标签页使用 `sub-tabs-container` 和 `sub-tab` 类

### 第六步：创建前端JavaScript

在 `static/js/tools/your_tool.js` 创建前端逻辑：

```javascript
/**
 * 工具名称 - 前端计算逻辑
 */

/**
 * 切换子标签页（如果有多标签）
 */
function switchSubTab(tabName) {
    // 隐藏所有标签内容
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // 移除所有子标签的active类
    const subTabs = document.querySelectorAll('.sub-tab');
    subTabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 显示选中的标签内容
    const targetContent = document.getElementById(tabName);
    if (targetContent) {
        targetContent.classList.add('active');
    }
    
    // 激活对应的子标签按钮
    subTabs.forEach(tab => {
        const onclick = tab.getAttribute('onclick');
        if (onclick && onclick.includes(tabName)) {
            tab.classList.add('active');
        }
    });
}

/**
 * 场景1计算
 */
async function calculateScenario1() {
    // 1. 获取输入值
    const param1Input = document.getElementById('param1').value.trim();
    const param2Input = document.getElementById('param2').value.trim();
    
    // 2. 验证输入
    if (param1Input === '') {
        showError('请输入参数1');
        return;
    }
    
    const param1 = parseFloat(param1Input);
    if (isNaN(param1)) {
        showError('参数1必须是有效数字');
        return;
    }
    if (param1 <= 0) {
        showError('参数1必须大于0');
        return;
    }
    
    // 类似验证param2...
    
    // 3. 构建请求参数
    const params = {
        scenario: 'scenario1',
        param1: param1,
        param2: param2
    };
    
    // 4. 调用API
    try {
        const result = await apiRequest('/api/tools/your-tool/calculate', 'POST', params);
        
        // 5. 显示结果
        document.getElementById('scenario1_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('scenario1_result_unit').textContent = result.unit;
        renderFormula('scenario1_result_formula', result.formula);
        document.getElementById('scenario1_result').style.display = 'block';
        
        // 6. 滚动到结果区域
        document.getElementById('scenario1_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}
```

**关键点**：
- 使用 `trim()` 处理输入
- 分别验证空值和数字有效性
- 使用 `apiRequest` 统一发送请求
- 使用 `renderFormula` 显示公式
- 使用 `showError` 显示错误（屏幕中间模态框）

### 第七步：注册工具

在 `app/main.py` 的 `tools_list` 中添加新工具：

```python
tools_list = [
    {"id": "current-calc", "name": "常用电流计算公式", "description": "..."},
    {"id": "inertia-calc", "name": "不同形状物体惯量计算", "description": "..."},
    {"id": "your-tool", "name": "工具名称", "description": "工具描述"},
]
```

### 第八步：验证公式

创建验证脚本 `scripts/verify_your_tool_formulas.py`：

```python
"""
验证工具名称计算公式的正确性
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.your_calculator import YourCalculator

def verify_scenario1():
    """验证场景1公式"""
    calculator = YourCalculator()
    
    test_cases = [
        {"param1": 100, "param2": 10, "expected": 1000},
        # 更多测试用例...
    ]
    
    for i, case in enumerate(test_cases, 1):
        result = calculator._calculate_scenario1(case)
        expected = case["expected"]
        actual = result.result
        status = "✓" if abs(actual - expected) < 0.0001 else "✗"
        print(f"测试 {i}: 期望={expected}, 实际={actual}, 状态={status}")

if __name__ == "__main__":
    verify_scenario1()
```

运行验证：

```bash
python3 scripts/verify_your_tool_formulas.py
```

### 第九步：测试和部署

```bash
# 1. 重启服务
sudo systemctl restart tool.w8.hk

# 2. 检查服务状态
sudo systemctl status tool.w8.hk

# 3. 测试页面
curl http://localhost:8000/tools/your-tool

# 4. 测试API
curl -X POST http://localhost:8000/api/tools/your-tool/calculate \
  -H "Content-Type: application/json" \
  -d '{"scenario": "scenario1", "param1": 100, "param2": 10}'
```

## 代码规范

### 后端规范

1. **计算服务类**：
   - 类名：`XxxCalculator`
   - 方法：`calculate(scenario, params)` 作为入口
   - 私有方法：`_calculate_scenario_name(params)` 处理具体计算
   - 公式字符串：使用多行格式，`<br>` 换行

2. **参数验证**：
   - 先检查 `None`
   - 再检查类型（`float()` 转换）
   - 最后检查范围（`> 0` 等）
   - 错误信息要详细，包含当前值

3. **响应格式**：
   - 使用 `CurrentCalcResponse` 统一格式
   - `result`: 计算结果（float）
   - `unit`: 单位（str）
   - `formula`: 公式字符串（支持HTML）
   - `scenario_name`: 场景名称（str）
   - `extra`: 额外信息（可选，Dict）

### 前端规范

1. **HTML结构**：
   - 继承 `base.html`
   - 使用统一的样式类
   - 参数说明表格使用 `reference-table` 样式
   - 输入框使用 `step="any"` 避免精度限制

2. **JavaScript函数**：
   - 使用 `async/await` 处理异步
   - 输入验证要完整（空值、NaN、范围）
   - 使用 `showError` 显示错误（屏幕中间模态框）
   - 使用 `renderFormula` 显示公式
   - 使用 `formatNumber` 格式化数字

3. **错误处理**：
   - 前端验证：用户友好的提示
   - 后端验证：详细的错误信息
   - 统一使用 `showError` 显示错误

## 样式规范

### 颜色方案

- 主色调：`#3498db` (蓝色)
- 成功色：`#27ae60` (绿色)
- 警告色：`#f39c12` (橙色)
- 错误色：`#e74c3c` (红色)
- 背景色：`#f5f5f5` (浅灰)
- 文字色：`#2c3e50` (深灰)
- 参数表格背景：`#e8f5e9` (浅绿)
- 参数表格边框：`#c8e6c9` (绿色边框)
- 分隔线颜色：`#4caf50` (绿色分隔线)

### 常用样式类

- `.page-header`: 页面标题
- `.tool-form`: 工具表单容器
- `.form-group`: 表单组
- `.formula-info`: 公式说明
- `.result-box`: 结果显示框
- `.result-value`: 结果数值
- `.result-formula`: 结果公式
- `.reference-table`: 参数说明表格
- `.required`: 必填项星号（红色）
- `.sub-tabs-container`: 标签页容器
- `.sub-tab`: 标签页按钮
- `.tab-content`: 标签页内容

### 标准布局结构

参考 `belt-intermittent` 工具的标准布局（https://tool.w8.hk/tools/belt-intermittent）：

```
1. 页面标题（page-header）
   ├─ 标题（h1）
   └─ 描述（subtitle）

2. 参数说明表格（reference-table）
   ├─ 3栏布局（grid-template-columns: 1fr 4px 1fr 4px 1fr）
   ├─ 绿色分隔线（#4caf50，宽度2px）
   └─ 底部必填项说明（红色文字）

3. 标签页导航（sub-tabs-container，如果多个计算模块）
   └─ 标签按钮（sub-tab）

4. 每个标签页内容（tab-content）
   ├─ 标题（h2）
   ├─ 公式说明（formula-info，在输入表单之前）
   ├─ 物理来源和适用范围说明（蓝色边框框，在输入表单之前）
   ├─ 输入表单（form-group）
   ├─ 计算按钮（btn btn-primary）
   └─ 结果显示区域（result-box）
```

**重要规则**：
- 公式说明和物理来源说明必须在输入表单之前
- 参数说明表格使用3栏布局，绿色分隔线
- 标签页用于组织多个计算模块
- 每个标签页内容独立，包含完整的输入和结果显示



## 安装和运行

### 1. 安装依赖

```bash
# 系统包
sudo apt install -y python3-fastapi python3-uvicorn python3-jinja2 python3-pydantic python3-openpyxl

# 或使用pip
pip install -r requirements.txt
```

### 2. 运行开发服务器

```bash
cd /home/ubuntu/workspace
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问应用

- **开发环境**: http://localhost:8000/
- **生产环境**: https://tool.w8.hk/
- **API文档**: https://tool.w8.hk/docs

### 4. 构建静态资源指纹

- 运行 `python scripts/fingerprint_static.py`，为 `static/js/tools/*.js` 生成指纹文件和 `static/manifest.json`
- 模板通过 `static_asset()` 读取 manifest，未生成时会自动回退到原始文件名
- 部署时同步 `static/manifest.json` 及指纹化后的脚本文件，便于前端缓存失效控制

## 部署配置

### Systemd服务

服务文件：`/etc/systemd/system/tool.w8.hk.service`

```ini
[Unit]
Description=Tool.w8.hk FastAPI Application
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/workspace
Environment="PATH=/home/ubuntu/workspace/venv/bin"
ExecStart=/home/ubuntu/workspace/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

管理命令：

```bash
# 启动服务
sudo systemctl start tool.w8.hk

# 停止服务
sudo systemctl stop tool.w8.hk

# 重启服务
sudo systemctl restart tool.w8.hk

# 查看状态
sudo systemctl status tool.w8.hk

# 开机自启
sudo systemctl enable tool.w8.hk
```

### Nginx反向代理

配置文件：`/etc/nginx/sites-available/tool.w8.hk`

```nginx
server {
    listen 80;
    server_name tool.w8.hk;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tool.w8.hk;

    ssl_certificate /etc/letsencrypt/live/tool.w8.hk/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tool.w8.hk/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/tool.w8.hk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL证书

使用Let's Encrypt：

```bash
sudo certbot --nginx -d tool.w8.hk
```

自动续期已配置在crontab中。

## 测试工具

### 公式验证

```bash
# 验证所有公式
python3 scripts/verify_screw_horizontal_formulas.py
python3 scripts/verify_inertia_formulas.py

# 对比Excel公式
python3 scripts/compare_formulas.py
```

### Excel分析

```bash
# 查看Excel内容
python3 scripts/view_excel.py data/文件名.xlsx

# 分析工作表
python3 scripts/analyze_excel.py data/文件名.xlsx "工作表名"
```

## 开发检查清单

添加新工具时，确保完成以下步骤：

- [ ] 分析Excel文件，提取公式和参数
- [ ] 创建后端计算服务类（`app/services/xxx_calculator.py`）
- [ ] 实现所有计算场景的方法
- [ ] 添加参数验证和错误处理
- [ ] 创建API请求模型（`app/routers/tools_api.py`）
- [ ] 添加API路由
- [ ] 添加页面路由（`app/routers/tools.py`）
- [ ] 创建HTML页面（`templates/tools/xxx.html`）
- [ ] 添加参数说明表格（如需要）
- [ ] 添加物理来源说明
- [ ] 创建前端JavaScript（`static/js/tools/xxx.js`）
- [ ] 实现输入验证
- [ ] 实现API调用和结果显示
- [ ] 在主页注册新工具（`app/main.py`）
- [ ] 创建验证脚本（`scripts/verify_xxx_formulas.py`）
- [ ] 运行验证，确保公式正确
- [ ] 测试页面和API
- [ ] 重启服务并验证

## 常见问题

## 打包分发

如果需要将当前项目打包成可交付的压缩包，可运行内置脚本生成包含源码、静态资源、模板及工具配置的 Zip 文件：

```bash
python3 scripts/package_app.py  # 默认输出到 dist/tool-app.zip

# 自定义输出路径
python3 scripts/package_app.py --output /tmp/tool-app.zip
```

打包时会排除 `__pycache__` 和 `.pyc` 文件，便于直接分发部署。

### 1. 公式显示不正确

- 检查公式字符串是否包含HTML标签（`<br>`, `<sub>`等，尤其是上下标）
- 确保 `renderFormula` 函数使用 `innerHTML` 而不是 `textContent`

### 2. 输入验证失败

- 检查输入框的 `step` 属性（应使用 `step="any"`）
- 检查前端验证逻辑（空值、NaN、范围）
- 检查后端参数模型定义

### 3. 参数传递失败

- 检查API请求模型是否包含所有参数
- 检查前端发送的参数名称是否匹配
- 查看服务器日志中的参数值

### 4. 服务无法启动

- 检查Python依赖是否安装
- 检查端口8000是否被占用
- 查看systemd日志：`sudo journalctl -u tool.w8.hk -f`

## 许可证

本项目仅供学习和参考使用。
