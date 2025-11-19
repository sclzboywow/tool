/**
 * 风机选型计算 - 前端计算逻辑
 */

let performancePoints = [];
let pressureEfficiencyChart = null;
let pressurePowerChart = null;

// 初始化：页面加载时不自动添加性能点，让用户选择是否添加
document.addEventListener('DOMContentLoaded', function() {
    // 可以在这里添加初始化逻辑
});

/**
 * 添加性能点
 */
function addPerformancePoint(phi = '', psi_p = '', eta = '') {
    const container = document.getElementById('performance-points-container');
    const pointIndex = performancePoints.length;
    
    const pointDiv = document.createElement('div');
    pointDiv.className = 'performance-point';
    pointDiv.id = `point-${pointIndex}`;
    pointDiv.style.cssText = 'display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 1rem; align-items: end; margin-bottom: 1rem; padding: 1rem; background: #f8f9fa; border-radius: 4px;';
    
    pointDiv.innerHTML = `
        <div class="form-group">
            <label>流量系数 φ <span class="required">*</span></label>
            <input type="number" class="phi-input" step="0.0001" value="${phi}" placeholder="例如: 0.2231">
        </div>
        <div class="form-group">
            <label>压力系数 ψ<sub>p</sub> <span class="required">*</span></label>
            <input type="number" class="psi-p-input" step="0.0001" value="${psi_p}" placeholder="例如: 0.43">
        </div>
        <div class="form-group">
            <label>效率 η (%) <span class="required">*</span></label>
            <input type="number" class="eta-input" step="0.1" min="0" max="100" value="${eta}" placeholder="例如: 87.6">
        </div>
        <button type="button" class="remove-point-btn" onclick="removePerformancePoint(${pointIndex})" style="padding: 0.5rem 1rem; background: #e74c3c; color: white; border: none; border-radius: 4px; cursor: pointer;">删除</button>
    `;
    
    container.appendChild(pointDiv);
    performancePoints.push({ phi, psi_p, eta });
}

/**
 * 删除性能点
 */
function removePerformancePoint(index) {
    const pointDiv = document.getElementById(`point-${index}`);
    if (pointDiv) {
        pointDiv.remove();
        performancePoints.splice(index, 1);
        updatePerformancePointsIndex();
    }
}

/**
 * 更新性能点索引
 */
function updatePerformancePointsIndex() {
    const container = document.getElementById('performance-points-container');
    const points = container.querySelectorAll('.performance-point');
    performancePoints = [];
    
    points.forEach((pointDiv, index) => {
        pointDiv.id = `point-${index}`;
        const removeBtn = pointDiv.querySelector('.remove-point-btn');
        if (removeBtn) {
            removeBtn.setAttribute('onclick', `removePerformancePoint(${index})`);
        }
        
        const phi_input = pointDiv.querySelector('.phi-input');
        const psi_p_input = pointDiv.querySelector('.psi-p-input');
        const eta_input = pointDiv.querySelector('.eta-input');
        
        if (phi_input && psi_p_input && eta_input) {
            const phi = phi_input.value ? parseFloat(phi_input.value) : '';
            const psi_p = psi_p_input.value ? parseFloat(psi_p_input.value) : '';
            const eta = eta_input.value ? parseFloat(eta_input.value) : '';
            
            performancePoints.push({ phi, psi_p, eta });
        }
    });
}

/**
 * 清空所有性能点
 */
function clearPerformancePoints() {
    const container = document.getElementById('performance-points-container');
    container.innerHTML = '';
    performancePoints = [];
}

/**
 * 计算风机选型
 */
