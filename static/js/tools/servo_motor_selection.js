/**
 * 伺服电机选型计算
 */

/**
 * 切换标签页
 */
function switchSubTab(tabName) {
    // 隐藏所有标签页内容
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 显示选中的标签页内容
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // 更新标签按钮状态
    const tabButtons = document.querySelectorAll('.sub-tab');
    tabButtons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 激活对应的按钮
    event.target.classList.add('active');
}

/**
 * 计算直线电机选型
 */
async function calculateLinearMotor() {
    const params = {
        scenario: "linear_motor",
        a: parseFloat(document.getElementById("linear_a").value),
        V: parseFloat(document.getElementById("linear_V").value),
        S: parseFloat(document.getElementById("linear_S").value),
        Mt: parseFloat(document.getElementById("linear_Mt").value),
        Mf: parseFloat(document.getElementById("linear_Mf").value) || 0,
        mu: parseFloat(document.getElementById("linear_mu").value) || 0.2,
    };
    
    // 验证必需参数
    const required = ["a", "V", "S", "Mt"];
    for (const key of required) {
        if (!params[key] && params[key] !== 0) {
            alert(`请填写必需参数: ${key}`);
            return;
        }
    }
    
    try {
        const response = await fetch("/api/tools/servo-motor-selection/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(params),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "计算失败");
        }
        
        displayLinearResult(data);
    } catch (error) {
        alert("计算错误: " + error.message);
        console.error("计算错误:", error);
    }
}

/**
 * 显示直线电机计算结果
 */
