/**
 * 伺服电机参数计算
 */

// 监听轴类型变化，显示/隐藏倾斜角输入
document.addEventListener('DOMContentLoaded', function() {
    const axisTypeSelect = document.getElementById('axis_type');
    const thetaGroup = document.getElementById('theta_group');
    
    if (axisTypeSelect && thetaGroup) {
        axisTypeSelect.addEventListener('change', function() {
            if (this.value === '倾斜轴') {
                thetaGroup.style.display = 'block';
            } else {
                thetaGroup.style.display = 'none';
            }
        });
    }
});

/**
 * 计算伺服电机参数
 */
async function calculateServoMotorParams() {
    const params = {
        scenario: "servo_motor_params",
        axis_type: document.getElementById("axis_type").value,
        m: parseFloat(document.getElementById("m").value),
        mb: parseFloat(document.getElementById("mb").value) || 0,
        Fb: parseFloat(document.getElementById("Fb").value) || 0,
        d: parseFloat(document.getElementById("d").value),
        Pb: parseFloat(document.getElementById("Pb").value),
        l: parseFloat(document.getElementById("l").value),
        z: parseFloat(document.getElementById("z").value) || 1,
        J13: parseFloat(document.getElementById("J13").value) || 0,
        u: parseFloat(document.getElementById("u").value) || 0.1,
        Fc: parseFloat(document.getElementById("Fc").value) || 0,
        eta: parseFloat(document.getElementById("eta").value) || 0.9,
        V: parseFloat(document.getElementById("V").value),
        amax: parseFloat(document.getElementById("amax").value),
    };
    
    // 倾斜角（仅倾斜轴需要）
    if (params.axis_type === '倾斜轴') {
        params.theta = parseFloat(document.getElementById("theta").value) || 0;
    }
    
    // 电机参数（可选）
    const Jm = document.getElementById("Jm").value;
    if (Jm) {
        params.Jm = parseFloat(Jm);
    }
    
    const Ts = document.getElementById("Ts").value;
    if (Ts) {
        params.Ts = parseFloat(Ts);
    }
    
    const Tmax_motor = document.getElementById("Tmax_motor").value;
    if (Tmax_motor) {
        params.Tmax_motor = parseFloat(Tmax_motor);
    }
    
    const Nmax_motor = document.getElementById("Nmax_motor").value;
    if (Nmax_motor) {
        params.Nmax_motor = parseFloat(Nmax_motor);
    }
    
    // 验证必需参数
    const required = ["m", "d", "Pb", "l", "V", "amax"];
    for (const key of required) {
        if (!params[key] && params[key] !== 0) {
            alert(`请填写必需参数: ${key}`);
            return;
        }
    }
    
    try {
        const response = await fetch("/api/tools/servo-motor-params/calculate", {
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
        
        displayResult(data);
    } catch (error) {
        alert("计算错误: " + error.message);
        console.error("计算错误:", error);
    }
}

/**
 * 显示计算结果
 */
function displayResult(data) {
    const container = document.getElementById("result-container");
    const content = document.getElementById("result-content");
    
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
    
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">电机选型变量</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机一转移动量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">P</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.P.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">m/rev</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机最大转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.N}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rev/min</td></tr>`;
    
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">惯量</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">质量折算惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>11</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.J11.toFixed(5)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">丝杠折算惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>12</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.J12.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">其他惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>13</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.J13.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">负载惯量</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">J<sub>1</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.J1.toFixed(5)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">扭矩</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">摩擦扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>f</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tf.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">重力扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>g</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tg.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">空载扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>m</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tm.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">切削扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>c</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tc.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">负载扭矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>mc</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tmc.toFixed(4)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">加速扭矩</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">T<sub>max</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Tmax.toFixed(4)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    
    html += `</tbody></table>`;
    html += `</div>`;
    
    // 如果提供了电机参数，显示选型确认结果
    if (result.inertia_ratio !== undefined || result.no_load_ratio !== undefined || 
        result.load_ratio !== undefined || result.speed_judgment !== undefined || 
        result.accel_ratio !== undefined) {
        html += `<div style="margin-top: 2rem; padding: 1.5rem; background: #fff9e6; border-radius: 4px; border-left: 4px solid #f39c12;">`;
        html += `<h3 style="margin-top: 0; color: #2c3e50;">伺服电机选型确认</h3>`;
        html += `<table class="result-table" style="width: 100%; border-collapse: collapse; margin-top: 1rem;">`;
        html += `<thead><tr style="background: #f39c12; color: white;">`;
        html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #e67e22;">参数</th>`;
        html += `<th style="padding: 0.75rem; text-align: right; border: 1px solid #e67e22;">数值</th>`;
        html += `<th style="padding: 0.75rem; text-align: left; border: 1px solid #e67e22;">判定结论</th>`;
        html += `</tr></thead>`;
        html += `<tbody>`;
        
        if (result.inertia_ratio !== undefined) {
            const judgmentClass = result.inertia_judgment.includes('满足') ? 'color: #27ae60;' : 'color: #e74c3c;';
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">负载惯量比</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.inertia_ratio.toFixed(2)}%</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7; ${judgmentClass} font-weight: bold;">${result.inertia_judgment}</td></tr>`;
        }
        
        if (result.no_load_ratio !== undefined) {
            const judgmentClass = result.no_load_judgment.includes('满足') ? 'color: #27ae60;' : 'color: #e74c3c;';
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">空载扭矩比率</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.no_load_ratio.toFixed(2)}%</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7; ${judgmentClass} font-weight: bold;">${result.no_load_judgment}</td></tr>`;
        }
        
        if (result.load_ratio !== undefined) {
            const judgmentClass = result.load_judgment.includes('满足') ? 'color: #27ae60;' : 'color: #e74c3c;';
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">负载扭矩比率</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.load_ratio.toFixed(2)}%</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7; ${judgmentClass} font-weight: bold;">${result.load_judgment}</td></tr>`;
        }
        
        if (result.speed_judgment !== undefined) {
            const judgmentClass = result.speed_judgment.includes('满足') ? 'color: #27ae60;' : 'color: #e74c3c;';
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">最高转速</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">-</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7; ${judgmentClass} font-weight: bold;">${result.speed_judgment}</td></tr>`;
        }
        
        if (result.accel_ratio !== undefined) {
            const judgmentClass = result.accel_judgment.includes('满足') ? 'color: #27ae60;' : 'color: #e74c3c;';
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加速扭矩比率</td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.accel_ratio.toFixed(2)}%</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7; ${judgmentClass} font-weight: bold;">${result.accel_judgment}</td></tr>`;
        }
        
        html += `</tbody></table>`;
        html += `</div>`;
    }
    
    content.innerHTML = html;
    container.style.display = "block";
    container.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * 重置表单
 */
function resetForm() {
    document.getElementById("axis_type").value = "水平轴";
    document.getElementById("m").value = "500";
    document.getElementById("mb").value = "0";
    document.getElementById("Fb").value = "0";
    document.getElementById("d").value = "40";
    document.getElementById("Pb").value = "6";
    document.getElementById("l").value = "500";
    document.getElementById("z").value = "1";
    document.getElementById("J13").value = "0";
    document.getElementById("u").value = "0.1";
    document.getElementById("Fc").value = "0";
    document.getElementById("eta").value = "0.9";
    document.getElementById("theta").value = "0";
    document.getElementById("V").value = "8";
    document.getElementById("amax").value = "5";
    document.getElementById("Jm").value = "0.0023";
    document.getElementById("Ts").value = "11";
    document.getElementById("Tmax_motor").value = "15";
    document.getElementById("Nmax_motor").value = "3000";
    
    // 隐藏倾斜角输入
    document.getElementById("theta_group").style.display = "none";
    
    // 隐藏结果
    document.getElementById("result-container").style.display = "none";
}