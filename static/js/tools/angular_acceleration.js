/**
 * 角加速度计算 - 前端计算逻辑
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

/**
 * 1. 加速时间计算
 */
async function calculateAccelerationTime() {
    const tInput = document.getElementById('at_t').value.trim();
    const AInput = document.getElementById('at_A').value.trim();
    
    if (tInput === '') {
        showError('请输入每次定位时间');
        return;
    }
    const t = parseFloat(tInput);
    if (isNaN(t) || t <= 0) {
        showError('每次定位时间必须大于0');
        return;
    }
    
    if (AInput === '') {
        showError('请输入加减速时间比');
        return;
    }
    const A = parseFloat(AInput);
    if (isNaN(A) || A <= 0 || A >= 1) {
        showError('加减速时间比必须在0和1之间');
        return;
    }
    
    const params = {
        scenario: 'acceleration_time',
        t: t,
        A: A
    };
    
    try {
        const result = await apiRequest('/api/tools/angular-acceleration/calculate', 'POST', params);
        
        document.getElementById('at_t0_value').textContent = formatNumber(result.result, 4);
        renderFormula('at_result_formula', result.formula);
        document.getElementById('at_result').style.display = 'block';
        document.getElementById('at_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 电机转速计算
 */
async function calculateMotorSpeed() {
    const iInput = document.getElementById('ms_i').value.trim();
    const tInput = document.getElementById('ms_t').value.trim();
    const LInput = document.getElementById('ms_L').value.trim();
    const AInput = document.getElementById('ms_A').value.trim();
    
    if (iInput === '') {
        showError('请输入减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    if (tInput === '') {
        showError('请输入每次定位时间');
        return;
    }
    const t = parseFloat(tInput);
    if (isNaN(t) || t <= 0) {
        showError('每次定位时间必须大于0');
        return;
    }
    
    if (LInput === '') {
        showError('请输入每次运动角度');
        return;
    }
    const L = parseFloat(LInput);
    if (isNaN(L) || L <= 0) {
        showError('每次运动角度必须大于0');
        return;
    }
    
    if (AInput === '') {
        showError('请输入加减速时间比');
        return;
    }
    const A = parseFloat(AInput);
    if (isNaN(A) || A <= 0 || A >= 1) {
        showError('加减速时间比必须在0和1之间');
        return;
    }
    
    const params = {
        scenario: 'motor_speed',
        i: i,
        t: t,
        L: L,
        A: A
    };
    
    try {
        const result = await apiRequest('/api/tools/angular-acceleration/calculate', 'POST', params);
        
        if (result.extra) {
            if (result.extra.t0 !== undefined) {
                document.getElementById('ms_t0_value').textContent = formatNumber(result.extra.t0, 4);
            }
            if (result.extra.beta !== undefined) {
                document.getElementById('ms_beta_value').textContent = formatNumber(result.extra.beta, 6);
            }
            if (result.extra.Nmax !== undefined) {
                document.getElementById('ms_Nmax_value').textContent = formatNumber(result.extra.Nmax, 4);
            }
            if (result.extra.betaM !== undefined) {
                document.getElementById('ms_betaM_value').textContent = formatNumber(result.extra.betaM, 6);
            }
        }
        document.getElementById('ms_NM_value').textContent = formatNumber(result.result, 4);
        renderFormula('ms_result_formula', result.formula);
        document.getElementById('ms_result').style.display = 'block';
        document.getElementById('ms_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 扭矩计算
 */
async function calculateTorque() {
    const JInput = document.getElementById('tq_J').value.trim();
    const betaMInput = document.getElementById('tq_betaM').value.trim();
    
    if (JInput === '') {
        showError('请输入负载惯量');
        return;
    }
    const J = parseFloat(JInput);
    if (isNaN(J) || J <= 0) {
        showError('负载惯量必须大于0');
        return;
    }
    
    if (betaMInput === '') {
        showError('请输入电机输出轴角加速度');
        return;
    }
    const betaM = parseFloat(betaMInput);
    if (isNaN(betaM) || betaM <= 0) {
        showError('电机输出轴角加速度必须大于0');
        return;
    }
    
    const params = {
        scenario: 'torque',
        J: J,
        betaM: betaM
    };
    
    try {
        const result = await apiRequest('/api/tools/angular-acceleration/calculate', 'POST', params);
        
        if (result.extra && result.extra.T !== undefined) {
            document.getElementById('tq_T_value').textContent = formatNumber(result.extra.T, 6);
        }
        document.getElementById('tq_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('tq_result_unit').textContent = result.unit;
        renderFormula('tq_result_formula', result.formula);
        document.getElementById('tq_result').style.display = 'block';
        document.getElementById('tq_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}
