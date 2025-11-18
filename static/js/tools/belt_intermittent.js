/**
 * 皮带轮间歇运动选型计算 - 前端计算逻辑
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
 * 1. 速度曲线 - 加速时间计算
 */
async function calculateSpeedCurve() {
    const t = parseFloat(document.getElementById('sc_t').value);
    const A = parseFloat(document.getElementById('sc_A').value);
    
    if (!t || t <= 0) {
        showError('请输入有效的定位时间');
        return;
    }
    if (A === undefined || A < 0 || A > 1) {
        showError('加减速时间比应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'speed_curve',
        t: t,
        A: A
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
        document.getElementById('sc_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('sc_result_unit').textContent = result.unit;
        renderFormula('sc_result_formula', result.formula);
        document.getElementById('sc_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 电机转速计算
 */
async function calculateMotorSpeed() {
    const LInput = document.getElementById('ms_L').value.trim();
    const DInput = document.getElementById('ms_D').value.trim();
    const tInput = document.getElementById('ms_t').value.trim();
    const t0Input = document.getElementById('ms_t0').value.trim();
    const iInput = document.getElementById('ms_i').value.trim();
    
    if (LInput === '') {
        showError('请输入每次运动距离');
        return;
    }
    const L = parseFloat(LInput);
    if (isNaN(L) || L <= 0) {
        showError('每次运动距离必须大于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入滚筒直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('滚筒直径必须大于0');
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
    
    if (t0Input === '') {
        showError('请输入加速时间');
        return;
    }
    const t0 = parseFloat(t0Input);
    if (isNaN(t0) || t0 <= 0) {
        showError('加速时间必须大于0');
        return;
    }
    if (t0 >= t) {
        showError('加速时间必须小于定位时间');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'motor_speed',
        L: L,
        D: D,
        t: t,
        t0: t0,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
        if (result.extra) {
            document.getElementById('ms_beta_value').textContent = formatNumber(result.extra.beta, 4);
            document.getElementById('ms_N_value').textContent = formatNumber(result.extra.N, 2);
            document.getElementById('ms_betaM_value').textContent = formatNumber(result.extra.betaM, 4);
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
 * 3. 负载转矩计算
 */
async function calculateLoadTorque() {
    const FAInput = document.getElementById('lt_FA').value.trim();
    const mLInput = document.getElementById('lt_mL').value.trim();
    const aInput = document.getElementById('lt_a').value.trim();
    const muInput = document.getElementById('lt_mu').value.trim();
    const DInput = document.getElementById('lt_D').value.trim();
    const etaInput = document.getElementById('lt_eta').value.trim();
    const iInput = document.getElementById('lt_i').value.trim();
    const etaGInput = document.getElementById('lt_etaG').value.trim();
    
    const FA = FAInput === '' ? 0 : parseFloat(FAInput);
    if (isNaN(FA) || FA < 0) {
        showError('外力必须大于等于0');
        return;
    }
    
    if (mLInput === '') {
        showError('请输入皮带与工作物总质量');
        return;
    }
    const mL = parseFloat(mLInput);
    if (isNaN(mL) || mL <= 0) {
        showError('皮带与工作物总质量必须大于0');
        return;
    }
    
    const a = aInput === '' ? 0 : parseFloat(aInput);
    if (isNaN(a) || a < -90 || a > 90) {
        showError('移动方向与水平轴夹角应在-90°到90°之间');
        return;
    }
    
    const mu = muInput === '' ? 0.3 : parseFloat(muInput);
    if (isNaN(mu) || mu < 0) {
        showError('滑动面摩擦系数不能为负数');
        return;
    }
    
    if (DInput === '') {
        showError('请输入滚筒直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('滚筒直径必须大于0');
        return;
    }
    
    const eta = etaInput === '' ? 0.9 : parseFloat(etaInput);
    if (isNaN(eta) || eta <= 0 || eta > 1) {
        showError('传送带和滚筒的机械效率应在0-1之间');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const etaG = etaGInput === '' ? 0.7 : parseFloat(etaGInput);
    if (isNaN(etaG) || etaG <= 0 || etaG > 1) {
        showError('减速机机械效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'load_torque',
        FA: FA,
        mL: mL,
        a: a,
        mu: mu,
        D: D,
        eta: eta,
        i: i,
        etaG: etaG
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.F) {
            document.getElementById('lt_F_value').textContent = formatNumber(result.extra.F, 4);
            }
            if (result.extra.TL) {
                document.getElementById('lt_TL_value').textContent = formatNumber(result.extra.TL, 6);
            }
        }
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
 * 4. 电机轴加速转矩计算
 */
async function calculateAccelerationTorque() {
    const mLInput = document.getElementById('at_mL').value.trim();
    const DInput = document.getElementById('at_D').value.trim();
    const m2Input = document.getElementById('at_m2').value.trim();
    const iInput = document.getElementById('at_i').value.trim();
    const JMInput = document.getElementById('at_JM').value.trim();
    const betaMInput = document.getElementById('at_betaM').value.trim();
    const etaGInput = document.getElementById('at_etaG').value.trim();
    
    if (mLInput === '') {
        showError('请输入皮带与工作物总质量');
        return;
    }
    const mL = parseFloat(mLInput);
    if (isNaN(mL) || mL <= 0) {
        showError('皮带与工作物总质量必须大于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入滚筒直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('滚筒直径必须大于0');
        return;
    }
    
    if (m2Input === '') {
        showError('请输入滚筒质量');
        return;
    }
    const m2 = parseFloat(m2Input);
    if (isNaN(m2) || m2 <= 0) {
        showError('滚筒质量必须大于0');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const JM = JMInput === '' ? 0.00027 : parseFloat(JMInput);
    if (isNaN(JM) || JM <= 0) {
        showError('电机惯量必须大于0');
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
    
    const etaG = etaGInput === '' ? 0.7 : parseFloat(etaGInput);
    if (isNaN(etaG) || etaG <= 0 || etaG > 1) {
        showError('减速机机械效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'acceleration_torque',
        mL: mL,
        D: D,
        m2: m2,
        i: i,
        JM: JM,
        betaM: betaM,
        etaG: etaG
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.JM1 !== undefined) {
                document.getElementById('at_JM1_value').textContent = formatNumber(result.extra.JM1, 6);
            }
            if (result.extra.JM2 !== undefined) {
                document.getElementById('at_JM2_value').textContent = formatNumber(result.extra.JM2, 6);
            }
            if (result.extra.JL !== undefined) {
                document.getElementById('at_JL_value').textContent = formatNumber(result.extra.JL, 6);
            }
            if (result.extra.J !== undefined) {
                document.getElementById('at_J_value').textContent = formatNumber(result.extra.J, 6);
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
    const TLMInput = document.getElementById('rt_TLM').value.trim();
    const TSInput = document.getElementById('rt_TS').value.trim();
    const SInput = document.getElementById('rt_S').value.trim();
    
    if (TLMInput === '') {
        showError('请输入电机轴负载转矩');
        return;
    }
    const TLM = parseFloat(TLMInput);
    if (isNaN(TLM) || TLM < 0) {
        showError('电机轴负载转矩必须大于等于0');
        return;
    }
    
    if (TSInput === '') {
        showError('请输入电机轴加速转矩');
        return;
    }
    const TS = parseFloat(TSInput);
    if (isNaN(TS) || TS < 0) {
        showError('电机轴加速转矩必须大于等于0');
        return;
    }
    
    const S = SInput === '' ? 2 : parseFloat(SInput);
    if (isNaN(S) || S <= 0) {
        showError('安全系数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'required_torque',
        TLM: TLM,
        TS: TS,
        S: S
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
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
        showError('请输入折算到减速机轴的负载惯量');
        return;
    }
    const JL = parseFloat(JLInput);
    if (isNaN(JL) || JL <= 0) {
        showError('折算到减速机轴的负载惯量必须大于0');
        return;
    }
    
    if (iInput === '') {
        showError('请输入减速比');
        return;
    }
    const i = parseFloat(iInput);
    if (isNaN(i) || i <= 0) {
        showError('减速比必须大于0');
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
        const result = await apiRequest('/api/tools/belt-intermittent/calculate', 'POST', params);
        document.getElementById('ir_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('ir_result_formula', result.formula);
        
        // 显示警告
        const warningDiv = document.getElementById('ir_warning');
        if (result.result > 5) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.borderLeft = '4px solid #ffc107';
            warningDiv.innerHTML = '<strong>警告：</strong>惯量比大于5，建议考虑调整减速比或选择更大惯量的电机以提高惯量匹配。';
        } else {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#d4edda';
            warningDiv.style.borderLeft = '4px solid #28a745';
            warningDiv.innerHTML = '<strong>提示：</strong>惯量比在合理范围内（≤5）。';
        }
        
        document.getElementById('ir_result').style.display = 'block';
        document.getElementById('ir_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}
