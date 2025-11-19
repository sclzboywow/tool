/**
 * 鼓风机选型计算 - 前端计算逻辑
 */

/**
 * 计算鼓风机选型
 */
async function calculateBlowerSelection() {
    // 获取输入参数
    const params = {
        scenario: "blower_selection",
        Pd: parseFloat(document.getElementById('Pd').value),
        delta_P1: parseFloat(document.getElementById('delta_P1').value),
        delta_Pf: parseFloat(document.getElementById('delta_Pf').value),
        P0: parseFloat(document.getElementById('P0').value),
        delta_Px: parseFloat(document.getElementById('delta_Px').value) || 0,
        Vu: parseFloat(document.getElementById('Vu').value),
        i: parseFloat(document.getElementById('i').value),
        q: parseFloat(document.getElementById('q').value),
        delta: parseFloat(document.getElementById('delta').value),
        Qf: parseFloat(document.getElementById('Qf').value) || 0,
        PX: parseFloat(document.getElementById('PX').value),
        T0: parseFloat(document.getElementById('T0').value),
        Ta: parseFloat(document.getElementById('Ta').value),
        PZ: parseFloat(document.getElementById('PZ').value),
        Pa: parseFloat(document.getElementById('Pa').value),
        k: parseFloat(document.getElementById('k').value),
        eta_n: parseFloat(document.getElementById('eta_n').value),
        eta_m: parseFloat(document.getElementById('eta_m').value)
    };
    
    // 验证必需参数
    const requiredFields = ['Pd', 'delta_P1', 'delta_Pf', 'P0', 'Vu', 'i', 'q', 'delta', 'PX', 'T0', 'Ta', 'PZ', 'Pa', 'k', 'eta_n', 'eta_m'];
    for (const field of requiredFields) {
        if (params[field] === undefined || params[field] === null || isNaN(params[field])) {
            alert(`请填写所有必填项，${field} 不能为空`);
            return;
        }
    }
    
    // 验证参数范围
    if (params.P0 <= 0) {
        alert('标准大气压P0必须大于0');
        return;
    }
    if (params.Vu <= 0) {
        alert('高炉有效容积Vu必须大于0');
        return;
    }
    if (params.i <= 0) {
        alert('高炉利用系数i必须大于0');
        return;
    }
    if (params.q <= 0) {
        alert('单位生铁耗风量q必须大于0');
        return;
    }
    if (params.delta < 0 || params.delta > 100) {
        alert('高炉漏风率delta应在0-100%之间');
        return;
    }
    if (params.T0 <= 0) {
        alert('标准温度T0必须大于0');
        return;
    }
    if (params.Ta <= 0) {
        alert('风机入口实际温度Ta必须大于0');
        return;
    }
    if (params.PX <= 0) {
        alert('风机入口实际大气压PX必须大于0');
        return;
    }
    if (params.Pa <= 0) {
        alert('风机入口大气压Pa必须大于0');
        return;
    }
    if (params.k <= 1) {
        alert('绝热指数k必须大于1');
        return;
    }
    if (params.eta_n <= 0 || params.eta_n > 1) {
        alert('内效率eta_n应在0-1之间');
        return;
    }
    if (params.eta_m <= 0 || params.eta_m > 1) {
        alert('机械效率eta_m应在0-1之间');
        return;
    }
    
    try {
        // 调用API
        const response = await fetch('/api/tools/blower-selection/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '计算失败');
        }
        
        const result = await response.json();
        displayResult(result);
    } catch (error) {
        alert('计算错误: ' + error.message);
        console.error('计算错误:', error);
    }
}

/**
 * 显示计算结果
 */
