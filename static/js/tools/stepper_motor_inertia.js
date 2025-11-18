/**
 * 步进电机惯量计算 - 前端计算逻辑
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
 * 1. 滚珠丝杠惯量计算
 */
async function calculateBallScrew() {
    const WInput = document.getElementById('bs_W').value.trim();
    const BPInput = document.getElementById('bs_BP').value.trim();
    const GLInput = document.getElementById('bs_GL').value.trim();
    
    if (WInput === '') {
        showError('请输入可动部分总重量');
        return;
    }
    const W = parseFloat(WInput);
    if (isNaN(W) || W <= 0) {
        showError('可动部分总重量必须大于0');
        return;
    }
    
    if (BPInput === '') {
        showError('请输入丝杠螺距');
        return;
    }
    const BP = parseFloat(BPInput);
    if (isNaN(BP) || BP <= 0) {
        showError('丝杠螺距必须大于0');
        return;
    }
    
    if (GLInput === '') {
        showError('请输入减速比');
        return;
    }
    const GL = parseFloat(GLInput);
    if (isNaN(GL) || GL <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'ball_screw',
        W: W,
        BP: BP,
        GL: GL
    };
    
    try {
        const result = await apiRequest('/api/tools/stepper-motor-inertia/calculate', 'POST', params);
        
        document.getElementById('bs_result_value').textContent = formatNumber(result.result, 10);
        document.getElementById('bs_result_unit').textContent = result.unit;
        renderFormula('bs_result_formula', result.formula);
        document.getElementById('bs_result').style.display = 'block';
        document.getElementById('bs_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 齿条和小齿轮・传送带・链条传动惯量计算
 */
async function calculateRackPinion() {
    const WInput = document.getElementById('rp_W').value.trim();
    const DInput = document.getElementById('rp_D').value.trim();
    const GLInput = document.getElementById('rp_GL').value.trim();
    
    if (WInput === '') {
        showError('请输入可动部分总重量');
        return;
    }
    const W = parseFloat(WInput);
    if (isNaN(W) || W <= 0) {
        showError('可动部分总重量必须大于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入小齿轮/链轮直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('小齿轮/链轮直径必须大于0');
        return;
    }
    
    if (GLInput === '') {
        showError('请输入减速比');
        return;
    }
    const GL = parseFloat(GLInput);
    if (isNaN(GL) || GL <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'rack_pinion',
        W: W,
        D: D,
        GL: GL
    };
    
    try {
        const result = await apiRequest('/api/tools/stepper-motor-inertia/calculate', 'POST', params);
        
        document.getElementById('rp_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('rp_result_unit').textContent = result.unit;
        renderFormula('rp_result_formula', result.formula);
        document.getElementById('rp_result').style.display = 'block';
        document.getElementById('rp_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 旋转体・转盘驱动惯量计算
 */
async function calculateTurntable() {
    const J1Input = document.getElementById('tt_J1').value.trim();
    const WInput = document.getElementById('tt_W').value.trim();
    const LInput = document.getElementById('tt_L').value.trim();
    const GLInput = document.getElementById('tt_GL').value.trim();
    
    if (J1Input === '') {
        showError('请输入转盘的惯性矩');
        return;
    }
    const J1 = parseFloat(J1Input);
    if (isNaN(J1) || J1 < 0) {
        showError('转盘的惯性矩必须大于等于0');
        return;
    }
    
    if (WInput === '') {
        showError('请输入转盘上物体的重量');
        return;
    }
    const W = parseFloat(WInput);
    if (isNaN(W) || W <= 0) {
        showError('转盘上物体的重量必须大于0');
        return;
    }
    
    if (LInput === '') {
        showError('请输入物体与旋转轴的距离');
        return;
    }
    const L = parseFloat(LInput);
    if (isNaN(L) || L <= 0) {
        showError('物体与旋转轴的距离必须大于0');
        return;
    }
    
    if (GLInput === '') {
        showError('请输入减速比');
        return;
    }
    const GL = parseFloat(GLInput);
    if (isNaN(GL) || GL <= 0) {
        showError('减速比必须大于0');
        return;
    }
    
    const params = {
        scenario: 'turntable',
        J1: J1,
        W: W,
        L: L,
        GL: GL
    };
    
    try {
        const result = await apiRequest('/api/tools/stepper-motor-inertia/calculate', 'POST', params);
        
        document.getElementById('tt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('tt_result_unit').textContent = result.unit;
        renderFormula('tt_result_formula', result.formula);
        document.getElementById('tt_result').style.display = 'block';
        document.getElementById('tt_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 角加速度计算
 */
async function calculateAngularAcceleration() {
    const nInput = document.getElementById('aa_n').value.trim();
    const deltaTInput = document.getElementById('aa_delta_t').value.trim();
    
    if (nInput === '') {
        showError('请输入转速');
        return;
    }
    const n = parseFloat(nInput);
    if (isNaN(n) || n <= 0) {
        showError('转速必须大于0');
        return;
    }
    
    if (deltaTInput === '') {
        showError('请输入加速时间');
        return;
    }
    const delta_t = parseFloat(deltaTInput);
    if (isNaN(delta_t) || delta_t <= 0) {
        showError('加速时间必须大于0');
        return;
    }
    
    const params = {
        scenario: 'angular_acceleration',
        n: n,
        delta_t: delta_t
    };
    
    try {
        const result = await apiRequest('/api/tools/stepper-motor-inertia/calculate', 'POST', params);
        
        document.getElementById('aa_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('aa_result_unit').textContent = result.unit;
        renderFormula('aa_result_formula', result.formula);
        document.getElementById('aa_result').style.display = 'block';
        document.getElementById('aa_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 电机力矩计算
 */
async function calculateMotorTorque() {
    const JInput = document.getElementById('mt_J').value.trim();
    const epsilonInput = document.getElementById('mt_epsilon').value.trim();
    const TLInput = document.getElementById('mt_T_L').value.trim();
    const etaInput = document.getElementById('mt_eta').value.trim();
    
    if (JInput === '') {
        showError('请输入惯量');
        return;
    }
    const J = parseFloat(JInput);
    if (isNaN(J) || J <= 0) {
        showError('惯量必须大于0');
        return;
    }
    
    if (epsilonInput === '') {
        showError('请输入角加速度');
        return;
    }
    const epsilon = parseFloat(epsilonInput);
    if (isNaN(epsilon) || epsilon <= 0) {
        showError('角加速度必须大于0');
        return;
    }
    
    const T_L = TLInput === '' ? 0 : parseFloat(TLInput);
    if (isNaN(T_L) || T_L < 0) {
        showError('系统外力折算到电机上的力矩必须大于等于0');
        return;
    }
    
    if (etaInput === '') {
        showError('请输入传动系统的效率');
        return;
    }
    const eta = parseFloat(etaInput);
    if (isNaN(eta) || eta <= 0 || eta > 1) {
        showError('传动系统的效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'motor_torque',
        J: J,
        epsilon: epsilon,
        T_L: T_L,
        eta: eta
    };
    
    try {
        const result = await apiRequest('/api/tools/stepper-motor-inertia/calculate', 'POST', params);
        
        document.getElementById('mt_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('mt_result_unit').textContent = result.unit;
        renderFormula('mt_result_formula', result.formula);
        document.getElementById('mt_result').style.display = 'block';
        document.getElementById('mt_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

