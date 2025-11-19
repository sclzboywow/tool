/**
 * 风机选型计算举例（锅炉送风机选型）
 */

/**
 * 计算
 */
async function calculate() {
    // 获取输入参数
    const params = {
        scenario: "fan_selection_example",
        // 煤质参数
        Car: parseFloat(document.getElementById("Car").value),
        OAR: parseFloat(document.getElementById("OAR").value),
        Hy: parseFloat(document.getElementById("Hy").value),
        Nar: parseFloat(document.getElementById("Nar").value),
        War: parseFloat(document.getElementById("War").value),
        Aar: parseFloat(document.getElementById("Aar").value),
        Sar: parseFloat(document.getElementById("Sar").value),
        Qnet_ar: parseFloat(document.getElementById("Qnet_ar").value),
    };
    
    // 燃煤量（如果提供）
    const B = document.getElementById("B").value;
    if (B && B.trim() !== "") {
        params.B = parseFloat(B);
    } else {
        // 通过锅炉参数计算
        const D = document.getElementById("D").value;
        const h_main = document.getElementById("h_main").value;
        const h_feed = document.getElementById("h_feed").value;
        if (D && h_main && h_feed) {
            params.D = parseFloat(D);
            params.h_main = parseFloat(h_main);
            params.h_feed = parseFloat(h_feed);
            const blowdown = document.getElementById("blowdown").value;
            if (blowdown) params.blowdown = parseFloat(blowdown);
            const h_blowdown = document.getElementById("h_blowdown").value;
            if (h_blowdown) params.h_blowdown = parseFloat(h_blowdown);
            const eta_boiler = document.getElementById("eta_boiler").value;
            if (eta_boiler) params.eta_boiler = parseFloat(eta_boiler);
        }
    }
    
    // 其他参数
    const alpha = document.getElementById("alpha").value;
    if (alpha) params.alpha = parseFloat(alpha);
    
    const tk = document.getElementById("tk").value;
    if (tk) params.tk = parseFloat(tk);
    
    const tg = document.getElementById("tg").value;
    if (tg) params.tg = parseFloat(tg);
    
    const b = document.getElementById("b").value;
    if (b) params.b = parseFloat(b);
    
    const k1 = document.getElementById("k1").value;
    if (k1) params.k1 = parseFloat(k1);
    
    const k2_primary = document.getElementById("k2_primary").value;
    if (k2_primary) params.k2_primary = parseFloat(k2_primary);
    
    const k2_secondary = document.getElementById("k2_secondary").value;
    if (k2_secondary) params.k2_secondary = parseFloat(k2_secondary);
    
    const delta_h_primary = document.getElementById("delta_h_primary").value;
    if (delta_h_primary) params.delta_h_primary = parseFloat(delta_h_primary);
    
    const delta_h_secondary = document.getElementById("delta_h_secondary").value;
    if (delta_h_secondary) params.delta_h_secondary = parseFloat(delta_h_secondary);
    
    const eta1 = document.getElementById("eta1").value;
    if (eta1) params.eta1 = parseFloat(eta1);
    
    const eta2 = document.getElementById("eta2").value;
    if (eta2) params.eta2 = parseFloat(eta2);
    
    const eta3 = document.getElementById("eta3").value;
    if (eta3) params.eta3 = parseFloat(eta3);
    
    const K_motor = document.getElementById("K_motor").value;
    if (K_motor) params.K_motor = parseFloat(K_motor);
    
    const rho_ko = document.getElementById("rho_ko").value;
    if (rho_ko) params.rho_ko = parseFloat(rho_ko);
    
    // 验证必需参数
    const required = ["Car", "OAR", "Hy", "Nar", "War", "Aar", "Sar", "Qnet_ar", "b"];
    for (const key of required) {
        if (!params[key] && params[key] !== 0) {
            alert(`请填写必需参数: ${key}`);
            return;
        }
    }
    
    if (!params.B && (!params.D || !params.h_main || !params.h_feed)) {
        alert("请提供燃煤量B，或提供计算燃煤量所需的参数(D, h_main, h_feed)");
        return;
    }
    
    if (!params.delta_h_primary || !params.delta_h_secondary) {
        alert("请填写一次风机和二次风机的总阻力");
        return;
    }
    
    try {
        // 调用API
        const response = await fetch("/api/tools/fan-selection-example/calculate", {
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
    
    // 燃烧空气量和烟气量
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">燃烧空气量和烟气量</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">燃烧空气量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>o</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vo.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">CO<sub>2</sub>和SO<sub>2</sub>产生量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>RO2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.VRO2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">含氮量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>N2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.VN2.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">理论水蒸气含量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>H2Oo</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.VH2Oo.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">理论烟气量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>yo</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vyo.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">实际烟气量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>y</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vy.toFixed(6)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Nm³/kg</td></tr>`;
    
    // 送风机风量
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">送风机风量</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">送风机总风量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>g</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vg.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">m³/h</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">一次风量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>g1</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vg_primary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">m³/h</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">二次风量</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">V<sub>g2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Vg_secondary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">m³/h</td></tr>`;
    
    // 送风机阻力
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">送风机阻力</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">一次风机阻力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">H<sub>g1</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Hg_primary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Pa</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">二次风机阻力</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">H<sub>g2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Hg_secondary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">Pa</td></tr>`;
    
    // 电动机功率
    html += `<tr><td colspan="4" style="padding: 0.5rem; background: #ecf0f1; font-weight: bold; border: 1px solid #bdc3c7;">电动机功率</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">一次风机电动机功率</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N<sub>g1</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Ng_primary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kW</td></tr>`;
    html += `<tr><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">二次风机电动机功率</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">N<sub>g2</sub></td><td style="padding: 0.5rem; text-align: right; border: 1px solid #bdc3c7;">${result.Ng_secondary.toFixed(2)}</td><td style="padding: 0.5rem; border: 1px solid #bdc3c7;">kW</td></tr>`;
    
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
    document.getElementById("Car").value = "43.83";
    document.getElementById("OAR").value = "21.51";
    document.getElementById("Hy").value = "4.39";
    document.getElementById("Nar").value = "0.72";
    document.getElementById("War").value = "5.35";
    document.getElementById("Aar").value = "24.02";
    document.getElementById("Sar").value = "0.18";
    document.getElementById("Qnet_ar").value = "16929";
    document.getElementById("B").value = "";
    document.getElementById("D").value = "90";
    document.getElementById("h_main").value = "3500";
    document.getElementById("h_feed").value = "947";
    document.getElementById("blowdown").value = "0.02";
    document.getElementById("h_blowdown").value = "1491";
    document.getElementById("eta_boiler").value = "0.89";
    document.getElementById("alpha").value = "1.2";
    document.getElementById("tk").value = "20";
    document.getElementById("tg").value = "20";
    document.getElementById("b").value = "89.515";
    document.getElementById("k1").value = "1.15";
    document.getElementById("k2_primary").value = "1.2";
    document.getElementById("k2_secondary").value = "1.25";
    document.getElementById("delta_h_primary").value = "16100";
    document.getElementById("delta_h_secondary").value = "8315";
    document.getElementById("eta1").value = "0.85";
    document.getElementById("eta2").value = "0.98";
    document.getElementById("eta3").value = "0.9";
    document.getElementById("K_motor").value = "1.1";
    document.getElementById("rho_ko").value = "1.293";
    
    document.getElementById("result-container").style.display = "none";
}

