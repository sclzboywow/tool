/**
 * 风机性能表 - 前端计算逻辑
 */

let pressureChart = null;
let efficiencyChart = null;
let performancePoints = [];

// 初始化：添加默认性能点
document.addEventListener('DOMContentLoaded', function() {
    // 添加默认的4个性能点（基于Excel中的数据）
    const defaultPoints = [
        { psi_p: 0.43, phi: 0.2231, eta: 0.88 },
        { psi_p: 0.409, phi: 0.238, eta: 0.89 },
        { psi_p: 0.386, phi: 0.2545, eta: 0.87 },
        { psi_p: 0.3598, phi: 0.271, eta: 0.83 }
    ];
    
    defaultPoints.forEach(point => {
        addPerformancePoint(point.psi_p, point.phi, point.eta);
    });
});

/**
 * 添加性能点
 */
function addPerformancePoint(psi_p = '', phi = '', eta = '') {
    const container = document.getElementById('performance-points-container');
    const pointIndex = performancePoints.length;
    
    const pointDiv = document.createElement('div');
    pointDiv.className = 'performance-point';
    pointDiv.id = `point-${pointIndex}`;
    
    pointDiv.innerHTML = `
        <div class="form-group">
            <label>压力系数 ψ<sub>p</sub> <span class="required">*</span></label>
            <input type="number" class="psi-p-input" step="0.0001" value="${psi_p}" placeholder="例如: 0.43">
        </div>
        <div class="form-group">
            <label>流量系数 φ <span class="required">*</span></label>
            <input type="number" class="phi-input" step="0.0001" value="${phi}" placeholder="例如: 0.2231">
        </div>
        <div class="form-group">
            <label>效率 η <span class="required">*</span></label>
            <input type="number" class="eta-input" step="0.01" min="0" max="1" value="${eta}" placeholder="例如: 0.88">
        </div>
        <button type="button" class="remove-point-btn" onclick="removePerformancePoint(${pointIndex})">删除</button>
    `;
    
    container.appendChild(pointDiv);
    performancePoints.push({ psi_p, phi, eta });
}

/**
 * 删除性能点
 */
function removePerformancePoint(index) {
    const pointDiv = document.getElementById(`point-${index}`);
    if (pointDiv) {
        pointDiv.remove();
        performancePoints.splice(index, 1);
        // 重新编号所有点
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
        
        const psi_p_input = pointDiv.querySelector('.psi-p-input');
        const phi_input = pointDiv.querySelector('.phi-input');
        const eta_input = pointDiv.querySelector('.eta-input');
        
        if (psi_p_input && phi_input && eta_input) {
            const psi_p = psi_p_input.value ? parseFloat(psi_p_input.value) : '';
            const phi = phi_input.value ? parseFloat(phi_input.value) : '';
            const eta = eta_input.value ? parseFloat(eta_input.value) : '';
            
            performancePoints.push({ psi_p, phi, eta });
        }
    });
}

/**
 * 清空所有性能点
 */
function clearPerformancePoints() {
    if (confirm('确定要清空所有性能点吗？')) {
        const container = document.getElementById('performance-points-container');
        container.innerHTML = '';
        performancePoints = [];
    }
}

/**
 * 获取所有性能点数据
 */
function getPerformancePoints() {
    const container = document.getElementById('performance-points-container');
    const points = container.querySelectorAll('.performance-point');
    const result = [];
    
    points.forEach(pointDiv => {
        const psi_p = parseFloat(pointDiv.querySelector('.psi-p-input').value);
        const phi = parseFloat(pointDiv.querySelector('.phi-input').value);
        const eta = parseFloat(pointDiv.querySelector('.eta-input').value);
        
        if (!isNaN(psi_p) && !isNaN(phi) && !isNaN(eta) && eta > 0 && eta <= 1) {
            result.push({ psi_p, phi, eta });
        }
    });
    
    return result;
}

/**
 * 计算风机性能
 */
