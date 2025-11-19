/**
 * 不同形状物体惯量计算 - 前端计算逻辑
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
 * 显示错误信息
 */
function showError(message) {
    alert(message);
}

/**
 * 1. 圆柱体惯量计算（平行）
 */
async function calculateCylinderParallel() {
    const d0 = parseFloat(document.getElementById('cp_d0').value);
    const d1 = parseFloat(document.getElementById('cp_d1').value) || 0;
    const L = parseFloat(document.getElementById('cp_L').value);
    const rho = parseFloat(document.getElementById('cp_rho').value);
    const e = parseFloat(document.getElementById('cp_e').value) || 0;
    
    if (!d0 || d0 <= 0) {
        showError('请输入有效的外径');
        return;
    }
    if (d1 < 0) {
        showError('内径不能为负数');
        return;
    }
    if (d1 >= d0) {
        showError('内径必须小于外径');
        return;
    }
    if (!L || L <= 0) {
        showError('请输入有效的长度');
        return;
    }
    if (!rho || rho <= 0) {
        showError('请输入有效的密度');
        return;
    }
    
    const params = {
        scenario: 'cylinder_parallel',
        d0: d0,
        d1: d1,
        L: L,
        rho: rho,
        e: e
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('cp_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('cp_result_unit').textContent = result.unit;
        if (result.mass !== undefined) {
            document.getElementById('cp_mass').textContent = formatNumber(result.mass, 4);
        }
        renderFormula('cp_result_formula', result.formula);
        document.getElementById('cp_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 2. 圆柱体惯量计算（垂直）
 */
async function calculateCylinderPerpendicular() {
    const d0 = parseFloat(document.getElementById('cperp_d0').value);
    const d1 = parseFloat(document.getElementById('cperp_d1').value) || 0;
    const L = parseFloat(document.getElementById('cperp_L').value);
    const rho = parseFloat(document.getElementById('cperp_rho').value);
    const e = parseFloat(document.getElementById('cperp_e').value) || 0;
    
    if (!d0 || d0 <= 0) {
        showError('请输入有效的外径');
        return;
    }
    if (d1 < 0) {
        showError('内径不能为负数');
        return;
    }
    if (d1 >= d0) {
        showError('内径必须小于外径');
        return;
    }
    if (!L || L <= 0) {
        showError('请输入有效的长度');
        return;
    }
    if (!rho || rho <= 0) {
        showError('请输入有效的密度');
        return;
    }
    
    const params = {
        scenario: 'cylinder_perpendicular',
        d0: d0,
        d1: d1,
        L: L,
        rho: rho,
        e: e
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('cperp_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('cperp_result_unit').textContent = result.unit;
        if (result.mass !== undefined) {
            document.getElementById('cperp_mass').textContent = formatNumber(result.mass, 4);
        }
        renderFormula('cperp_result_formula', result.formula);
        document.getElementById('cperp_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 3. 方形物体惯量计算
 */
async function calculateRectangular() {
    const x = parseFloat(document.getElementById('rect_x').value);
    const y = parseFloat(document.getElementById('rect_y').value);
    const z = parseFloat(document.getElementById('rect_z').value);
    const rho = parseFloat(document.getElementById('rect_rho').value);
    const e = parseFloat(document.getElementById('rect_e').value) || 0;
    
    if (!x || x <= 0) {
        showError('请输入有效的长度');
        return;
    }
    if (!y || y <= 0) {
        showError('请输入有效的宽度');
        return;
    }
    if (!z || z <= 0) {
        showError('请输入有效的高度');
        return;
    }
    if (!rho || rho <= 0) {
        showError('请输入有效的密度');
        return;
    }
    
    const params = {
        scenario: 'rectangular',
        x: x,
        y: y,
        z: z,
        rho: rho,
        e: e
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('rect_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('rect_result_unit').textContent = result.unit;
        if (result.mass !== undefined) {
            document.getElementById('rect_mass').textContent = formatNumber(result.mass, 4);
        }
        renderFormula('rect_result_formula', result.formula);
        document.getElementById('rect_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 4. 饼状物体惯量计算
 */
async function calculateDisk() {
    const d = parseFloat(document.getElementById('disk_d').value);
    const h = parseFloat(document.getElementById('disk_h').value);
    const rho = parseFloat(document.getElementById('disk_rho').value);
    const e = parseFloat(document.getElementById('disk_e').value) || 0;
    
    if (!d || d <= 0) {
        showError('请输入有效的直径');
        return;
    }
    if (!h || h <= 0) {
        showError('请输入有效的厚度');
        return;
    }
    if (!rho || rho <= 0) {
        showError('请输入有效的密度');
        return;
    }
    
    const params = {
        scenario: 'disk',
        d: d,
        h: h,
        rho: rho,
        e: e
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('disk_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('disk_result_unit').textContent = result.unit;
        if (result.mass !== undefined) {
            document.getElementById('disk_mass').textContent = formatNumber(result.mass, 4);
        }
        renderFormula('disk_result_formula', result.formula);
        document.getElementById('disk_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 直线运动物体惯量计算
 */
async function calculateLinearMotion() {
    const A = parseFloat(document.getElementById('lm_A').value);
    const m = parseFloat(document.getElementById('lm_m').value);
    
    if (!A || A <= 0) {
        showError('请输入有效的运动量');
        return;
    }
    if (!m || m <= 0) {
        showError('请输入有效的质量');
        return;
    }
    
    const params = {
        scenario: 'linear_motion',
        A: A,
        m: m
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('lm_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('lm_result_unit').textContent = result.unit;
        renderFormula('lm_result_formula', result.formula);
        document.getElementById('lm_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 6. 直接惯量计算
 */
async function calculateDirectInertia() {
    const J0 = parseFloat(document.getElementById('di_J0').value);
    const m = parseFloat(document.getElementById('di_m').value);
    const e = parseFloat(document.getElementById('di_e').value);
    
    if (!J0 || J0 <= 0) {
        showError('请输入有效的惯量');
        return;
    }
    if (!m || m <= 0) {
        showError('请输入有效的质量');
        return;
    }
    if (e === undefined || e < 0) {
        showError('请输入有效的距离');
        return;
    }
    
    const params = {
        scenario: 'direct_inertia',
        J0: J0,
        m: m,
        e: e
    };
    
    try {
        const result = await apiRequest('/api/tools/inertia-calc/calculate', 'POST', params);
        document.getElementById('di_result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('di_result_unit').textContent = result.unit;
        if (result.mass !== undefined) {
            document.getElementById('di_mass').textContent = formatNumber(result.mass, 4);
        }
        renderFormula('di_result_formula', result.formula);
        document.getElementById('di_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

