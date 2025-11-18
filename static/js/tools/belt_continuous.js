/**
 * 皮带轮连续运动选型计算 - 前端计算逻辑
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
 * 1. 电机转速计算（连续运动）
 */
async function calculateMotorSpeed() {
    const VInput = document.getElementById('ms_V').value.trim();
    const DInput = document.getElementById('ms_D').value.trim();
    const iInput = document.getElementById('ms_i').value.trim();
    
    if (VInput === '') {
        showError('请输入皮带速度');
        return;
    }
    const V = parseFloat(VInput);
    if (isNaN(V) || V <= 0) {
        showError('皮带速度必须大于0');
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
        V: V,
        D: D,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-continuous/calculate', 'POST', params);
        if (result.extra && result.extra.N) {
            document.getElementById('ms_N_value').textContent = formatNumber(result.extra.N, 2);
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
 * 2. 负载转矩计算
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
        const result = await apiRequest('/api/tools/belt-continuous/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.F !== undefined) {
                document.getElementById('lt_F_value').textContent = formatNumber(result.extra.F, 4);
            }
            if (result.extra.TL !== undefined) {
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
 * 3. 计算折算到电机轴的惯量
 */
async function calculateInertiaConversion() {
    const mLInput = document.getElementById('ic_mL').value.trim();
    const DInput = document.getElementById('ic_D').value.trim();
    const m2Input = document.getElementById('ic_m2').value.trim();
    
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
    
    const params = {
        scenario: 'inertia_conversion',
        mL: mL,
        D: D,
        m2: m2
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-continuous/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.JM1 !== undefined) {
                document.getElementById('ic_JM1_value').textContent = formatNumber(result.extra.JM1, 6);
            }
            if (result.extra.JM2 !== undefined) {
                document.getElementById('ic_JM2_value').textContent = formatNumber(result.extra.JM2, 6);
            }
        }
        document.getElementById('ic_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('ic_result_unit').textContent = result.unit;
        renderFormula('ic_result_formula', result.formula);
        document.getElementById('ic_result').style.display = 'block';
        document.getElementById('ic_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 必须转矩计算（连续运动，无加速转矩）
 */
async function calculateRequiredTorque() {
    const TLMInput = document.getElementById('rt_TLM').value.trim();
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
    
    const S = SInput === '' ? 1.5 : parseFloat(SInput);
    if (isNaN(S) || S <= 0) {
        showError('安全系数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'required_torque',
        TLM: TLM,
        S: S
    };
    
    try {
        const result = await apiRequest('/api/tools/belt-continuous/calculate', 'POST', params);
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
 * 5. 惯量比计算
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
        const result = await apiRequest('/api/tools/belt-continuous/calculate', 'POST', params);
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

