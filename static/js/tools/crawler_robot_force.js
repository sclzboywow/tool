/**
 * 履带机器人驱动力计算 - 前端计算逻辑
 */

/**
 * 切换子标签页
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

// showError 函数已在 common.js 中定义，使用屏幕中间的模态框显示

/**
 * 1. 功率计算
 */
async function calculatePower() {
    const fInput = document.getElementById('pc_f').value.trim();
    const m1Input = document.getElementById('pc_m1').value.trim();
    const m2Input = document.getElementById('pc_m2').value.trim();
    const vRatedInput = document.getElementById('pc_v_rated').value.trim();
    const slopePercentInput = document.getElementById('pc_slope_percent').value.trim();
    const nEffectiveInput = document.getElementById('pc_n_effective').value.trim();
    const PMotorInput = document.getElementById('pc_P_motor').value.trim();
    
    if (fInput === '') {
        showError('请输入滚动摩擦系数');
        return;
    }
    const f = parseFloat(fInput);
    if (isNaN(f) || f < 0) {
        showError('滚动摩擦系数必须大于等于0');
        return;
    }
    
    if (m1Input === '') {
        showError('请输入车体重量');
        return;
    }
    const m1 = parseFloat(m1Input);
    if (isNaN(m1) || m1 <= 0) {
        showError('车体重量必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入负载重量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 < 0) {
        showError('负载重量必须大于等于0');
        return;
    }
    
    if (vRatedInput === '') {
        showError('请输入平地车体额定速度');
        return;
    }
    const v_rated = parseFloat(vRatedInput);
    if (isNaN(v_rated) || v_rated <= 0) {
        showError('平地车体额定速度必须大于0');
        return;
    }
    
    if (slopePercentInput === '') {
        showError('请输入轨道坡度');
        return;
    }
    const slope_percent = parseFloat(slopePercentInput);
    if (isNaN(slope_percent) || slope_percent < 0) {
        showError('轨道坡度必须大于等于0');
        return;
    }
    
    if (nEffectiveInput === '') {
        showError('请输入有效电机数');
        return;
    }
    const n_effective = parseFloat(nEffectiveInput);
    if (isNaN(n_effective) || n_effective <= 0) {
        showError('有效电机数必须大于0');
        return;
    }
    
    if (PMotorInput === '') {
        showError('请输入电机功率');
        return;
    }
    const P_motor = parseFloat(PMotorInput);
    if (isNaN(P_motor) || P_motor <= 0) {
        showError('电机功率必须大于0');
        return;
    }
    
    const params = {
        scenario: 'power_calc',
        f: f,
        m1: m1,
        m2: m2,
        v_rated: v_rated,
        slope_percent: slope_percent,
        n_effective: n_effective,
        P_motor: P_motor
    };
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.P1 !== undefined) {
                document.getElementById('pc_P1_value').textContent = formatNumber(result.extra.P1, 2);
            }
            if (result.extra.P2 !== undefined) {
                document.getElementById('pc_P2_value').textContent = formatNumber(result.extra.P2, 2);
            }
            if (result.extra.P3 !== undefined) {
                document.getElementById('pc_P3_value').textContent = formatNumber(result.extra.P3, 2);
            }
        }
        document.getElementById('pc_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('pc_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('pc_warning');
        if (result.result < 1.2) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>行走功率安全系数小于1.2，建议重新选择电机或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('pc_result').style.display = 'block';
        document.getElementById('pc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 扭矩计算
 */
async function calculateTorque() {
    const fInput = document.getElementById('tc_f').value.trim();
    const m1Input = document.getElementById('tc_m1').value.trim();
    const m2Input = document.getElementById('tc_m2').value.trim();
    const DInput = document.getElementById('tc_D').value.trim();
    const slopePercentInput = document.getElementById('tc_slope_percent').value.trim();
    const IActualInput = document.getElementById('tc_I_actual').value.trim();
    const INoLoadInput = document.getElementById('tc_I_no_load').value.trim();
    const IRatedInput = document.getElementById('tc_I_rated').value.trim();
    const TRatedInput = document.getElementById('tc_T_rated').value.trim();
    const iTotalInput = document.getElementById('tc_i_total').value.trim();
    const nEffectiveInput = document.getElementById('tc_n_effective').value.trim();
    
    if (fInput === '') {
        showError('请输入滚动摩擦系数');
        return;
    }
    const f = parseFloat(fInput);
    if (isNaN(f) || f < 0) {
        showError('滚动摩擦系数必须大于等于0');
        return;
    }
    
    if (m1Input === '') {
        showError('请输入车体重量');
        return;
    }
    const m1 = parseFloat(m1Input);
    if (isNaN(m1) || m1 <= 0) {
        showError('车体重量必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入负载重量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 < 0) {
        showError('负载重量必须大于等于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入履带轮子直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('履带轮子直径必须大于0');
        return;
    }
    
    if (slopePercentInput === '') {
        showError('请输入轨道坡度');
        return;
    }
    const slope_percent = parseFloat(slopePercentInput);
    if (isNaN(slope_percent) || slope_percent < 0) {
        showError('轨道坡度必须大于等于0');
        return;
    }
    
    if (IActualInput === '') {
        showError('请输入实际电流(平均)');
        return;
    }
    const I_actual = parseFloat(IActualInput);
    if (isNaN(I_actual) || I_actual <= 0) {
        showError('实际电流(平均)必须大于0');
        return;
    }
    
    if (INoLoadInput === '') {
        showError('请输入空转电流');
        return;
    }
    const I_no_load = parseFloat(INoLoadInput);
    if (isNaN(I_no_load) || I_no_load < 0) {
        showError('空转电流必须大于等于0');
        return;
    }
    
    if (IRatedInput === '') {
        showError('请输入额定电流');
        return;
    }
    const I_rated = parseFloat(IRatedInput);
    if (isNaN(I_rated) || I_rated <= 0) {
        showError('额定电流必须大于0');
        return;
    }
    
    if (TRatedInput === '') {
        showError('请输入额定扭矩');
        return;
    }
    const T_rated = parseFloat(TRatedInput);
    if (isNaN(T_rated) || T_rated <= 0) {
        showError('额定扭矩必须大于0');
        return;
    }
    
    if (iTotalInput === '') {
        showError('请输入总减速比');
        return;
    }
    const i_total = parseFloat(iTotalInput);
    if (isNaN(i_total) || i_total <= 0) {
        showError('总减速比必须大于0');
        return;
    }
    
    if (nEffectiveInput === '') {
        showError('请输入有效电机数');
        return;
    }
    const n_effective = parseFloat(nEffectiveInput);
    if (isNaN(n_effective) || n_effective <= 0) {
        showError('有效电机数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'torque_calc',
        f: f,
        m1: m1,
        m2: m2,
        D: D,
        slope_percent: slope_percent,
        I_actual: I_actual,
        I_no_load: I_no_load,
        I_rated: I_rated,
        T_rated: T_rated,
        i_total: i_total,
        n_effective: n_effective
    };
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.T1 !== undefined) {
                document.getElementById('tc_T1_value').textContent = formatNumber(result.extra.T1, 4);
            }
            if (result.extra.T2 !== undefined) {
                document.getElementById('tc_T2_value').textContent = formatNumber(result.extra.T2, 4);
            }
            if (result.extra.T3 !== undefined) {
                document.getElementById('tc_T3_value').textContent = formatNumber(result.extra.T3, 4);
            }
        }
        document.getElementById('tc_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('tc_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('tc_warning');
        if (result.result < 1.2) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>行走额定扭矩安全系数小于1.2，建议重新选择电机或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('tc_result').style.display = 'block';
        document.getElementById('tc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 加速扭矩计算
 */
async function calculateAccelerationTorque() {
    const fInput = document.getElementById('atc_f').value.trim();
    const m1Input = document.getElementById('atc_m1').value.trim();
    const m2Input = document.getElementById('atc_m2').value.trim();
    const DInput = document.getElementById('atc_D').value.trim();
    const slopePercentInput = document.getElementById('atc_slope_percent').value.trim();
    const aInput = document.getElementById('atc_a').value.trim();
    const aSlopeInput = document.getElementById('atc_a_slope').value.trim();
    const TMaxInput = document.getElementById('atc_T_max').value.trim();
    const iTotalInput = document.getElementById('atc_i_total').value.trim();
    const nEffectiveInput = document.getElementById('atc_n_effective').value.trim();
    
    if (fInput === '') {
        showError('请输入滚动摩擦系数');
        return;
    }
    const f = parseFloat(fInput);
    if (isNaN(f) || f < 0) {
        showError('滚动摩擦系数必须大于等于0');
        return;
    }
    
    if (m1Input === '') {
        showError('请输入车体重量');
        return;
    }
    const m1 = parseFloat(m1Input);
    if (isNaN(m1) || m1 <= 0) {
        showError('车体重量必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入负载重量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 < 0) {
        showError('负载重量必须大于等于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入履带轮子直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('履带轮子直径必须大于0');
        return;
    }
    
    if (slopePercentInput === '') {
        showError('请输入轨道坡度');
        return;
    }
    const slope_percent = parseFloat(slopePercentInput);
    if (isNaN(slope_percent) || slope_percent < 0) {
        showError('轨道坡度必须大于等于0');
        return;
    }
    
    if (aInput === '') {
        showError('请输入运行加速度');
        return;
    }
    const a = parseFloat(aInput);
    if (isNaN(a) || a < 0) {
        showError('运行加速度必须大于等于0');
        return;
    }
    
    if (aSlopeInput === '') {
        showError('请输入坡道加速度');
        return;
    }
    const a_slope = parseFloat(aSlopeInput);
    if (isNaN(a_slope) || a_slope < 0) {
        showError('坡道加速度必须大于等于0');
        return;
    }
    
    if (TMaxInput === '') {
        showError('请输入最大扭矩');
        return;
    }
    const T_max = parseFloat(TMaxInput);
    if (isNaN(T_max) || T_max <= 0) {
        showError('最大扭矩必须大于0');
        return;
    }
    
    if (iTotalInput === '') {
        showError('请输入总减速比');
        return;
    }
    const i_total = parseFloat(iTotalInput);
    if (isNaN(i_total) || i_total <= 0) {
        showError('总减速比必须大于0');
        return;
    }
    
    if (nEffectiveInput === '') {
        showError('请输入有效电机数');
        return;
    }
    const n_effective = parseFloat(nEffectiveInput);
    if (isNaN(n_effective) || n_effective <= 0) {
        showError('有效电机数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'acceleration_torque_calc',
        f: f,
        m1: m1,
        m2: m2,
        D: D,
        slope_percent: slope_percent,
        a: a,
        a_slope: a_slope,
        T_max: T_max,
        i_total: i_total,
        n_effective: n_effective
    };
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.T4 !== undefined) {
                document.getElementById('atc_T4_value').textContent = formatNumber(result.extra.T4, 4);
            }
            if (result.extra.T5 !== undefined) {
                document.getElementById('atc_T5_value').textContent = formatNumber(result.extra.T5, 4);
            }
            if (result.extra.T6 !== undefined) {
                document.getElementById('atc_T6_value').textContent = formatNumber(result.extra.T6, 4);
            }
        }
        document.getElementById('atc_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('atc_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('atc_warning');
        if (result.result < 1.2) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>加速最大扭矩安全系数小于1.2，建议重新选择电机或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('atc_result').style.display = 'block';
        document.getElementById('atc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 越障计算
 */
async function calculateObstacle() {
    const m1Input = document.getElementById('oc_m1').value.trim();
    const m2Input = document.getElementById('oc_m2').value.trim();
    const DInput = document.getElementById('oc_D').value.trim();
    const obstacleHeightInput = document.getElementById('oc_obstacle_height').value.trim();
    const fInput = document.getElementById('oc_f').value.trim();
    const slopePercentInput = document.getElementById('oc_slope_percent').value.trim();
    const aSlopeInput = document.getElementById('oc_a_slope').value.trim();
    const peakAttachmentInput = document.getElementById('oc_peak_attachment').value.trim();
    const TMaxInput = document.getElementById('oc_T_max').value.trim();
    const iTotalInput = document.getElementById('oc_i_total').value.trim();
    const nEffectiveInput = document.getElementById('oc_n_effective').value.trim();
    
    if (m1Input === '') {
        showError('请输入车体重量');
        return;
    }
    const m1 = parseFloat(m1Input);
    if (isNaN(m1) || m1 <= 0) {
        showError('车体重量必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入负载重量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 < 0) {
        showError('负载重量必须大于等于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入履带轮子直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('履带轮子直径必须大于0');
        return;
    }
    
    if (fInput === '') {
        showError('请输入滚动摩擦系数');
        return;
    }
    const f = parseFloat(fInput);
    if (isNaN(f) || f < 0) {
        showError('滚动摩擦系数必须大于等于0');
        return;
    }
    
    if (slopePercentInput === '') {
        showError('请输入轨道坡度');
        return;
    }
    const slope_percent = parseFloat(slopePercentInput);
    if (isNaN(slope_percent) || slope_percent < 0) {
        showError('轨道坡度必须大于等于0');
        return;
    }
    
    if (aSlopeInput === '') {
        showError('请输入坡道加速度');
        return;
    }
    const a_slope = parseFloat(aSlopeInput);
    if (isNaN(a_slope) || a_slope < 0) {
        showError('坡道加速度必须大于等于0');
        return;
    }
    
    if (peakAttachmentInput === '') {
        showError('请输入地面峰值附着系数');
        return;
    }
    const peak_attachment = parseFloat(peakAttachmentInput);
    if (isNaN(peak_attachment) || peak_attachment <= 0) {
        showError('地面峰值附着系数必须大于0');
        return;
    }
    
    if (TMaxInput === '') {
        showError('请输入最大扭矩');
        return;
    }
    const T_max = parseFloat(TMaxInput);
    if (isNaN(T_max) || T_max <= 0) {
        showError('最大扭矩必须大于0');
        return;
    }
    
    if (iTotalInput === '') {
        showError('请输入总减速比');
        return;
    }
    const i_total = parseFloat(iTotalInput);
    if (isNaN(i_total) || i_total <= 0) {
        showError('总减速比必须大于0');
        return;
    }
    
    if (nEffectiveInput === '') {
        showError('请输入有效电机数');
        return;
    }
    const n_effective = parseFloat(nEffectiveInput);
    if (isNaN(n_effective) || n_effective <= 0) {
        showError('有效电机数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'obstacle_calc',
        m1: m1,
        m2: m2,
        D: D,
        f: f,
        slope_percent: slope_percent,
        a_slope: a_slope,
        peak_attachment: peak_attachment,
        T_max: T_max,
        i_total: i_total,
        n_effective: n_effective
    };
    
    // 如果提供了障碍物高度，添加到参数中（可选参数）
    if (obstacleHeightInput !== '') {
        const obstacle_height = parseFloat(obstacleHeightInput);
        if (!isNaN(obstacle_height) && obstacle_height >= 0) {
            params.obstacle_height = obstacle_height;
        }
    }
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.T7 !== undefined) {
                document.getElementById('oc_T7_value').textContent = formatNumber(result.extra.T7, 4);
            }
            if (result.extra.T8 !== undefined) {
                document.getElementById('oc_T8_value').textContent = formatNumber(result.extra.T8, 4);
            }
            if (result.extra.T9 !== undefined) {
                document.getElementById('oc_T9_value').textContent = formatNumber(result.extra.T9, 4);
            }
            if (result.extra.T_road !== undefined) {
                document.getElementById('oc_T_road_value').textContent = formatNumber(result.extra.T_road, 4);
            }
            if (result.extra.K_road !== undefined) {
                document.getElementById('oc_K_road_value').textContent = formatNumber(result.extra.K_road, 2);
            }
        }
        document.getElementById('oc_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('oc_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('oc_warning');
        let warnings = [];
        if (result.result < 1.2) {
            warnings.push('越障最大扭矩安全系数小于1.2');
        }
        if (result.extra && result.extra.K_road < 1.2) {
            warnings.push('路面提供扭矩安全系数小于1.2');
        }
        if (warnings.length > 0) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>' + warnings.join('，') + '，建议重新选择电机或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('oc_result').style.display = 'block';
        document.getElementById('oc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 原地回转计算
 */
async function calculateRotation() {
    const m1Input = document.getElementById('rc_m1').value.trim();
    const m2Input = document.getElementById('rc_m2').value.trim();
    const fInput = document.getElementById('rc_f').value.trim();
    const uInput = document.getElementById('rc_u').value.trim();
    const LInput = document.getElementById('rc_L').value.trim();
    const BInput = document.getElementById('rc_B').value.trim();
    const IActualInput = document.getElementById('rc_I_actual').value.trim();
    const INoLoadInput = document.getElementById('rc_I_no_load').value.trim();
    const IRatedInput = document.getElementById('rc_I_rated').value.trim();
    const TRatedInput = document.getElementById('rc_T_rated').value.trim();
    const iTotalInput = document.getElementById('rc_i_total').value.trim();
    const DDriveInput = document.getElementById('rc_D_drive').value.trim();
    
    if (m1Input === '') {
        showError('请输入车体重量');
        return;
    }
    const m1 = parseFloat(m1Input);
    if (isNaN(m1) || m1 <= 0) {
        showError('车体重量必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入负载重量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 < 0) {
        showError('负载重量必须大于等于0');
        return;
    }
    
    if (fInput === '') {
        showError('请输入滚动摩擦系数');
        return;
    }
    const f = parseFloat(fInput);
    if (isNaN(f) || f < 0) {
        showError('滚动摩擦系数必须大于等于0');
        return;
    }
    
    if (uInput === '') {
        showError('请输入滑动摩擦系数');
        return;
    }
    const u = parseFloat(uInput);
    if (isNaN(u) || u < 0) {
        showError('滑动摩擦系数必须大于等于0');
        return;
    }
    
    if (LInput === '') {
        showError('请输入接地长度（前后）');
        return;
    }
    const L = parseFloat(LInput);
    if (isNaN(L) || L <= 0) {
        showError('接地长度（前后）必须大于0');
        return;
    }
    
    if (BInput === '') {
        showError('请输入履带间距（左右）');
        return;
    }
    const B = parseFloat(BInput);
    if (isNaN(B) || B <= 0) {
        showError('履带间距（左右）必须大于0');
        return;
    }
    
    if (IActualInput === '') {
        showError('请输入实际电流(平均)');
        return;
    }
    const I_actual = parseFloat(IActualInput);
    if (isNaN(I_actual) || I_actual <= 0) {
        showError('实际电流(平均)必须大于0');
        return;
    }
    
    if (INoLoadInput === '') {
        showError('请输入空转电流');
        return;
    }
    const I_no_load = parseFloat(INoLoadInput);
    if (isNaN(I_no_load) || I_no_load < 0) {
        showError('空转电流必须大于等于0');
        return;
    }
    
    if (IRatedInput === '') {
        showError('请输入额定电流');
        return;
    }
    const I_rated = parseFloat(IRatedInput);
    if (isNaN(I_rated) || I_rated <= 0) {
        showError('额定电流必须大于0');
        return;
    }
    
    if (TRatedInput === '') {
        showError('请输入额定扭矩');
        return;
    }
    const T_rated = parseFloat(TRatedInput);
    if (isNaN(T_rated) || T_rated <= 0) {
        showError('额定扭矩必须大于0');
        return;
    }
    
    if (iTotalInput === '') {
        showError('请输入总减速比');
        return;
    }
    const i_total = parseFloat(iTotalInput);
    if (isNaN(i_total) || i_total <= 0) {
        showError('总减速比必须大于0');
        return;
    }
    
    if (DDriveInput === '') {
        showError('请输入履带驱动轮直径');
        return;
    }
    const D_drive = parseFloat(DDriveInput);
    if (isNaN(D_drive) || D_drive <= 0) {
        showError('履带驱动轮直径必须大于0');
        return;
    }
    
    const params = {
        scenario: 'rotation_calc',
        m1: m1,
        m2: m2,
        f: f,
        u: u,
        L: L,
        B: B,
        I_actual: I_actual,
        I_no_load: I_no_load,
        I_rated: I_rated,
        T_rated: T_rated,
        i_total: i_total,
        D_drive: D_drive
    };
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.F1 !== undefined) {
                document.getElementById('rc_F1_value').textContent = formatNumber(result.extra.F1, 2);
            }
            if (result.extra.F2 !== undefined) {
                document.getElementById('rc_F2_value').textContent = formatNumber(result.extra.F2, 2);
            }
        }
        document.getElementById('rc_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('rc_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('rc_warning');
        if (result.result < 1.2) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>原地回转扭矩安全系数小于1.2，建议重新选择电机或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('rc_result').style.display = 'block';
        document.getElementById('rc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 6. 减速器校验
 */
async function calculateReducerCheck() {
    const IActualInput = document.getElementById('rch_I_actual').value.trim();
    const INoLoadInput = document.getElementById('rch_I_no_load').value.trim();
    const IRatedInput = document.getElementById('rch_I_rated').value.trim();
    const TRatedInput = document.getElementById('rch_T_rated').value.trim();
    const iReducerInput = document.getElementById('rch_i_reducer').value.trim();
    const iCustomInput = document.getElementById('rch_i_custom').value.trim();
    const TGearLargeInput = document.getElementById('rch_T_gear_large').value.trim();
    const TGearSmallInput = document.getElementById('rch_T_gear_small').value.trim();
    const TReducerRatedInput = document.getElementById('rch_T_reducer_rated').value.trim();
    
    if (IActualInput === '') {
        showError('请输入实际电流(平均)');
        return;
    }
    const I_actual = parseFloat(IActualInput);
    if (isNaN(I_actual) || I_actual <= 0) {
        showError('实际电流(平均)必须大于0');
        return;
    }
    
    if (INoLoadInput === '') {
        showError('请输入空转电流');
        return;
    }
    const I_no_load = parseFloat(INoLoadInput);
    if (isNaN(I_no_load) || I_no_load < 0) {
        showError('空转电流必须大于等于0');
        return;
    }
    
    if (IRatedInput === '') {
        showError('请输入额定电流');
        return;
    }
    const I_rated = parseFloat(IRatedInput);
    if (isNaN(I_rated) || I_rated <= 0) {
        showError('额定电流必须大于0');
        return;
    }
    
    if (TRatedInput === '') {
        showError('请输入额定扭矩');
        return;
    }
    const T_rated = parseFloat(TRatedInput);
    if (isNaN(T_rated) || T_rated <= 0) {
        showError('额定扭矩必须大于0');
        return;
    }
    
    if (iReducerInput === '') {
        showError('请输入减速器减速比');
        return;
    }
    const i_reducer = parseFloat(iReducerInput);
    if (isNaN(i_reducer) || i_reducer <= 0) {
        showError('减速器减速比必须大于0');
        return;
    }
    
    if (iCustomInput === '') {
        showError('请输入自制减速比');
        return;
    }
    const i_custom = parseFloat(iCustomInput);
    if (isNaN(i_custom) || i_custom <= 0) {
        showError('自制减速比必须大于0');
        return;
    }
    
    if (TReducerRatedInput === '') {
        showError('请输入减速器额定扭矩');
        return;
    }
    const T_reducer_rated = parseFloat(TReducerRatedInput);
    if (isNaN(T_reducer_rated) || T_reducer_rated <= 0) {
        showError('减速器额定扭矩必须大于0');
        return;
    }
    
    const T_gear_large = TGearLargeInput === '' ? null : parseFloat(TGearLargeInput);
    if (TGearLargeInput !== '' && (isNaN(T_gear_large) || T_gear_large <= 0)) {
        showError('大齿轮许用扭矩必须大于0');
        return;
    }
    
    const T_gear_small = TGearSmallInput === '' ? null : parseFloat(TGearSmallInput);
    if (TGearSmallInput !== '' && (isNaN(T_gear_small) || T_gear_small <= 0)) {
        showError('小齿轮许用扭矩必须大于0');
        return;
    }
    
    const params = {
        scenario: 'reducer_check',
        I_actual: I_actual,
        I_no_load: I_no_load,
        I_rated: I_rated,
        T_rated: T_rated,
        i_reducer: i_reducer,
        i_custom: i_custom,
        T_reducer_rated: T_reducer_rated
    };
    
    if (T_gear_large !== null) {
        params.T_gear_large = T_gear_large;
    }
    if (T_gear_small !== null) {
        params.T_gear_small = T_gear_small;
    }
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.T_gear_large_out !== undefined) {
                document.getElementById('rch_T_gear_large_out_value').textContent = formatNumber(result.extra.T_gear_large_out, 4);
            }
            if (result.extra.T_gear_small_out !== undefined) {
                document.getElementById('rch_T_gear_small_out_value').textContent = formatNumber(result.extra.T_gear_small_out, 4);
            }
            if (result.extra.T_reducer_out !== undefined) {
                document.getElementById('rch_T_reducer_out_value').textContent = formatNumber(result.extra.T_reducer_out, 4);
            }
            if (result.extra.K_gear_large !== undefined) {
                document.getElementById('rch_K_gear_large_value').textContent = formatNumber(result.extra.K_gear_large, 2);
            }
            if (result.extra.K_gear_small !== undefined) {
                document.getElementById('rch_K_gear_small_value').textContent = formatNumber(result.extra.K_gear_small, 2);
            }
        }
        document.getElementById('rch_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('rch_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('rch_warning');
        let warnings = [];
        if (result.result < 1.2) {
            warnings.push('减速器安全系数小于1.2');
        }
        if (result.extra && result.extra.K_gear_large !== undefined && result.extra.K_gear_large < 1.2) {
            warnings.push('大齿轮安全系数小于1.2');
        }
        if (result.extra && result.extra.K_gear_small !== undefined && result.extra.K_gear_small < 1.2) {
            warnings.push('小齿轮安全系数小于1.2');
        }
        if (warnings.length > 0) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>' + warnings.join('，') + '，建议重新选择减速器或调整参数，以确保系统可靠运行。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('rch_result').style.display = 'block';
        document.getElementById('rch_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 7. 速度计算
 */
async function calculateSpeed() {
    const nRatedInput = document.getElementById('sc_n_rated').value.trim();
    const nMaxInput = document.getElementById('sc_n_max').value.trim();
    const iTotalInput = document.getElementById('sc_i_total').value.trim();
    const DInput = document.getElementById('sc_D').value.trim();
    
    if (nRatedInput === '') {
        showError('请输入额定转速');
        return;
    }
    const n_rated = parseFloat(nRatedInput);
    if (isNaN(n_rated) || n_rated <= 0) {
        showError('额定转速必须大于0');
        return;
    }
    
    if (nMaxInput === '') {
        showError('请输入最高转速');
        return;
    }
    const n_max = parseFloat(nMaxInput);
    if (isNaN(n_max) || n_max <= 0) {
        showError('最高转速必须大于0');
        return;
    }
    
    if (iTotalInput === '') {
        showError('请输入总减速比');
        return;
    }
    const i_total = parseFloat(iTotalInput);
    if (isNaN(i_total) || i_total <= 0) {
        showError('总减速比必须大于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入履带轮子直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('履带轮子直径必须大于0');
        return;
    }
    
    const params = {
        scenario: 'speed_calc',
        n_rated: n_rated,
        n_max: n_max,
        i_total: i_total,
        D: D
    };
    
    try {
        const result = await apiRequest('/api/tools/crawler-robot-force/calculate', 'POST', params);
        if (result.extra && result.extra.v_max_calc !== undefined) {
            document.getElementById('sc_v_max_calc_value').textContent = formatNumber(result.extra.v_max_calc, 4);
        }
        document.getElementById('sc_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('sc_result_unit').textContent = result.unit;
        renderFormula('sc_result_formula', result.formula);
        document.getElementById('sc_result').style.display = 'block';
        document.getElementById('sc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}