async function calculateFanPerformance() {
    // 1. 获取主要参数
    const D = parseFloat(document.getElementById('D').value);
    const n = parseFloat(document.getElementById('n').value);
    const T = parseFloat(document.getElementById('T').value);
    const P_inlet = parseFloat(document.getElementById('P_inlet').value);
    
    // 验证主要参数
    if (isNaN(D) || D <= 0) {
        showError('请输入有效的叶轮直径');
        return;
    }
    if (isNaN(n) || n <= 0) {
        showError('请输入有效的主轴转速');
        return;
    }
    if (isNaN(T)) {
        showError('请输入有效的介质温度');
        return;
    }
    if (isNaN(P_inlet) || P_inlet <= 0) {
        showError('请输入有效的进口大气压');
        return;
    }
    
    // 2. 获取性能点
    const points = getPerformancePoints();
    if (points.length === 0) {
        showError('请至少添加一个性能点');
        return;
    }
    
    // 3. 构建请求参数
    const params = {
        scenario: 'fan_performance',
        D: D,
        n: n,
        T: T,
        P_inlet: P_inlet,
        performance_points: points
    };
    
    try {
        // 4. 调用API
        const response = await fetch('/api/tools/fan-performance/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '计算失败');
        }
        
        const result = await response.json();
        
        // 5. 显示结果
        displayResults(result);
        
    } catch (error) {
        showError(error.message || '计算失败，请检查输入参数');
    }
}

/**
 * 显示计算结果
 */
function displayResults(result) {
    const container = document.getElementById('result-container');
    container.style.display = 'block';
    
    // 显示结果表格
    displayResultTable(result.result);
    
    // 绘制曲线图
    drawCharts(result.result);
    
    // 滚动到结果区域
    container.scrollIntoView({ behavior: 'smooth' });
}

/**
 * 显示结果表格
 */
function displayResultTable(results) {
    const container = document.getElementById('result-table-container');
    
    let html = '<table class="result-table">';
    html += '<thead><tr>';
    html += '<th>序号</th>';
    html += '<th>压力系数 ψ<sub>p</sub></th>';
    html += '<th>流量系数 φ</th>';
    html += '<th>效率 η</th>';
    html += '<th>压力 P (Pa)</th>';
    html += '<th>流量 Q (m³/h)</th>';
    html += '<th>内功率 P<sub>internal</sub> (kW)</th>';
    html += '</tr></thead>';
    html += '<tbody>';
    
    results.forEach((point, index) => {
        html += '<tr>';
        html += `<td>${index + 1}</td>`;
        html += `<td>${point.psi_p}</td>`;
        html += `<td>${point.phi}</td>`;
        html += `<td>${point.eta}</td>`;
        html += `<td>${point.pressure.toFixed(2)}</td>`;
        html += `<td>${point.flow_rate.toFixed(2)}</td>`;
        html += `<td>${point.internal_power.toFixed(2)}</td>`;
        html += '</tr>';
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
}

/**
 * 绘制性能曲线图
 */
function drawCharts(results) {
    // 准备数据
    const flowRates = results.map(p => p.flow_rate);
    const pressures = results.map(p => p.pressure);
    const efficiencies = results.map(p => p.eta * 100); // 转换为百分比
    
    // 绘制流量-压力曲线
    drawPressureChart(flowRates, pressures);
    
    // 绘制流量-效率曲线
    drawEfficiencyChart(flowRates, efficiencies);
}

/**
 * 绘制流量-压力曲线
 */
function drawPressureChart(flowRates, pressures) {
    const ctx = document.getElementById('pressureChart').getContext('2d');
    
    // 销毁旧图表
    if (pressureChart) {
        pressureChart.destroy();
    }
    
    pressureChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flowRates.map(f => f.toFixed(0)),
            datasets: [{
                label: '压力 (Pa)',
                data: pressures,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
                fill: false,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: '流量-压力曲线',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '流量 (m³/h)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString();
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '压力 (Pa)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

/**
 * 绘制流量-效率曲线
 */
function drawEfficiencyChart(flowRates, efficiencies) {
    const ctx = document.getElementById('efficiencyChart').getContext('2d');
    
    // 销毁旧图表
    if (efficiencyChart) {
        efficiencyChart.destroy();
    }
    
    efficiencyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flowRates.map(f => f.toFixed(0)),
            datasets: [{
                label: '效率 (%)',
                data: efficiencies,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.4,
                fill: false,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: '流量-效率曲线',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '流量 (m³/h)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString();
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '效率 (%)'
                    },
                    min: 0,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