function displayLinearResult(data) {
    const container = document.getElementById("linear_result-container");
    const content = document.getElementById("linear_result-content");
    
    if (!data.result) {
        content.innerHTML = "<p>计算结果为空</p>";
        container.style.display = "block";
        return;
    }
    
    const result = data.result;
    
    let html = "";
    
    // 显示公式
    if (data.formula) {
        html += `<div style="margin-bottom: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #3498db;">`;
        html += `<h3 style="margin-top: 0; color: #2c3e50;">计算过程</h3>`;
        html += `<div style="line-height: 1.8; color: #34495e;">${data.formula}</div>`;
        html += `</div>`;
    }
    
    // 显示结果表格
    html += `<div style="overflow-x: auto;">`;
    html += `<table class="result-table" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">`;
    html += `<thead><tr style="background: #3498db; color: white;">`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">参数</th>`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">符号</th>`;
    html += `<th style="padding: 0.75rem; text-align: right; border: 1px solid #2980b9;">数值</th>`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">单位</th>`;
    html += `</tr></thead>`;
    html += `<tbody>`;
    
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加减速阶段推力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>a</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Fa.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">匀速阶段推力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>v</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Fv.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加减速时间</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">t<sub>1</sub>=t<sub>3</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.t1.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">s</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">匀速运动时间</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">t<sub>2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.t2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">s</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">峰值推力（大于该值）</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">F<sub>p</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Fp.toFixed(2)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">有效推力（大于该值）</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">F<sub>c</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Fc.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">反电势常数（小于该值）</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">K<sub>e</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Ke.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">-</td></tr>`;
    
    html += `</tbody></table>`;
    html += `</div>`;
    
    content.innerHTML = html;
    container.style.display = "block";
    container.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * 计算旋转电机选型
 */
async function calculateRotaryMotor() {
    const params = {
        scenario: "rotary_motor",
        a: parseFloat(document.getElementById("rotary_a").value),
        V: parseFloat(document.getElementById("rotary_V").value),
        S: parseFloat(document.getElementById("rotary_S").value),
        Mt: parseFloat(document.getElementById("rotary_Mt").value),
        Mf: parseFloat(document.getElementById("rotary_Mf").value) || 0,
        mu: parseFloat(document.getElementById("rotary_mu").value) || 1,
        eta: parseFloat(document.getElementById("rotary_eta").value) || 0.9,
        PB: parseFloat(document.getElementById("rotary_PB").value),
        DB: parseFloat(document.getElementById("rotary_DB").value),
        MB: parseFloat(document.getElementById("rotary_MB").value) || 0,
    };
    
    // 验证必需参数
    const required = ["a", "V", "S", "Mt", "PB", "DB"];
    for (const key of required) {
        if (!params[key] && params[key] !== 0) {
            alert(`请填写必需参数: ${key}`);
            return;
        }
    }
    
    try {
        const response = await fetch("/api/tools/servo-motor-selection/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(params),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || "计算失败");
        }
        
        displayRotaryResult(data);
    } catch (error) {
        alert("计算错误: " + error.message);
        console.error("计算错误:", error);
    }
}

/**
 * 显示旋转电机计算结果
 */
function displayRotaryResult(data) {
    const container = document.getElementById("rotary_result-container");
    const content = document.getElementById("rotary_result-content");
    
    if (!data.result) {
        content.innerHTML = "<p>计算结果为空</p>";
        container.style.display = "block";
        return;
    }
    
    const result = data.result;
    
    let html = "";
    
    // 显示公式
    if (data.formula) {
        html += `<div style="margin-bottom: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #3498db;">`;
        html += `<h3 style="margin-top: 0; color: #2c3e50;">计算过程</h3>`;
        html += `<div style="line-height: 1.8; color: #34495e;">${data.formula}</div>`;
        html += `</div>`;
    }
    
    // 显示结果表格
    html += `<div style="overflow-x: auto;">`;
    html += `<table class="result-table" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">`;
    html += `<thead><tr style="background: #3498db; color: white;">`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">参数</th>`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">符号</th>`;
    html += `<th style="padding: 0.75rem; text-align: right; border: 1px solid #2980b9;">数值</th>`;
    html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #2980b9;">单位</th>`;
    html += `</tr></thead>`;
    html += `<tbody>`;
    
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">惯量和转速</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">工作台转动惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>a</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Ja.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">丝杆转动惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>b</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Jb.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.N.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rpm</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加减速时间</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">t<sub>1</sub>=t<sub>3</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.t1.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">s</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">匀速移动时间</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">t<sub>2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.t2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">s</td></tr>`;
    
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">扭矩</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加速扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>A</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.TA.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">匀速扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>B</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.TB.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">减速扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>C</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.TC.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">峰值扭矩（大于该值）</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">T<sub>max</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Tmax.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">时效扭矩（大于该值）</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">T<sub>rmsx</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Trmsx.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">额定扭矩（大于该值）</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">T<sub>f</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Tf.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">转子惯量（大于该值）</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>A</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.JA.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">×10⁻⁴ kg·m²</td></tr>`;
    
    html += `</tbody></table>`;
    html += `</div>`;
    
    content.innerHTML = html;
    container.style.display = "block";
    container.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * 重置直线电机表单
 */
function resetLinearForm() {
    document.getElementById("linear_a").value = "11";
    document.getElementById("linear_V").value = "80";
    document.getElementById("linear_S").value = "700";
    document.getElementById("linear_Mt").value = "300";
    document.getElementById("linear_Mf").value = "20";
    document.getElementById("linear_mu").value = "0.2";
    document.getElementById("linear_result-container").style.display = "none";
}

/**
 * 重置旋转电机表单
 */
function resetRotaryForm() {
    document.getElementById("rotary_a").value = "5";
    document.getElementById("rotary_V").value = "15";
    document.getElementById("rotary_S").value = "50";
    document.getElementById("rotary_Mt").value = "150";
    document.getElementById("rotary_Mf").value = "0";
    document.getElementById("rotary_mu").value = "1";
    document.getElementById("rotary_eta").value = "0.9";
    document.getElementById("rotary_PB").value = "5";
    document.getElementById("rotary_DB").value = "20";
    document.getElementById("rotary_MB").value = "0.64";
    document.getElementById("rotary_result-container").style.display = "none";
}