function displayResult(result) {
    const container = document.getElementById('result-container');
    const content = document.getElementById('result-content');
    
    if (!result.result || typeof result.result !== 'object') {
        content.innerHTML = '<p style="color: #e74c3c;">计算结果格式错误</p>';
        container.style.display = 'block';
        return;
    }
    
    const data = result.result;
    
    // 构建结果HTML
    let html = '<div class="result-table">';
    html += '<table style="width: 100%; border-collapse: collapse; margin-top: 1rem;">';
    html += '<thead><tr style="background: #3498db; color: white;"><th style="padding: 0.75rem; text-align: left;">参数</th><th style="padding: 0.75rem; text-align: right;">数值</th><th style="padding: 0.75rem; text-align: left;">单位</th></tr></thead>';
    html += '<tbody>';
    
    // 压力相关结果
    html += '<tr style="background: #ecf0f1;"><td colspan="3" style="padding: 0.5rem; font-weight: bold;">压力参数</td></tr>';
    html += `<tr><td style="padding: 0.5rem;">高炉所需风压 P<sub>c</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Pc.toFixed(6)}</td><td style="padding: 0.5rem;">MPa</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">风机入口压力 P<sub>fx</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Pfx.toFixed(6)}</td><td style="padding: 0.5rem;">MPa</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">风机出口风压 P<sub>h</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Ph.toFixed(6)}</td><td style="padding: 0.5rem;">MPa</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">压比 ε</td><td style="padding: 0.5rem; text-align: right;">${data.epsilon.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    
    // 风量相关结果
    html += '<tr style="background: #ecf0f1;"><td colspan="3" style="padding: 0.5rem; font-weight: bold;">风量参数</td></tr>';
    html += `<tr><td style="padding: 0.5rem;">高炉入炉风量 Q<sub>g</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Qg.toFixed(2)}</td><td style="padding: 0.5rem;">m³/h</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">风机出口风量1 Q<sub>2</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Q2.toFixed(2)}</td><td style="padding: 0.5rem;">m³/h</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">风机出口风量2 Q<sub>3</sub></td><td style="padding: 0.5rem; text-align: right;">${data.Q3.toFixed(2)}</td><td style="padding: 0.5rem;">m³/h</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">实际送风量 Q</td><td style="padding: 0.5rem; text-align: right;">${data.Q.toFixed(2)}</td><td style="padding: 0.5rem;">m³/min</td></tr>`;
    
    // 修正系数
    html += '<tr style="background: #ecf0f1;"><td colspan="3" style="padding: 0.5rem; font-weight: bold;">修正系数</td></tr>';
    html += `<tr><td style="padding: 0.5rem;">气压修正系数 K<sub>1</sub></td><td style="padding: 0.5rem; text-align: right;">${data.K1.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">气温修正系数 K<sub>2</sub></td><td style="padding: 0.5rem; text-align: right;">${data.K2.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">湿度修正系数 K<sub>3</sub></td><td style="padding: 0.5rem; text-align: right;">${data.K3.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">风量修正系数 K</td><td style="padding: 0.5rem; text-align: right;">${data.K.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    
    // 功率
    html += '<tr style="background: #ecf0f1;"><td colspan="3" style="padding: 0.5rem; font-weight: bold;">功率参数</td></tr>';
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold;">鼓风机轴功率 N<sub>e</sub></td><td style="padding: 0.5rem; text-align: right; font-weight: bold; font-size: 1.1em; color: #e74c3c;">${data.Ne.toFixed(2)}</td><td style="padding: 0.5rem; font-weight: bold;">kW</td></tr>`;
    
    html += '</tbody></table>';
    html += '</div>';
    
    // 显示公式
    if (result.formula) {
        html += '<div style="margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 4px; border-left: 4px solid #3498db;">';
        html += '<h3 style="margin-top: 0; color: #2c3e50;">计算过程</h3>';
        html += '<div style="line-height: 1.8; color: #34495e;">' + result.formula + '</div>';
        html += '</div>';
    }
    
    content.innerHTML = html;
    container.style.display = 'block';
    
    // 滚动到结果区域
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * 重置表单
 */
function resetForm() {
    document.getElementById('Pd').value = '0.2';
    document.getElementById('delta_P1').value = '0.15';
    document.getElementById('delta_Pf').value = '0.03';
    document.getElementById('P0').value = '0.101325';
    document.getElementById('delta_Px').value = '0.003';
    document.getElementById('Vu').value = '1350';
    document.getElementById('i').value = '1.26';
    document.getElementById('q').value = '2400';
    document.getElementById('delta').value = '3';
    document.getElementById('Qf').value = '300';
    document.getElementById('PX').value = '99770';
    document.getElementById('T0').value = '273';
    document.getElementById('Ta').value = '308';
    document.getElementById('PZ').value = '5157';
    document.getElementById('Pa').value = '102770';
    document.getElementById('k').value = '1.4';
    document.getElementById('eta_n').value = '0.98';
    document.getElementById('eta_m').value = '0.95';
    
    document.getElementById('result-container').style.display = 'none';
}

