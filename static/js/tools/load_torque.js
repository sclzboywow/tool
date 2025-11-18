/**
 * 不同驱动机构下负载转矩计算 - 前端计算逻辑
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
 * 1. 滚珠丝杠驱动下负载转矩计算
 */
async function calculateBallScrew() {
    const FAInput = document.getElementById('bs_FA').value.trim();
    const mInput = document.getElementById('bs_m').value.trim();
    const gInput = document.getElementById('bs_g').value.trim();
    const alphaInput = document.getElementById('bs_alpha').value.trim();
    const muInput = document.getElementById('bs_mu').value.trim();
    const PBInput = document.getElementById('bs_PB').value.trim();
    const etaInput = document.getElementById('bs_eta').value.trim();
    const mu0Input = document.getElementById('bs_mu0').value.trim();
    const F0Input = document.getElementById('bs_F0').value.trim();
    const iInput = document.getElementById('bs_i').value.trim();
    
    if (FAInput === '') {
        showError('请输入外力');
        return;
    }
    const FA = parseFloat(FAInput);
    if (isNaN(FA)) {
        showError('外力必须是有效数字');
        return;
    }
    
    if (mInput === '') {
        showError('请输入工作物与工作台的总质量');
        return;
    }
    const m = parseFloat(mInput);
    if (isNaN(m) || m <= 0) {
        showError('工作物与工作台的总质量必须大于0');
        return;
    }
    
    const g = gInput === '' ? 9.807 : parseFloat(gInput);
    if (isNaN(g) || g <= 0) {
        showError('重力加速度必须大于0');
        return;
    }
    
    if (alphaInput === '') {
        showError('请输入倾斜角度');
        return;
    }
    const alpha = parseFloat(alphaInput);
    if (isNaN(alpha)) {
        showError('倾斜角度必须是有效数字');
        return;
    }
    
    if (muInput === '') {
        showError('请输入滑动面的摩擦系数');
        return;
    }
    const mu = parseFloat(muInput);
    if (isNaN(mu) || mu < 0) {
        showError('滑动面的摩擦系数必须大于等于0');
        return;
    }
    
    if (PBInput === '') {
        showError('请输入滚珠螺杆螺距');
        return;
    }
    const PB = parseFloat(PBInput);
    if (isNaN(PB) || PB <= 0) {
        showError('滚珠螺杆螺距必须大于0');
        return;
    }
    
    if (etaInput === '') {
        showError('请输入机械效率');
        return;
    }
    const eta = parseFloat(etaInput);
    if (isNaN(eta) || eta <= 0 || eta > 1) {
        showError('机械效率应在0-1之间');
        return;
    }
    
    if (mu0Input === '') {
        showError('请输入预压螺帽的内部摩擦系数');
        return;
    }
    const mu0 = parseFloat(mu0Input);
    if (isNaN(mu0) || mu0 < 0) {
        showError('预压螺帽的内部摩擦系数必须大于等于0');
        return;
    }
    
    if (F0Input === '') {
        showError('请输入预负载');
        return;
    }
    const F0 = parseFloat(F0Input);
    if (isNaN(F0) || F0 < 0) {
        showError('预负载必须大于等于0');
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
        scenario: 'ball_screw',
        FA: FA,
        m: m,
        g: g,
        alpha: alpha,
        mu: mu,
        PB: PB,
        eta: eta,
        mu0: mu0,
        F0: F0,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/load-torque/calculate', 'POST', params);
        
        if (result.extra && result.extra.F !== undefined) {
            document.getElementById('bs_F_value').textContent = formatNumber(result.extra.F, 10);
        }
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
 * 2. 滑轮驱动下负载转矩计算
 */
async function calculatePulley() {
    const FAInput = document.getElementById('p_FA').value.trim();
    const mInput = document.getElementById('p_m').value.trim();
    const gInput = document.getElementById('p_g').value.trim();
    const muInput = document.getElementById('p_mu').value.trim();
    const DInput = document.getElementById('p_D').value.trim();
    const iInput = document.getElementById('p_i').value.trim();
    
    if (FAInput === '') {
        showError('请输入外力');
        return;
    }
    const FA = parseFloat(FAInput);
    if (isNaN(FA)) {
        showError('外力必须是有效数字');
        return;
    }
    
    if (mInput === '') {
        showError('请输入工作物与工作台的总质量');
        return;
    }
    const m = parseFloat(mInput);
    if (isNaN(m) || m <= 0) {
        showError('工作物与工作台的总质量必须大于0');
        return;
    }
    
    const g = gInput === '' ? 9.807 : parseFloat(gInput);
    if (isNaN(g) || g <= 0) {
        showError('重力加速度必须大于0');
        return;
    }
    
    if (muInput === '') {
        showError('请输入滑动面的摩擦系数');
        return;
    }
    const mu = parseFloat(muInput);
    if (isNaN(mu) || mu < 0) {
        showError('滑动面的摩擦系数必须大于等于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入终段滑轮直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('终段滑轮直径必须大于0');
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
        scenario: 'pulley',
        FA: FA,
        m: m,
        g: g,
        mu: mu,
        D: D,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/load-torque/calculate', 'POST', params);
        
        document.getElementById('p_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('p_result_unit').textContent = result.unit;
        renderFormula('p_result_formula', result.formula);
        document.getElementById('p_result').style.display = 'block';
        document.getElementById('p_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 金属线、皮带齿轮、齿条驱动下负载转矩计算
 */
async function calculateBeltGearRack() {
    const FAInput = document.getElementById('bgr_FA').value.trim();
    const mInput = document.getElementById('bgr_m').value.trim();
    const gInput = document.getElementById('bgr_g').value.trim();
    const alphaInput = document.getElementById('bgr_alpha').value.trim();
    const muInput = document.getElementById('bgr_mu').value.trim();
    const DInput = document.getElementById('bgr_D').value.trim();
    const etaInput = document.getElementById('bgr_eta').value.trim();
    const iInput = document.getElementById('bgr_i').value.trim();
    
    if (FAInput === '') {
        showError('请输入外力');
        return;
    }
    const FA = parseFloat(FAInput);
    if (isNaN(FA)) {
        showError('外力必须是有效数字');
        return;
    }
    
    if (mInput === '') {
        showError('请输入工作物与工作台的总质量');
        return;
    }
    const m = parseFloat(mInput);
    if (isNaN(m) || m <= 0) {
        showError('工作物与工作台的总质量必须大于0');
        return;
    }
    
    const g = gInput === '' ? 9.807 : parseFloat(gInput);
    if (isNaN(g) || g <= 0) {
        showError('重力加速度必须大于0');
        return;
    }
    
    if (alphaInput === '') {
        showError('请输入倾斜角度');
        return;
    }
    const alpha = parseFloat(alphaInput);
    if (isNaN(alpha)) {
        showError('倾斜角度必须是有效数字');
        return;
    }
    
    if (muInput === '') {
        showError('请输入滑动面的摩擦系数');
        return;
    }
    const mu = parseFloat(muInput);
    if (isNaN(mu) || mu < 0) {
        showError('滑动面的摩擦系数必须大于等于0');
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
    
    if (etaInput === '') {
        showError('请输入机械效率');
        return;
    }
    const eta = parseFloat(etaInput);
    if (isNaN(eta) || eta <= 0 || eta > 1) {
        showError('机械效率应在0-1之间');
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
        scenario: 'belt_gear_rack',
        FA: FA,
        m: m,
        g: g,
        alpha: alpha,
        mu: mu,
        D: D,
        eta: eta,
        i: i
    };
    
    try {
        const result = await apiRequest('/api/tools/load-torque/calculate', 'POST', params);
        
        if (result.extra && result.extra.F !== undefined) {
            document.getElementById('bgr_F_value').textContent = formatNumber(result.extra.F, 10);
        }
        document.getElementById('bgr_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('bgr_result_unit').textContent = result.unit;
        renderFormula('bgr_result_formula', result.formula);
        document.getElementById('bgr_result').style.display = 'block';
        document.getElementById('bgr_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 实际测试计算方法
 */
async function calculateTestMethod() {
    const FBInput = document.getElementById('tm_FB').value.trim();
    const DInput = document.getElementById('tm_D').value.trim();
    
    if (FBInput === '') {
        showError('请输入主轴开始运动时的力');
        return;
    }
    const FB = parseFloat(FBInput);
    if (isNaN(FB) || FB <= 0) {
        showError('主轴开始运动时的力必须大于0');
        return;
    }
    
    if (DInput === '') {
        showError('请输入终段滑轮直径');
        return;
    }
    const D = parseFloat(DInput);
    if (isNaN(D) || D <= 0) {
        showError('终段滑轮直径必须大于0');
        return;
    }
    
    const params = {
        scenario: 'test_method',
        FB: FB,
        D: D
    };
    
    try {
        const result = await apiRequest('/api/tools/load-torque/calculate', 'POST', params);
        
        document.getElementById('tm_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('tm_result_unit').textContent = result.unit;
        renderFormula('tm_result_formula', result.formula);
        document.getElementById('tm_result').style.display = 'block';
        document.getElementById('tm_result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

