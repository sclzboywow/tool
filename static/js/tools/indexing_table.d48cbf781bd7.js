/**
 * 分度盘机构选型计算 - 前端计算逻辑
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
 * 1. 速度曲线 - 加减速时间计算
 */
async function calculateSpeedCurve() {
    const tInput = document.getElementById('sc_t').value.trim();
    const AInput = document.getElementById('sc_A').value.trim();
    
    if (tInput === '') {
        showError('请输入定位时间');
        return;
    }
    const t = parseFloat(tInput);
    if (isNaN(t) || t <= 0) {
        showError('定位时间必须大于0');
        return;
    }
    
    if (AInput === '') {
        showError('请输入加减速时间比');
        return;
    }
    const A = parseFloat(AInput);
    if (isNaN(A) || A < 0 || A > 1) {
        showError('加减速时间比应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'speed_curve',
        t: t,
        A: A
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        document.getElementById('sc_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('sc_result_unit').textContent = result.unit;
        renderFormula('sc_result_formula', result.formula);
        document.getElementById('sc_result').style.display = 'block';
        document.getElementById('sc_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 电机转速计算
 */
async function calculateMotorSpeed() {
    const thetaInput = document.getElementById('ms_theta').value.trim();
    const tInput = document.getElementById('ms_t').value.trim();
    const t0Input = document.getElementById('ms_t0').value.trim();
    const iInput = document.getElementById('ms_i').value.trim();
    
    if (thetaInput === '') {
        showError('请输入定位角度');
        return;
    }
    const theta = parseFloat(thetaInput);
    if (isNaN(theta) || theta <= 0) {
        showError('定位角度必须大于0');
        return;
    }
    
    if (tInput === '') {
        showError('请输入定位时间');
        return;
    }
    const t = parseFloat(tInput);
    if (isNaN(t) || t <= 0) {
        showError('定位时间必须大于0');
        return;
    }
    
    if (t0Input === '') {
        showError('请输入加减速时间');
        return;
    }
    const t0 = parseFloat(t0Input);
    if (isNaN(t0) || t0 <= 0) {
        showError('加减速时间必须大于0');
        return;
    }
    
    if (t0 >= t) {
        showError('加减速时间必须小于定位时间');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速机减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速机减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'motor_speed',
        theta: theta,
        t: t,
        t0: t0,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.betaG !== undefined) {
                document.getElementById('ms_betaG_value').textContent = formatNumber(result.extra.betaG, 6);
            }
            if (result.extra.N !== undefined) {
                document.getElementById('ms_N_value').textContent = formatNumber(result.extra.N, 2);
            }
            if (result.extra.betaM !== undefined) {
                document.getElementById('ms_betaM_value').textContent = formatNumber(result.extra.betaM, 6);
            }
        }
        document.getElementById('ms_result_value').textContent = formatNumber(result.result, 2);
        document.getElementById('ms_result_unit').textContent = result.unit;
        renderFormula('ms_result_formula', result.formula);
        document.getElementById('ms_result').style.display = 'block';
        document.getElementById('ms_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 负载转矩计算（分度盘摩擦负载很小，通常忽略）
 */
async function calculateLoadTorque() {
    const params = {
        scenario: 'load_torque'
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        document.getElementById('lt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('lt_result_unit').textContent = result.unit;
        renderFormula('lt_result_formula', result.formula);
        document.getElementById('lt_result').style.display = 'block';
        document.getElementById('lt_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 加速转矩计算
 */
async function calculateAccelerationTorque() {
    const DTInput = document.getElementById('at_DT').value.trim();
    const LTInput = document.getElementById('at_LT').value.trim();
    const DWInput = document.getElementById('at_DW').value.trim();
    const LWInput = document.getElementById('at_LW').value.trim();
    const rhoInput = document.getElementById('at_rho').value.trim();
    const nInput = document.getElementById('at_n').value.trim();
    const lInput = document.getElementById('at_l').value.trim();
    const iInput = document.getElementById('at_i').value.trim();
    const JMInput = document.getElementById('at_JM').value.trim();
    const betaMInput = document.getElementById('at_betaM').value.trim();
    const etaGInput = document.getElementById('at_etaG').value.trim();
    
    if (DTInput === '') {
        showError('请输入分度盘直径');
        return;
    }
    const DT = parseFloat(DTInput);
    if (isNaN(DT) || DT <= 0) {
        showError('分度盘直径必须大于0');
        return;
    }
    
    if (LTInput === '') {
        showError('请输入分度盘厚度');
        return;
    }
    const LT = parseFloat(LTInput);
    if (isNaN(LT) || LT <= 0) {
        showError('分度盘厚度必须大于0');
        return;
    }
    
    if (DWInput === '') {
        showError('请输入工作物直径');
        return;
    }
    const DW = parseFloat(DWInput);
    if (isNaN(DW) || DW <= 0) {
        showError('工作物直径必须大于0');
        return;
    }
    
    if (LWInput === '') {
        showError('请输入工作物厚度');
        return;
    }
    const LW = parseFloat(LWInput);
    if (isNaN(LW) || LW <= 0) {
        showError('工作物厚度必须大于0');
        return;
    }
    
    if (rhoInput === '') {
        showError('请输入工作台材质密度');
        return;
    }
    const rho = parseFloat(rhoInput);
    if (isNaN(rho) || rho <= 0) {
        showError('工作台材质密度必须大于0');
        return;
    }
    
    if (nInput === '') {
        showError('请输入工作物数量');
        return;
    }
    const n = parseFloat(nInput);
    if (isNaN(n) || n <= 0) {
        showError('工作物数量必须大于0');
        return;
    }
    
    if (lInput === '') {
        showError('请输入由分度盘中心至工作物中心的距离');
        return;
    }
    const l = parseFloat(lInput);
    if (isNaN(l) || l <= 0) {
        showError('由分度盘中心至工作物中心的距离必须大于0');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速机减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速机减速比必须大于0');
        return;
    }
    
    if (JMInput === '') {
        showError('请输入电机惯量');
        return;
    }
    const JM = parseFloat(JMInput);
    if (isNaN(JM) || JM <= 0) {
        showError('电机惯量必须大于0');
        return;
    }
    
    if (betaMInput === '') {
        showError('请输入电机轴角加速度');
        return;
    }
    const betaM = parseFloat(betaMInput);
    if (isNaN(betaM) || betaM <= 0) {
        showError('电机轴角加速度必须大于0');
        return;
    }
    
    const etaG = etaGInput === '' ? 0.7 : parseFloat(etaGInput);
    if (isNaN(etaG) || etaG <= 0 || etaG > 1) {
        showError('减速机效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'acceleration_torque',
        DT: DT,
        LT: LT,
        DW: DW,
        LW: LW,
        rho: rho,
        n: n,
        l: l,
        i: i,
        JM: JM,
        betaM: betaM,
        etaG: etaG
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.JT !== undefined) {
                document.getElementById('at_JT_value').textContent = formatNumber(result.extra.JT, 6);
            }
            if (result.extra.JW1 !== undefined) {
                document.getElementById('at_JW1_value').textContent = formatNumber(result.extra.JW1, 6);
            }
            if (result.extra.mw !== undefined) {
                document.getElementById('at_mw_value').textContent = formatNumber(result.extra.mw, 6);
            }
            if (result.extra.JW !== undefined) {
                document.getElementById('at_JW_value').textContent = formatNumber(result.extra.JW, 6);
            }
            if (result.extra.JL !== undefined) {
                document.getElementById('at_JL_value').textContent = formatNumber(result.extra.JL, 6);
            }
            if (result.extra.JLM !== undefined) {
                document.getElementById('at_JLM_value').textContent = formatNumber(result.extra.JLM, 6);
            }
        }
        document.getElementById('at_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('at_result_unit').textContent = result.unit;
        renderFormula('at_result_formula', result.formula);
        document.getElementById('at_result').style.display = 'block';
        document.getElementById('at_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 必须转矩计算
 */
async function calculateRequiredTorque() {
    const TSInput = document.getElementById('rt_TS').value.trim();
    const TLInput = document.getElementById('rt_TL').value.trim();
    const SInput = document.getElementById('rt_S').value.trim();
    
    if (TSInput === '') {
        showError('请输入电机轴加速转矩');
        return;
    }
    const TS = parseFloat(TSInput);
    if (isNaN(TS) || TS < 0) {
        showError('电机轴加速转矩必须大于等于0');
        return;
    }
    
    const TL = TLInput === '' ? 0 : parseFloat(TLInput);
    if (isNaN(TL) || TL < 0) {
        showError('负载转矩必须大于等于0');
        return;
    }
    
    const S = SInput === '' ? 2 : parseFloat(SInput);
    if (isNaN(S) || S <= 0) {
        showError('安全系数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'required_torque',
        TS: TS,
        TL: TL,
        S: S
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        document.getElementById('rt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('rt_result_unit').textContent = result.unit;
        renderFormula('rt_result_formula', result.formula);
        document.getElementById('rt_result').style.display = 'block';
        document.getElementById('rt_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 6. 惯量比计算
 */
async function calculateInertiaRatio() {
    const JLInput = document.getElementById('ir_JL').value.trim();
    const iInput = document.getElementById('ir_i').value.trim();
    const JMInput = document.getElementById('ir_JM').value.trim();
    
    if (JLInput === '') {
        showError('请输入全负载惯量');
        return;
    }
    const JL = parseFloat(JLInput);
    if (isNaN(JL) || JL <= 0) {
        showError('全负载惯量必须大于0');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速机减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速机减速比必须大于0');
        return;
    }
    
    if (JMInput === '') {
        showError('请输入电机惯量');
        return;
    }
    const JM = parseFloat(JMInput);
    if (isNaN(JM) || JM <= 0) {
        showError('电机惯量必须大于0');
        return;
    }
    
    const params = {
        scenario: 'inertia_ratio',
        JL: JL,
        i: i,
        JM: JM
    };
    
    try {
        const result = await apiRequest('/api/tools/indexing-table/calculate', 'POST', params);
        document.getElementById('ir_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('ir_result_formula', result.formula);
        
        // 显示警告信息
        const warningDiv = document.getElementById('ir_warning');
        if (result.result > 5) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.border = '1px solid #ffc107';
            warningDiv.style.color = '#856404';
            warningDiv.innerHTML = '<strong>警告：</strong>惯量比大于5，建议重新选择电机或调整减速比，以确保系统具有良好的动态响应性能。';
        } else if (result.result > 3) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#d1ecf1';
            warningDiv.style.border = '1px solid #bee5eb';
            warningDiv.style.color = '#0c5460';
            warningDiv.innerHTML = '<strong>提示：</strong>惯量比在3-5之间，系统动态响应性能可接受，但建议优化到3以下以获得更好的性能。';
        } else {
            warningDiv.style.display = 'none';
        }
        
        document.getElementById('ir_result').style.display = 'block';
        document.getElementById('ir_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

