/**
 * 伺服电机惯量计算（齿轮齿条传动）
 */

/**
 * 计算
 */
async function calculate() {
    // 获取输入参数
    const params = {
        scenario: "servo_motor_inertia",
        M: parseFloat(document.getElementById("M").value),
        v_fast: parseFloat(document.getElementById("v_fast").value),
        t_acc: parseFloat(document.getElementById("t_acc").value),
        a: parseFloat(document.getElementById("a").value),
        u: parseFloat(document.getElementById("u").value) || 0.1,
        m_gear: parseFloat(document.getElementById("m_gear").value),
        Z: parseFloat(document.getElementById("Z").value),
        D: parseFloat(document.getElementById("D").value),
        eta: parseFloat(document.getElementById("eta").value) || 0.98,
        i: parseFloat(document.getElementById("i").value),
        eta_reducer: parseFloat(document.getElementById("eta_reducer").value) || 0.8,
        Jm: parseFloat(document.getElementById("Jm").value),
        JG: parseFloat(document.getElementById("JG").value) || 0,
        Jg: parseFloat(document.getElementById("Jg").value) || 0,
        is_vertical: document.getElementById("is_vertical").value === "true",
        g: parseFloat(document.getElementById("g").value) || 9.8,
    };
    
    // 用于惯量匹配的Jm（可选）
    const Jm_inertia = document.getElementById("Jm_inertia").value;
    if (Jm_inertia) {
        params.Jm_inertia = parseFloat(Jm_inertia);
    }
    
    // 侧倾力矩计算参数（可选）
    const an = document.getElementById("an").value;
    if (an) params.an = parseFloat(an);
    
    const a0 = document.getElementById("a0").value;
    if (a0) params.a0 = parseFloat(a0);
    
    const Z2 = document.getElementById("Z2").value;
    if (Z2) params.Z2 = parseFloat(Z2);
    
    const X2 = document.getElementById("X2").value;
    if (X2) params.X2 = parseFloat(X2);
    
    const y2 = document.getElementById("y2").value;
    if (y2) params.y2 = parseFloat(y2);
    
    // 切削参数（可选）
    const FC = document.getElementById("FC").value;
    if (FC && FC.trim() !== "") {
        params.FC = parseFloat(FC);
    }
    
    const v_cut = document.getElementById("v_cut").value;
    if (v_cut && v_cut.trim() !== "") {
        params.v_cut = parseFloat(v_cut);
    }
    
    // 验证必需参数
    const required = ["M", "v_fast", "t_acc", "a", "m_gear", "Z", "D", "i", "Jm"];
    for (const key of required) {
        if (!params[key] && params[key] !== 0) {
            alert(`请填写必需参数: ${key}`);
            return;
        }
    }
    
    try {
        // 调用API
        const response = await fetch("/api/tools/servo-motor-inertia/calculate", {
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
        
        // 显示结果
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
    
    // 快速移动时
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">快速移动时</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">加速力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>a</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Fa.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">摩擦力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>f</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Ff.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">合力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>total</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.F_total.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">齿轮最高转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">n<sub>1</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.n1.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rpm</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">齿轮角加速度</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">β<sub>G</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.beta_G.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rad/s²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">合力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>req</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Treq.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">减速机输入端的加速力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.T2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机最大转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">n<sub>2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.n2.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rpm</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机角加速度</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">β<sub>m</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.beta_m.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rad/s²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机克服自身惯量加速的力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>m</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tm.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">电机在加速时总的输出力矩</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">T<sub>m1</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c; border: 1px solid #bdc3c7;">${result.Tm1.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    
    // 切削时（如果有）
    if (result.Fc !== undefined) {
        html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">切削时</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">切削抗力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>c</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Fc.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">合力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>cut</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.F_cut.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>c</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Tc.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机输出端的额定力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">T<sub>3</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.T3.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
        if (result.n_cut !== undefined) {
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">对应的齿轮转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">n<sub>cut</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.n_cut.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rpm</td></tr>`;
            html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">电机转速</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">n<sub>motor_cut</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.n_motor_cut.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">rpm</td></tr>`;
        }
    }
    
    // 侧倾力矩
    if (result.F2rmax !== undefined) {
        html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">侧倾力矩计算</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">最大水平切向力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>tangential</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.F_tangential.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">最大径向力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>2rmax</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.F2rmax.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">最大轴向力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">F<sub>2amax</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.F2amax.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N</td></tr>`;
        html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">侧倾力矩</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">M<sub>2Kmax</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.M2Kmax.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N·m</td></tr>`;
    }
    
    // 惯量匹配
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">惯量匹配</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">负载惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>L</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.JL.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">折算到减速机输入端的惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>1</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.J1.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">折算到电机输出端的惯量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">J<sub>2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.J2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kg·m²</td></tr>`;
    html += `<tr style="background: ${result.lambda_inertia > 10 ? '#ffebee' : '#e8f5e9'};"><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">惯量匹配值</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">λ</td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: ${result.lambda_inertia > 10 ? '#e74c3c' : '#27ae60'}; border: 1px solid #bdc3c7;">${result.lambda_inertia.toFixed(6)}</td><td style="padding: 0.5rem; font-weight: bold; border: 1px solid #bdc3c7;">-</td></tr>`;
    if (result.lambda_inertia > 10) {
        html += `<tr><td colspan="4" style="padding: 0.5rem; color: #e74c3c; border: 1px solid #bdc3c7;">⚠ 警告: 惯量匹配值λ > 10，建议重新选型</td></tr>`;
    }
    
    html += `</tbody></table>`;
    html += `</div>`;
    
    content.innerHTML = html;
    container.style.display = "block";
    
    // 滚动到结果区域
    container.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * 重置表单
 */
function resetForm() {
    document.getElementById("M").value = "2000";
    document.getElementById("v_fast").value = "50";
    document.getElementById("t_acc").value = "1";
    document.getElementById("a").value = "10";
    document.getElementById("u").value = "0.1";
    document.getElementById("is_vertical").value = "false";
    document.getElementById("FC").value = "0";
    document.getElementById("v_cut").value = "0";
    document.getElementById("m_gear").value = "3";
    document.getElementById("Z").value = "20";
    document.getElementById("D").value = "0.06048";
    document.getElementById("eta").value = "0.98";
    document.getElementById("JG").value = "0";
    document.getElementById("i").value = "16";
    document.getElementById("eta_reducer").value = "0.8";
    document.getElementById("Jm").value = "0.0036";
    document.getElementById("Jm_inertia").value = "0.0061";
    document.getElementById("Jg").value = "0.0006";
    document.getElementById("g").value = "9.8";
    document.getElementById("an").value = "21.116";
    document.getElementById("a0").value = "19.5283";
    document.getElementById("Z2").value = "0.0812";
    document.getElementById("X2").value = "15.5";
    document.getElementById("y2").value = "0.089127";
    
    document.getElementById("result-container").style.display = "none";
}