async function calculateFanSelection() {
    // 获取输入参数
    const Q = parseFloat(document.getElementById('Q').value);
    const P = parseFloat(document.getElementById('P').value);
    const H = parseFloat(document.getElementById('H').value) || 0;
    const P_inlet = parseFloat(document.getElementById('P_inlet').value) || 0;
    const T = parseFloat(document.getElementById('T').value);
    const k = parseFloat(document.getElementById('k').value) || 1.4;
    const n = parseFloat(document.getElementById('n').value);
    const fan_type = document.getElementById('fan_type').value;
    const D = parseFloat(document.getElementById('D').value);
    const suction_type = document.getElementById('suction_type').value;
    const rho_standard = parseFloat(document.getElementById('rho_standard').value) || 1.2;
    
    // 验证必需参数
    if (!Q || Q <= 0) {
        alert('请输入流量Q（必须大于0）');
        return;
    }
    if (!P || P <= 0) {
        alert('请输入全压P（必须大于0）');
        return;
    }
    if (T === undefined || T === null || isNaN(T)) {
        alert('请输入工作温度T');
        return;
    }
    if (!n || n <= 0) {
        alert('请输入工作转速n（必须大于0）');
        return;
    }
    if (!fan_type) {
        alert('请选择风机型号');
        return;
    }
    if (!D || D <= 0) {
        alert('请输入叶轮直径D（必须大于0）');
        return;
    }
    if (k <= 1) {
        alert('绝热指数k必须大于1');
        return;
    }
    
    // 收集性能点数据（如果提供）
    updatePerformancePointsIndex();
    let performance_points = null;
    if (performancePoints.length > 0) {
        // 验证性能点数据
        for (let i = 0; i < performancePoints.length; i++) {
            const point = performancePoints[i];
            if (!point.phi || !point.psi_p || !point.eta) {
                alert(`性能点${i + 1}的数据不完整，请填写所有字段`);
                return;
            }
            if (point.eta < 0 || point.eta > 100) {
                alert(`性能点${i + 1}的效率η应在0-100%之间`);
                return;
            }
        }
        performance_points = performancePoints.map(p => ({
            phi: parseFloat(p.phi),
            psi_p: parseFloat(p.psi_p),
            eta: parseFloat(p.eta)
        }));
    }
    
    const params = {
        scenario: "fan_selection",
        Q: Q,
        P: P,
        H: H,
        P_inlet: P_inlet,
        T: T,
        k: k,
        n: n,
        fan_type: fan_type,
        D: D,
        suction_type: suction_type,
        rho_standard: rho_standard
    };
    
    if (performance_points) {
        params.performance_points = performance_points;
    }
    
    try {
        // 调用API
        const response = await fetch('/api/tools/fan-selection/calculate', {
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
    
    // 中间结果
    html += '<h3 style="margin-top: 0; color: #2c3e50;">中间计算结果</h3>';
    html += '<table style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">';
    html += '<thead><tr style="background: #3498db; color: white;"><th style="padding: 0.75rem; text-align: left;">参数</th><th style="padding: 0.75rem; text-align: right;">数值</th><th style="padding: 0.75rem; text-align: left;">单位</th></tr></thead>';
    html += '<tbody>';
    html += `<tr><td style="padding: 0.5rem;">当地大气压 P<sub>atm</sub></td><td style="padding: 0.5rem; text-align: right;">${data.P_atm.toFixed(2)}</td><td style="padding: 0.5rem;">Pa</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">工况密度 ρ<sub>working</sub></td><td style="padding: 0.5rem; text-align: right;">${data.rho_working.toFixed(6)}</td><td style="padding: 0.5rem;">kg/m³</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">压缩性系数 Z</td><td style="padding: 0.5rem; text-align: right;">${data.Z.toFixed(6)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">比转数 n<sub>s</sub></td><td style="padding: 0.5rem; text-align: right;">${data.ns.toFixed(2)}</td><td style="padding: 0.5rem;">-</td></tr>`;
    html += `<tr><td style="padding: 0.5rem;">线速度 u</td><td style="padding: 0.5rem; text-align: right;">${data.u.toFixed(2)}</td><td style="padding: 0.5rem;">m/s</td></tr>`;
    if (data.D_rough) {
        html += `<tr><td style="padding: 0.5rem;">粗算叶轮直径 D<sub>rough</sub></td><td style="padding: 0.5rem; text-align: right;">${data.D_rough.toFixed(4)}</td><td style="padding: 0.5rem;">m</td></tr>`;
    }
    html += `<tr style="background: #fff3cd;"><td style="padding: 0.5rem; font-weight: bold;">选型结果</td><td style="padding: 0.5rem; text-align: right; font-weight: bold; color: #e74c3c;">${data.fan_model}</td><td style="padding: 0.5rem;"></td></tr>`;
    html += '</tbody></table>';
    
    // 性能点结果
    if (data.performance_points && data.performance_points.length > 0) {
        html += '<h3 style="color: #2c3e50;">性能点计算结果</h3>';
        html += '<table style="width: 100%; border-collapse: collapse; margin-bottom: 2rem;">';
        html += '<thead><tr style="background: #3498db; color: white;">';
        html += '<th style="padding: 0.75rem; text-align: center;">序号</th>';
        html += '<th style="padding: 0.75rem; text-align: right;">流量 Q (m³/h)</th>';
        html += '<th style="padding: 0.75rem; text-align: right;">全压 P (Pa)</th>';
        html += '<th style="padding: 0.75rem; text-align: right;">内效率 η (%)</th>';
        html += '<th style="padding: 0.75rem; text-align: right;">内功率 (kW)</th>';
        html += '<th style="padding: 0.75rem; text-align: right;">轴功率 (kW)</th>';
        html += '</tr></thead>';
        html += '<tbody>';
        
        data.performance_points.forEach(point => {
            html += '<tr>';
            html += `<td style="padding: 0.5rem; text-align: center;">${point.序号}</td>`;
            html += `<td style="padding: 0.5rem; text-align: right;">${point.流量.toFixed(2)}</td>`;
            html += `<td style="padding: 0.5rem; text-align: right;">${point.全压.toFixed(2)}</td>`;
            html += `<td style="padding: 0.5rem; text-align: right;">${point.内效率.toFixed(1)}</td>`;
            html += `<td style="padding: 0.5rem; text-align: right;">${point.内功率.toFixed(2)}</td>`;
            html += `<td style="padding: 0.5rem; text-align: right; font-weight: bold;">${point.轴功率.toFixed(2)}</td>`;
            html += '</tr>';
        });
        
        html += '</tbody></table>';
    }
    
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
    
    // 显示图表容器
    const chartContainer = document.getElementById('chart-container');
    if (chartContainer) {
        chartContainer.style.display = 'block';
    }
    
    // 绘制性能曲线（需要等待DOM更新和Chart.js加载）
    if (data.performance_points && data.performance_points.length > 0) {
        // 使用setTimeout确保DOM已更新
        setTimeout(() => {
            if (typeof Chart !== 'undefined') {
                drawPerformanceCharts(data.performance_points);
            } else {
                console.error('Chart.js未加载');
            }
        }, 200);
    }
    
    // 滚动到结果区域
    container.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * 重置表单
 */
function resetForm() {
    document.getElementById('Q').value = '16000';
    document.getElementById('P').value = '350';
    document.getElementById('H').value = '33';
    document.getElementById('P_inlet').value = '0';
    document.getElementById('T').value = '60';
    document.getElementById('k').value = '1.4';
    document.getElementById('n').value = '420';
    document.getElementById('fan_type').value = '4-68';
    document.getElementById('D').value = '0.8';
    document.getElementById('suction_type').value = '单吸';
    document.getElementById('rho_standard').value = '1.2';
    
    // 清空性能点
    clearPerformancePoints();
    
    // 隐藏结果
    document.getElementById('result-container').style.display = 'none';
    
    // 隐藏图表容器
    const chartContainer = document.getElementById('chart-container');
    if (chartContainer) {
        chartContainer.style.display = 'none';
    }
    
    // 销毁图表
    if (pressureEfficiencyChart) {
        pressureEfficiencyChart.destroy();
        pressureEfficiencyChart = null;
    }
    if (pressurePowerChart) {
        pressurePowerChart.destroy();
        pressurePowerChart = null;
    }
}

/**
 * 绘制性能曲线图
 */
function drawPerformanceCharts(performancePoints) {
    // 准备数据
    const flowRates = performancePoints.map(p => p.流量);
    const pressures = performancePoints.map(p => p.全压);
    const efficiencies = performancePoints.map(p => p.内效率);
    const powers = performancePoints.map(p => p.轴功率);
    
    // 绘制流量-压力/效率曲线（双Y轴）
    drawPressureEfficiencyChart(flowRates, pressures, efficiencies);
    
    // 绘制流量-压力/功率曲线（双Y轴）
    drawPressurePowerChart(flowRates, pressures, powers);
}

/**
 * 绘制流量-压力/效率曲线（双Y轴）
 */
function drawPressureEfficiencyChart(flowRates, pressures, efficiencies) {
    const canvas = document.getElementById('pressureEfficiencyChart');
    if (!canvas) {
        console.error('找不到canvas元素: pressureEfficiencyChart');
        return;
    }
    
    if (typeof Chart === 'undefined') {
        console.error('Chart.js未加载');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    // 销毁旧图表
    if (pressureEfficiencyChart) {
        pressureEfficiencyChart.destroy();
    }
    
    pressureEfficiencyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flowRates.map(f => f.toFixed(0)),
            datasets: [
                {
                    label: '流量-压力',
                    data: pressures,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    yAxisID: 'y'
                },
                {
                    label: '流量-效率',
                    data: efficiencies,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: '流量-压力/效率曲线',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.datasetIndex === 0) {
                                return `流量-压力: ${context.parsed.x.toFixed(2)} m³/h, ${context.parsed.y.toFixed(2)} Pa`;
                            } else {
                                return `流量-效率: ${context.parsed.x.toFixed(2)} m³/h, ${context.parsed.y.toFixed(2)}%`;
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '流量 (m³/h)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(0);
                        }
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: '压力 (Pa)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(0);
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: '效率 (%)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    }
                }
            }
        }
    });
}

/**
 * 绘制流量-压力/功率曲线（双Y轴）
 */
function drawPressurePowerChart(flowRates, pressures, powers) {
    const canvas = document.getElementById('pressurePowerChart');
    if (!canvas) {
        console.error('找不到canvas元素: pressurePowerChart');
        return;
    }
    
    if (typeof Chart === 'undefined') {
        console.error('Chart.js未加载');
        return;
    }
    
    const ctx = canvas.getContext('2d');
    
    // 销毁旧图表
    if (pressurePowerChart) {
        pressurePowerChart.destroy();
    }
    
    pressurePowerChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flowRates.map(f => f.toFixed(0)),
            datasets: [
                {
                    label: '流量-压力',
                    data: pressures,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    yAxisID: 'y'
                },
                {
                    label: '流量-功率',
                    data: powers,
                    borderColor: 'rgb(255, 0, 0)',
                    backgroundColor: 'rgba(255, 0, 0, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                title: {
                    display: true,
                    text: '流量-压力/功率曲线',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.datasetIndex === 0) {
                                return `流量-压力: ${context.parsed.x.toFixed(2)} m³/h, ${context.parsed.y.toFixed(2)} Pa`;
                            } else {
                                return `流量-功率: ${context.parsed.x.toFixed(2)} m³/h, ${context.parsed.y.toFixed(2)} kW`;
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '流量 (m³/h)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(0);
                        }
                    }
                },
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: '压力 (Pa)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(0);
                        }
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: '功率 (kW)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        drawOnChartArea: false,
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}