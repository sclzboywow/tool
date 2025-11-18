/**
 * 丝杠水平运动选型计算 - 前端计算逻辑
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
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
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
    const Vl = parseFloat(document.getElementById('ms_Vl').value);
    const PB = parseFloat(document.getElementById('ms_PB').value);
    
    if (!Vl || Vl <= 0) {
        showError('请输入有效的速度');
        return;
    }
    if (!PB || PB <= 0) {
        showError('请输入有效的丝杠导程');
        return;
    }
    
    const params = {
        scenario: 'motor_speed',
        Vl: Vl,
        PB: PB
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        document.getElementById('ms_result_value').textContent = formatNumber(result.result, 2);
        document.getElementById('ms_result_unit').textContent = result.unit;
        renderFormula('ms_result_formula', result.formula);
        document.getElementById('ms_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 负荷转矩计算
 */
async function calculateLoadTorque() {
    const FA = parseFloat(document.getElementById('lt_FA').value) || 0;
    const M = parseFloat(document.getElementById('lt_M').value);
    const a = parseFloat(document.getElementById('lt_a').value) || 0;
    const mu = parseFloat(document.getElementById('lt_mu').value) || 0.1;
    const PB = parseFloat(document.getElementById('lt_PB').value);
    const eta = parseFloat(document.getElementById('lt_eta').value) || 0.9;
    
    if (M === undefined || M <= 0) {
        showError('请输入有效的滑动部分质量');
        return;
    }
    if (a < -90 || a > 90) {
        showError('移动方向与水平轴夹角应在-90°到90°之间');
        return;
    }
    if (mu < 0) {
        showError('摩擦系数不能为负数');
        return;
    }
    if (!PB || PB <= 0) {
        showError('请输入有效的丝杠导程');
        return;
    }
    if (eta <= 0 || eta > 1) {
        showError('机械效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'load_torque',
        FA: FA,
        M: M,
        a: a,
        mu: mu,
        PB: PB,
        eta: eta
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        // 解析结果，可能包含F和TL
        if (result.extra && result.extra.F) {
            document.getElementById('lt_F_value').textContent = formatNumber(result.extra.F, 4);
        }
        document.getElementById('lt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('lt_result_unit').textContent = result.unit;
        renderFormula('lt_result_formula', result.formula);
        document.getElementById('lt_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 克服惯量的加速转矩计算
 */
async function calculateAccelerationTorque() {
    const M = parseFloat(document.getElementById('at_M').value);
    const PB = parseFloat(document.getElementById('at_PB').value);
    const LB = parseFloat(document.getElementById('at_LB').value);
    const DB = parseFloat(document.getElementById('at_DB').value);
    const MC = parseFloat(document.getElementById('at_MC').value);
    const DC = parseFloat(document.getElementById('at_DC').value);
    const NM = parseFloat(document.getElementById('at_NM').value);
    const JM = parseFloat(document.getElementById('at_JM').value) || 0.0011;
    const t0 = parseFloat(document.getElementById('at_t0').value);
    
    if (!M || M <= 0) {
        showError('请输入有效的滑动部分质量');
        return;
    }
    if (!PB || PB <= 0) {
        showError('请输入有效的丝杠导程');
        return;
    }
    if (!LB || LB <= 0) {
        showError('请输入有效的丝杠长度');
        return;
    }
    if (!DB || DB <= 0) {
        showError('请输入有效的丝杠直径');
        return;
    }
    if (!MC || MC <= 0) {
        showError('请输入有效的连轴器质量');
        return;
    }
    if (!DC || DC <= 0) {
        showError('请输入有效的连轴器直径');
        return;
    }
    if (!NM || NM <= 0) {
        showError('请输入有效的电机转速');
        return;
    }
    if (!JM || JM <= 0) {
        showError('请输入有效的电机惯量');
        return;
    }
    if (!t0 || t0 <= 0) {
        showError('请输入有效的加速时间');
        return;
    }
    
    const params = {
        scenario: 'acceleration_torque',
        M: M,
        PB: PB,
        LB: LB,
        DB: DB,
        MC: MC,
        DC: DC,
        NM: NM,
        JM: JM,
        t0: t0
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        // 解析结果，可能包含多个值
        if (result.extra) {
            if (result.extra.JL1 !== undefined) {
                document.getElementById('at_JL1_value').textContent = formatNumber(result.extra.JL1, 6);
            }
            if (result.extra.JB !== undefined) {
                document.getElementById('at_JB_value').textContent = formatNumber(result.extra.JB, 6);
            }
            if (result.extra.JC !== undefined) {
                document.getElementById('at_JC_value').textContent = formatNumber(result.extra.JC, 6);
            }
            if (result.extra.JL !== undefined) {
                document.getElementById('at_JL_value').textContent = formatNumber(result.extra.JL, 6);
            }
        }
        document.getElementById('at_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('at_result_unit').textContent = result.unit;
        renderFormula('at_result_formula', result.formula);
        document.getElementById('at_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 必须转矩计算
 */
async function calculateRequiredTorque() {
    const TL = parseFloat(document.getElementById('rt_TL').value);
    const TS = parseFloat(document.getElementById('rt_TS').value);
    const S = parseFloat(document.getElementById('rt_S').value) || 1;
    
    if (TL === undefined || TL < 0) {
        showError('请输入有效的负载转矩');
        return;
    }
    if (TS === undefined || TS < 0) {
        showError('请输入有效的启动转矩');
        return;
    }
    if (!S || S <= 0) {
        showError('安全系数必须大于0');
        return;
    }
    
    const params = {
        scenario: 'required_torque',
        TL: TL,
        TS: TS,
        S: S
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        document.getElementById('rt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('rt_result_unit').textContent = result.unit;
        renderFormula('rt_result_formula', result.formula);
        document.getElementById('rt_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 7. 负荷与电机惯量比计算
 */
async function calculateInertiaRatioMotor() {
    const JLInput = document.getElementById('irm_JL').value.trim();
    const JMInput = document.getElementById('irm_JM').value.trim();
    
    if (JLInput === '' || isNaN(JLInput)) {
        showError('请输入有效的总负荷惯量');
        return;
    }
    
    const JL = parseFloat(JLInput);
    if (isNaN(JL) || JL <= 0) {
        showError('总负荷惯量必须大于0');
        return;
    }
    
    if (JMInput === '' || isNaN(JMInput)) {
        showError('请输入有效的电机惯量');
        return;
    }
    
    const JM = parseFloat(JMInput) || 0.0011;
    if (isNaN(JM) || JM <= 0) {
        showError('电机惯量必须大于0');
        return;
    }
    
    const params = {
        scenario: 'inertia_ratio_motor',
        JL: JL,
        JM: JM
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        document.getElementById('irm_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('irm_result_formula', result.formula);
        
        // 显示警告
        const warningDiv = document.getElementById('irm_warning');
        if (result.result > 5) {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#fff3cd';
            warningDiv.style.borderLeft = '4px solid #ffc107';
            warningDiv.innerHTML = '<strong>警告：</strong>惯量比大于5，建议考虑采用减速装置以提高惯量匹配。';
        } else {
            warningDiv.style.display = 'block';
            warningDiv.style.background = '#d4edda';
            warningDiv.style.borderLeft = '4px solid #28a745';
            warningDiv.innerHTML = '<strong>提示：</strong>惯量比在合理范围内。';
        }
        
        document.getElementById('irm_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 8. 负荷与减速机惯量比计算
 */
async function calculateInertiaRatioReducer() {
    const JLInput = document.getElementById('irr_JL').value.trim();
    const JMInput = document.getElementById('irr_JM').value.trim();
    const iInput = document.getElementById('irr_i').value.trim();
    
    // 验证总负荷惯量
    if (JLInput === '') {
        showError('请输入总负荷惯量');
        return;
    }
    
    const JL = parseFloat(JLInput);
    if (isNaN(JL)) {
        showError('总负荷惯量必须是有效数字');
        return;
    }
    if (JL <= 0) {
        showError('总负荷惯量必须大于0');
        return;
    }
    
    // 验证电机惯量
    if (JMInput === '') {
        showError('请输入电机惯量');
        return;
    }
    
    const JM = parseFloat(JMInput);
    if (isNaN(JM)) {
        showError('电机惯量必须是有效数字');
        return;
    }
    if (JM <= 0) {
        showError('电机惯量必须大于0');
        return;
    }
    
    // 验证减速比
    if (iInput === '') {
        showError('请输入减速机减速比');
        return;
    }
    
    const i = parseFloat(iInput);
    if (isNaN(i)) {
        showError('减速机减速比必须是有效数字');
        return;
    }
    if (i <= 0) {
        showError('减速机减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'inertia_ratio_reducer',
        JL: JL,
        JM: JM,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/screw-horizontal/calculate', 'POST', params);
        document.getElementById('irr_result_value').textContent = formatNumber(result.result, 2);
        renderFormula('irr_result_formula', result.formula);
        document.getElementById('irr_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}
