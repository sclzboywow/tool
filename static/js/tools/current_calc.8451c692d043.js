/**
 * 常用电流计算公式 - 前端计算逻辑
 */

/**
 * 主标签页和子标签页的映射关系
 */
const tabGroupMapping = {
    'pure_resistor': 'current',
    'inductive': 'current',
    'single_phase_motor': 'current',
    'three_phase_motor': 'current',
    'residential': 'current',
    'wire_resistance': 'resistance',
    'busbar_resistance': 'resistance',
    'wire_current_3phase': 'wire_current',
    'wire_current_1phase': 'wire_current',
    'voltage_loss': 'other',
    'voltage_loss_end_load': 'other',
    'voltage_loss_line_voltage': 'other',
    'voltage_loss_percent_formula': 'other',
    'energy_meter': 'other',
    'power_3phase': 'other',
    'power_1phase': 'other',
    'air_conditioner_home': 'other',
    'air_conditioner_large': 'other',
    'refrigeration_unit_convert': 'other'
};

/**
 * 切换主标签页
 */
function switchMainTab(mainTabId) {
    // 移除所有主标签的active类
    const mainTabs = document.querySelectorAll('.main-tab');
    mainTabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 激活选中的主标签（使用data-tab-id属性精确匹配）
    const targetMainTab = document.querySelector(`.main-tab[data-tab-id="${mainTabId}"]`);
    if (targetMainTab) {
        targetMainTab.classList.add('active');
    }
    
    // 隐藏所有子标签组
    const subTabsGroups = document.querySelectorAll('.sub-tabs');
    subTabsGroups.forEach(group => {
        group.classList.remove('active');
    });
    
    // 显示对应的子标签组
    const targetSubTabs = document.getElementById(`sub-tabs-${mainTabId}`);
    if (targetSubTabs) {
        targetSubTabs.classList.add('active');
        
        // 自动激活该组的第一个子标签
        const firstSubTab = targetSubTabs.querySelector('.sub-tab');
        if (firstSubTab) {
            const onclick = firstSubTab.getAttribute('onclick');
            if (onclick) {
                const match = onclick.match(/switchSubTab\('([^']+)'\)/);
                if (match && match[1]) {
                    switchSubTab(match[1]);
                }
            }
        }
    }
}

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
    
    // 确保对应的主标签也被激活
    const mainTabId = tabGroupMapping[tabName];
    if (mainTabId) {
        // 移除所有主标签的active类
        const mainTabs = document.querySelectorAll('.main-tab');
        mainTabs.forEach(tab => {
            tab.classList.remove('active');
        });
        
        // 使用data-tab-id属性精确匹配并激活对应的主标签
        const targetMainTab = document.querySelector(`.main-tab[data-tab-id="${mainTabId}"]`);
        if (targetMainTab) {
            targetMainTab.classList.add('active');
        }
        
        // 显示对应的子标签组
        const subTabsGroups = document.querySelectorAll('.sub-tabs');
        subTabsGroups.forEach(group => {
            group.classList.remove('active');
        });
        const targetSubTabs = document.getElementById(`sub-tabs-${mainTabId}`);
        if (targetSubTabs) {
            targetSubTabs.classList.add('active');
        }
    }
}

/**
 * 兼容旧的switchTab函数（向后兼容）
 */
function switchTab(tabName) {
    switchSubTab(tabName);
}

/**
 * 1. 纯电阻负荷计算 (前端计算)
 * 公式: I = P / U
 */
function calculatePureResistor() {
    const power = parseFloat(document.getElementById('pr_power').value);
    const voltage = parseFloat(document.getElementById('pr_voltage').value);
    
    // 验证输入
    if (!power || power <= 0) {
        showError('请输入有效的功率值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    
    // 计算
    const result = power / voltage;
    
    // 显示结果
    document.getElementById('pr_result_value').textContent = formatNumber(result);
    document.getElementById('pr_result_unit').textContent = 'A';
    document.getElementById('pr_result_formula').textContent = '公式: I = P / U';
    document.getElementById('pr_result').style.display = 'block';
}

/**
 * 2. 感性负荷计算 (前端计算)
 * 公式: I = P / (U × cosφ)
 */
function calculateInductive() {
    const power = parseFloat(document.getElementById('ind_power').value);
    const voltage = parseFloat(document.getElementById('ind_voltage').value);
    const cosPhi = parseFloat(document.getElementById('ind_cos_phi').value);
    
    // 验证输入
    if (!power || power <= 0) {
        showError('请输入有效的功率值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数 (0-1之间)');
        return;
    }
    
    // 计算
    const result = power / (voltage * cosPhi);
    
    // 显示结果
    document.getElementById('ind_result_value').textContent = formatNumber(result);
    document.getElementById('ind_result_unit').textContent = 'A';
    document.getElementById('ind_result_formula').textContent = '公式: I = P / (U × cosφ)';
    document.getElementById('ind_result').style.display = 'block';
}

/**
 * 3. 单相电动机计算 (前端计算)
 * 公式: I = P / (U × η × cosφ)
 */
function calculateSinglePhaseMotor() {
    const power = parseFloat(document.getElementById('spm_power').value);
    const voltage = parseFloat(document.getElementById('spm_voltage').value);
    let efficiency = parseFloat(document.getElementById('spm_efficiency').value);
    const cosPhi = parseFloat(document.getElementById('spm_cos_phi').value);
    
    // 验证输入
    if (!power || power <= 0) {
        showError('请输入有效的功率值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    // 效率参数：如果为空或无效，使用默认值0.875
    if (isNaN(efficiency) || efficiency <= 0 || efficiency > 1) {
        if (isNaN(efficiency) || efficiency === 0) {
            efficiency = 0.875; // 默认效率
        } else {
            showError('效率值必须在0-1之间');
            return;
        }
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数 (0-1之间)');
        return;
    }
    
    // 计算：I = P / (U × η × cosφ)
    const result = power / (voltage * efficiency * cosPhi);
    
    // 显示结果
    document.getElementById('spm_result_value').textContent = formatNumber(result);
    document.getElementById('spm_result_unit').textContent = 'A';
    document.getElementById('spm_result_formula').textContent = '公式: I = P / (U × η × cosφ)';
    document.getElementById('spm_result').style.display = 'block';
}

/**
 * 4. 三相电动机计算 (后端计算)
 * 公式: I = P / (√3 × U × η × cosφ)
 */
async function calculateThreePhaseMotor() {
    const power = parseFloat(document.getElementById('tpm_power').value);
    const voltage = parseFloat(document.getElementById('tpm_voltage').value);
    let efficiency = parseFloat(document.getElementById('tpm_efficiency').value);
    const cosPhi = parseFloat(document.getElementById('tpm_cos_phi').value);
    
    // 验证输入
    if (!power || power <= 0) {
        showError('请输入有效的功率值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    // 效率参数：如果为空或无效，使用默认值0.875
    if (isNaN(efficiency) || efficiency <= 0 || efficiency > 1) {
        if (isNaN(efficiency) || efficiency === 0) {
            efficiency = 0.875; // 默认效率
        } else {
            showError('效率值必须在0-1之间');
            return;
        }
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数 (0-1之间)');
        return;
    }
    
    try {
        // 调用后端API：I = P / (√3 × U × η × cosφ)
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'three_phase_motor',
            power: power,
            voltage: voltage,
            efficiency: efficiency,  // 确保效率参数被传递
            cos_phi: cosPhi
        });
        
        // 显示结果
        document.getElementById('tpm_result_value').textContent = formatNumber(result.result);
        document.getElementById('tpm_result_unit').textContent = result.unit;
        renderFormula('tpm_result_formula', result.formula);
        document.getElementById('tpm_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 5. 住宅总负荷计算 (后端计算)
 * 公式: I = (Kc × PΣ) / (U × cosφ)
 */
async function calculateResidential() {
    const totalPower = parseFloat(document.getElementById('res_total_power').value);
    const kc = parseFloat(document.getElementById('res_kc').value);
    const voltage = parseFloat(document.getElementById('res_voltage').value);
    const cosPhi = parseFloat(document.getElementById('res_cos_phi').value);
    
    // 验证输入
    if (!totalPower || totalPower <= 0) {
        showError('请输入有效的总功率值');
        return;
    }
    if (!kc || kc <= 0 || kc > 1) {
        showError('请输入有效的同期系数 (0-1之间)');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数 (0-1之间)');
        return;
    }
    
    try {
        // 调用后端API
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'residential',
            total_power: totalPower,
            kc: kc,
            voltage: voltage,
            cos_phi: cosPhi
        });
        
        // 显示结果
        document.getElementById('res_result_value').textContent = formatNumber(result.result);
        document.getElementById('res_result_unit').textContent = result.unit;
        renderFormula('res_result_formula', result.formula);
        document.getElementById('res_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}


/**
 * 切换导线电阻计算类型
 */
function toggleWireResistanceType() {
    const calcType = document.getElementById('wr_calc_type').value;
    const basicDiv = document.getElementById('wr_basic');
    const tempDiv = document.getElementById('wr_temperature');
    
    if (calcType === 'basic') {
        basicDiv.style.display = 'block';
        tempDiv.style.display = 'none';
    } else {
        basicDiv.style.display = 'none';
        tempDiv.style.display = 'block';
    }
}

/**
 * 6. 导线电阻计算 (后端计算)
 */
async function calculateWireResistance() {
    const calcType = document.getElementById('wr_calc_type').value;
    let params = {};
    
    if (calcType === 'basic') {
        const rho = parseFloat(document.getElementById('wr_rho').value);
        const area = parseFloat(document.getElementById('wr_area').value);
        
        if (!rho || rho <= 0) {
            showError('请输入有效的电阻率');
            return;
        }
        if (!area || area <= 0) {
            showError('请输入有效的截面积');
            return;
        }
        
        params = { scenario: 'wire_resistance', rho: rho, area: area };
    } else {
        const r20 = parseFloat(document.getElementById('wr_r20').value);
        const a20 = parseFloat(document.getElementById('wr_a20').value);
        const temperature = parseFloat(document.getElementById('wr_temperature').value);
        
        if (!r20 || r20 <= 0) {
            showError('请输入有效的20℃时的电阻值');
            return;
        }
        if (!a20) {
            showError('请输入有效的温度系数');
            return;
        }
        if (!temperature) {
            showError('请输入有效的温度值');
            return;
        }
        
        params = { scenario: 'wire_resistance', r20: r20, a20: a20, temperature: temperature };
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('wr_result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('wr_result_unit').textContent = result.unit;
        renderFormula('wr_result_formula', result.formula);
        document.getElementById('wr_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 7. 母线电阻计算 (后端计算)
 */
async function calculateBusbarResistance() {
    const conductivity = parseFloat(document.getElementById('br_conductivity').value);
    const area = parseFloat(document.getElementById('br_area').value);
    
    if (!area || area <= 0) {
        showError('请输入有效的截面积');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'busbar_resistance',
            conductivity: conductivity,
            area: area
        });
        
        document.getElementById('br_result_value').textContent = formatNumber(result.result);
        document.getElementById('br_result_unit').textContent = result.unit;
        renderFormula('br_result_formula', result.formula);
        document.getElementById('br_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 切换三相导线载流计算类型
 */
function toggleWireCurrent3Type() {
    const calcType = document.getElementById('wc3_type').value;
    const powerDiv = document.getElementById('wc3_power');
    const apparentDiv = document.getElementById('wc3_apparent');
    const cosPhiGroup = document.getElementById('wc3_cos_phi_group');
    
    if (calcType === 'power') {
        powerDiv.style.display = 'block';
        apparentDiv.style.display = 'none';
        cosPhiGroup.style.display = 'block';
    } else {
        powerDiv.style.display = 'none';
        apparentDiv.style.display = 'block';
        cosPhiGroup.style.display = 'none';
    }
}

/**
 * 8. 按安全载流量选择导线截面（三相电路）(后端计算)
 */
async function calculateWireCurrent3Phase() {
    const calcType = document.getElementById('wc3_type').value;
    const voltageInput = document.getElementById('wc3_voltage').value.trim();
    const voltage = parseFloat(voltageInput);
    let params = { scenario: 'wire_current_3phase', voltage: voltage };
    
    if (calcType === 'power') {
        const powerInput = document.getElementById('wc3_power_input').value.trim();
        const power = parseFloat(powerInput);
        const cosPhiInput = document.getElementById('wc3_cos_phi').value.trim();
        const cosPhi = parseFloat(cosPhiInput);
        
        if (isNaN(power) || power <= 0 || powerInput === '') {
            showError('请输入有效的功率值');
            return;
        }
        if (isNaN(cosPhi) || cosPhi <= 0 || cosPhi > 1 || cosPhiInput === '') {
            showError('请输入有效的功率因数');
            return;
        }
        
        params.power = power;
        params.cos_phi = cosPhi;
    } else {
        const apparentPowerInput = document.getElementById('wc3_apparent_power').value.trim();
        const apparentPower = parseFloat(apparentPowerInput);
        
        if (isNaN(apparentPower) || apparentPower <= 0 || apparentPowerInput === '') {
            showError('请输入有效的视在功率值');
            return;
        }
        
        params.apparent_power = apparentPower;
    }
    
    if (isNaN(voltage) || voltage <= 0 || voltageInput === '') {
        showError('请输入有效的电压值');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('wc3_result_value').textContent = formatNumber(result.result);
        document.getElementById('wc3_result_unit').textContent = result.unit;
        renderFormula('wc3_result_formula', result.formula);
        document.getElementById('wc3_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 切换单相导线载流计算类型
 */
function toggleWireCurrent1Type() {
    const calcType = document.getElementById('wc1_type').value;
    const powerDiv = document.getElementById('wc1_power');
    const apparentDiv = document.getElementById('wc1_apparent');
    const cosPhiGroup = document.getElementById('wc1_cos_phi_group');
    
    if (calcType === 'power') {
        powerDiv.style.display = 'block';
        apparentDiv.style.display = 'none';
        cosPhiGroup.style.display = 'block';
    } else {
        powerDiv.style.display = 'none';
        apparentDiv.style.display = 'block';
        cosPhiGroup.style.display = 'none';
    }
}

/**
 * 9. 按安全载流量选择导线截面（单相电路）(后端计算)
 */
async function calculateWireCurrent1Phase() {
    const calcType = document.getElementById('wc1_type').value;
    const voltageInput = document.getElementById('wc1_voltage').value.trim();
    const voltage = parseFloat(voltageInput);
    let params = { scenario: 'wire_current_1phase', voltage: voltage };
    
    if (calcType === 'power') {
        const powerInput = document.getElementById('wc1_power_input').value.trim();
        const power = parseFloat(powerInput);
        const cosPhiInput = document.getElementById('wc1_cos_phi').value.trim();
        const cosPhi = parseFloat(cosPhiInput);
        
        if (isNaN(power) || power <= 0 || powerInput === '') {
            showError('请输入有效的功率值');
            return;
        }
        if (isNaN(cosPhi) || cosPhi <= 0 || cosPhi > 1 || cosPhiInput === '') {
            showError('请输入有效的功率因数');
            return;
        }
        
        params.power = power;
        params.cos_phi = cosPhi;
    } else {
        const apparentPowerInput = document.getElementById('wc1_apparent_power').value.trim();
        const apparentPower = parseFloat(apparentPowerInput);
        
        if (isNaN(apparentPower) || apparentPower <= 0 || apparentPowerInput === '') {
            showError('请输入有效的视在功率值');
            return;
        }
        
        params.apparent_power = apparentPower;
    }
    
    if (isNaN(voltage) || voltage <= 0 || voltageInput === '') {
        showError('请输入有效的电压值');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('wc1_result_value').textContent = formatNumber(result.result);
        document.getElementById('wc1_result_unit').textContent = result.unit;
        renderFormula('wc1_result_formula', result.formula);
        document.getElementById('wc1_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 切换电压损失计算类型
 */
function toggleVoltageLossType() {
    const calcType = document.getElementById('vl_type').value;
    const ueGroup = document.getElementById('vl_ue_group');
    
    if (calcType === 'percent') {
        ueGroup.style.display = 'block';
    } else {
        ueGroup.style.display = 'none';
    }
}

/**
 * 10. 电压损失计算 (后端计算)
 */
async function calculateVoltageLoss() {
    const calcType = document.getElementById('vl_type').value;
    const u1 = parseFloat(document.getElementById('vl_u1').value);
    const u2 = parseFloat(document.getElementById('vl_u2').value);
    
    if (!u1) {
        showError('请输入有效的送电端电压');
        return;
    }
    if (!u2) {
        showError('请输入有效的受电端电压');
        return;
    }
    
    let params = { scenario: calcType === 'percent' ? 'voltage_loss_percent' : 'voltage_loss', u1: u1, u2: u2 };
    
    if (calcType === 'percent') {
        const ue = parseFloat(document.getElementById('vl_ue').value);
        if (!ue || ue <= 0) {
            showError('请输入有效的线路额定电压');
            return;
        }
        params.ue = ue;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('vl_result_value').textContent = formatNumber(result.result);
        document.getElementById('vl_result_unit').textContent = result.unit;
        renderFormula('vl_result_formula', result.formula);
        document.getElementById('vl_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 11. 电能表倍率计算 (后端计算)
 */
async function calculateEnergyMeter() {
    const kta = parseFloat(document.getElementById('em_kta').value);
    const ktae = parseFloat(document.getElementById('em_ktae').value) || 1;
    const ktv = parseFloat(document.getElementById('em_ktv').value);
    const ktve = parseFloat(document.getElementById('em_ktve').value) || 1;
    const kj = parseFloat(document.getElementById('em_kj').value) || 1;
    
    if (!kta || kta <= 0) {
        showError('请输入有效的实际电流互感器变比');
        return;
    }
    if (!ktv || ktv <= 0) {
        showError('请输入有效的实际电压互感器变比');
        return;
    }
    if (!ktae || ktae <= 0) {
        showError('电能表铭牌电流互感器变比必须大于0');
        return;
    }
    if (!ktve || ktve <= 0) {
        showError('电能表铭牌电压互感器变比必须大于0');
        return;
    }
    if (!kj || kj <= 0) {
        showError('计能器倍率必须大于0');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'energy_meter_multiplier',
            kta: kta,
            ktae: ktae,
            ktv: ktv,
            ktve: ktve,
            kj: kj
        });
        
        document.getElementById('em_result_value').textContent = formatNumber(result.result);
        document.getElementById('em_result_unit').textContent = result.unit || '';
        renderFormula('em_result_formula', result.formula);
        document.getElementById('em_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 12. 三相功率计算（从电流）(后端计算)
 */
async function calculatePower3Phase() {
    const current = parseFloat(document.getElementById('p3_current').value);
    const voltage = parseFloat(document.getElementById('p3_voltage').value);
    const cosPhi = parseFloat(document.getElementById('p3_cos_phi').value);
    let efficiency = parseFloat(document.getElementById('p3_efficiency').value);
    
    if (!current || current <= 0) {
        showError('请输入有效的电流值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数');
        return;
    }
    // 效率参数：如果为空或无效，使用默认值1.0（但建议用户输入实际效率值）
    if (isNaN(efficiency) || efficiency <= 0 || efficiency > 1) {
        if (isNaN(efficiency) || efficiency === 0) {
            efficiency = 1.0; // 默认效率（无损耗）
        } else {
            showError('效率必须在0-1之间');
            return;
        }
    }
    
    try {
        // 调用后端API：P = √3 × U × I × cosφ × η
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'power_from_current_3phase',
            current: current,
            voltage: voltage,
            cos_phi: cosPhi,
            efficiency: efficiency  // 确保效率参数被传递
        });
        
        document.getElementById('p3_result_value').textContent = formatNumber(result.result);
        document.getElementById('p3_result_unit').textContent = result.unit;
        renderFormula('p3_result_formula', result.formula);
        document.getElementById('p3_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 13. 单相功率计算（从电流）(后端计算)
 */
async function calculatePower1Phase() {
    const current = parseFloat(document.getElementById('p1_current').value);
    const voltage = parseFloat(document.getElementById('p1_voltage').value);
    const cosPhi = parseFloat(document.getElementById('p1_cos_phi').value);
    const efficiency = parseFloat(document.getElementById('p1_efficiency').value) || 1.0;
    
    if (!current || current <= 0) {
        showError('请输入有效的电流值');
        return;
    }
    if (!voltage || voltage <= 0) {
        showError('请输入有效的电压值');
        return;
    }
    if (!cosPhi || cosPhi <= 0 || cosPhi > 1) {
        showError('请输入有效的功率因数');
        return;
    }
    if (efficiency < 0 || efficiency > 1) {
        showError('效率必须在0-1之间');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'power_from_current_1phase',
            current: current,
            voltage: voltage,
            cos_phi: cosPhi,
            efficiency: efficiency
        });
        
        document.getElementById('p1_result_value').textContent = formatNumber(result.result);
        document.getElementById('p1_result_unit').textContent = result.unit;
        renderFormula('p1_result_formula', result.formula);
        document.getElementById('p1_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 14. 家庭用空调器容量选择 (后端计算)
 */
async function calculateAirConditionerHome() {
    const areaInput = document.getElementById('ach_area').value.trim();
    const area = parseFloat(areaInput);
    const unitCapacityInput = document.getElementById('ach_unit_capacity').value.trim();
    const unitCapacity = parseFloat(unitCapacityInput);
    
    if (isNaN(area) || area <= 0 || areaInput === '') {
        showError('请输入有效的房间面积');
        return;
    }
    if (isNaN(unitCapacity) || unitCapacity <= 0 || unitCapacityInput === '') {
        showError('请输入有效的单位面积制冷量');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'air_conditioner_home',
            area: area,
            unit_capacity: unitCapacity
        });
        
        document.getElementById('ach_result_value').textContent = formatNumber(result.result);
        document.getElementById('ach_result_unit').textContent = result.unit;
        renderFormula('ach_result_formula', result.formula);
        document.getElementById('ach_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 切换较大场所空调器容量计算中的人体排热量类型
 */
function toggleAirConditionerLargeX() {
    const xType = document.getElementById('acl_x_type').value;
    document.getElementById('acl_x').value = xType;
}

/**
 * 15. 较大场所用空调器容量选择 (后端计算)
 * 公式: Q = k ( q V + η X + u Qz )
 */
async function calculateAirConditionerLarge() {
    const kInput = document.getElementById('acl_k').value.trim();
    const k = parseFloat(kInput);
    const qInput = document.getElementById('acl_q').value.trim();
    const q = parseFloat(qInput);
    const volumeInput = document.getElementById('acl_volume').value.trim();
    const volume = parseFloat(volumeInput);
    const peopleCountInput = document.getElementById('acl_people_count').value.trim();
    const peopleCount = parseFloat(peopleCountInput) || 0;
    const xInput = document.getElementById('acl_x').value.trim();
    const x = parseFloat(xInput) || 432;
    const uInput = document.getElementById('acl_u').value.trim();
    const u = parseFloat(uInput) || 0;
    const qzInput = document.getElementById('acl_qz').value.trim();
    const qz = parseFloat(qzInput) || 0;
    
    if (isNaN(k) || k <= 0 || kInput === '') {
        showError('请输入有效的容量裕量系数');
        return;
    }
    if (isNaN(q) || q <= 0 || qInput === '') {
        showError('请输入有效的房间所需冷量');
        return;
    }
    if (isNaN(volume) || volume <= 0 || volumeInput === '') {
        showError('请输入有效的房间总容积');
        return;
    }
    if (peopleCount < 0 || isNaN(peopleCount)) {
        showError('房间总人数不能为负数');
        return;
    }
    if (isNaN(x) || x <= 0) {
        showError('请输入有效的人体排热量');
        return;
    }
    if (isNaN(u) || u < 0 || u > 0.6) {
        showError('设备同时使用率和利用率之积应在0~0.6之间');
        return;
    }
    if (isNaN(qz) || qz < 0) {
        showError('房间设备总发热量不能为负数');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'air_conditioner_large',
            k: k,
            q: q,
            volume: volume,
            people_count: peopleCount,
            x: x,
            u: u,
            qz: qz
        });
        
        document.getElementById('acl_result_value').textContent = formatNumber(result.result);
        document.getElementById('acl_result_unit').textContent = result.unit;
        renderFormula('acl_result_formula', result.formula);
        document.getElementById('acl_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 16. 制冷量单位换算 (前端计算)
 */
function convertRefrigerationUnit() {
    const fromUnit = document.getElementById('ruc_from_unit').value;
    const toUnit = document.getElementById('ruc_to_unit').value;
    const valueInput = document.getElementById('ruc_value').value.trim();
    const value = parseFloat(valueInput);
    
    if (isNaN(value) || value < 0 || valueInput === '') {
        showError('请输入有效的数值');
        return;
    }
    
    if (fromUnit === toUnit) {
        showError('从单位和到单位不能相同');
        return;
    }
    
    // 换算系数（以W为基准）
    // 1 W = 0.8598 Kcal/h = 3.412 BTU/h = 3.6 KJ/H
    // 1 Kcal/h = 1.163 W = 3.9683 BTU/h = 4.1886 KJ/H
    // 1 BTU/h = 0.293 W = 0.252 Kcal/h = 1.055 KJ/H
    // 1 KJ/H = 0.278 W = 0.239 Kcal/h = 0.948 BTU/h
    
    // 先转换为W（基准单位）
    let valueInW = 0;
    if (fromUnit === 'W') {
        valueInW = value;
    } else if (fromUnit === 'Kcal/h') {
        valueInW = value * 1.163;
    } else if (fromUnit === 'BTU/h') {
        valueInW = value * 0.293;
    } else if (fromUnit === 'KJ/H') {
        valueInW = value * 0.278;
    }
    
    // 从W转换为目标单位
    let result = 0;
    if (toUnit === 'W') {
        result = valueInW;
    } else if (toUnit === 'Kcal/h') {
        result = valueInW / 1.163;
    } else if (toUnit === 'BTU/h') {
        result = valueInW / 0.293;
    } else if (toUnit === 'KJ/H') {
        result = valueInW / 0.278;
    }
    
    // 显示结果
    document.getElementById('ruc_result_value').textContent = formatNumber(result, 4);
    document.getElementById('ruc_result_unit').textContent = toUnit;
    document.getElementById('ruc_result_formula').textContent = `${value} ${fromUnit} = ${formatNumber(result, 4)} ${toUnit}`;
    document.getElementById('ruc_result').style.display = 'block';
}

/**
 * 切换负荷在末端的线路电压损失计算类型
 */
function toggleVoltageLossEndLoadType() {
    const calcType = document.getElementById('vlel_type').value;
    const powerDiv = document.getElementById('vlel_power');
    const currentDiv = document.getElementById('vlel_current');
    
    if (calcType === 'power') {
        powerDiv.style.display = 'block';
        currentDiv.style.display = 'none';
    } else {
        powerDiv.style.display = 'none';
        currentDiv.style.display = 'block';
    }
}

/**
 * 16. 负荷在末端的线路电压损失计算 (后端计算)
 */
async function calculateVoltageLossEndLoad() {
    const calcType = document.getElementById('vlel_type').value;
    let params = { scenario: 'voltage_loss_end_load' };
    
    if (calcType === 'power') {
        const powerInput = document.getElementById('vlel_power_input').value.trim();
        const power = parseFloat(powerInput);
        const reactivePowerInput = document.getElementById('vlel_reactive_power').value.trim();
        const reactivePower = parseFloat(reactivePowerInput) || null;
        const cosPhiInput = document.getElementById('vlel_cos_phi').value.trim();
        const cosPhi = parseFloat(cosPhiInput) || null;
        const resistanceInput = document.getElementById('vlel_resistance').value.trim();
        const resistance = parseFloat(resistanceInput);
        const reactanceInput = document.getElementById('vlel_reactance').value.trim();
        const reactance = parseFloat(reactanceInput);
        const voltageInput = document.getElementById('vlel_voltage').value.trim();
        const voltage = parseFloat(voltageInput);
        
        if (isNaN(power) || power <= 0 || powerInput === '') {
            showError('请输入有效的有功功率');
            return;
        }
        if (isNaN(resistance) || resistance <= 0 || resistanceInput === '') {
            showError('请输入有效的线路电阻');
            return;
        }
        if (isNaN(reactance) || reactanceInput === '') {
            showError('请输入有效的线路电抗');
            return;
        }
        if (isNaN(voltage) || voltage <= 0 || voltageInput === '') {
            showError('请输入有效的线路电压');
            return;
        }
        if (!reactivePower && (!cosPhi || cosPhi <= 0 || cosPhi > 1)) {
            showError('请提供无功功率或功率因数');
            return;
        }
        
        params.power = power;
        params.resistance = resistance;
        params.reactance = reactance;
        params.voltage = voltage;
        if (reactivePower) {
            params.reactive_power = reactivePower;
        } else if (cosPhi) {
            params.cos_phi = cosPhi;
        }
    } else {
        const currentInput = document.getElementById('vlel_current_input').value.trim();
        const current = parseFloat(currentInput);
        const resistanceInput = document.getElementById('vlel_resistance2').value.trim();
        const resistance = parseFloat(resistanceInput);
        const reactanceInput = document.getElementById('vlel_reactance2').value.trim();
        const reactance = parseFloat(reactanceInput);
        const cosPhiInput = document.getElementById('vlel_cos_phi2').value.trim();
        const cosPhi = parseFloat(cosPhiInput);
        
        if (isNaN(current) || current <= 0 || currentInput === '') {
            showError('请输入有效的电流');
            return;
        }
        if (isNaN(resistance) || resistance <= 0 || resistanceInput === '') {
            showError('请输入有效的线路电阻');
            return;
        }
        if (isNaN(reactance) || reactanceInput === '') {
            showError('请输入有效的线路电抗');
            return;
        }
        if (isNaN(cosPhi) || cosPhi <= 0 || cosPhi > 1 || cosPhiInput === '') {
            showError('请输入有效的功率因数');
            return;
        }
        
        params.current = current;
        params.resistance = resistance;
        params.reactance = reactance;
        params.cos_phi = cosPhi;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('vlel_result_value').textContent = formatNumber(result.result);
        document.getElementById('vlel_result_unit').textContent = result.unit;
        renderFormula('vlel_result_formula', result.formula);
        document.getElementById('vlel_result').style.display = 'block';
        // 绘制电压矢量图
        drawVoltagePhasorDiagram(params, result);
        
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 切换线电压的电压损失计算类型
 */
function toggleVoltageLossLineVoltageType() {
    const calcType = document.getElementById('vllv_type').value;
    const powerDiv = document.getElementById('vllv_power');
    const currentDiv = document.getElementById('vllv_current');
    
    if (calcType === 'power') {
        powerDiv.style.display = 'block';
        currentDiv.style.display = 'none';
    } else {
        powerDiv.style.display = 'none';
        currentDiv.style.display = 'block';
    }
}

/**
 * 17. 线电压的电压损失计算 (后端计算)
 */
async function calculateVoltageLossLineVoltage() {
    const calcType = document.getElementById('vllv_type').value;
    let params = { scenario: 'voltage_loss_line_voltage' };
    
    if (calcType === 'power') {
        const powerInput = document.getElementById('vllv_power_input').value.trim();
        const power = parseFloat(powerInput);
        const reactivePowerInput = document.getElementById('vllv_reactive_power').value.trim();
        const reactivePower = parseFloat(reactivePowerInput) || null;
        const cosPhiInput = document.getElementById('vllv_cos_phi').value.trim();
        const cosPhi = parseFloat(cosPhiInput) || null;
        const resistanceInput = document.getElementById('vllv_resistance').value.trim();
        const resistance = parseFloat(resistanceInput);
        const reactanceInput = document.getElementById('vllv_reactance').value.trim();
        const reactance = parseFloat(reactanceInput);
        const voltageInput = document.getElementById('vllv_voltage').value.trim();
        const voltage = parseFloat(voltageInput);
        
        if (isNaN(power) || power <= 0 || powerInput === '') {
            showError('请输入有效的有功功率');
            return;
        }
        if (isNaN(resistance) || resistance <= 0 || resistanceInput === '') {
            showError('请输入有效的线路电阻');
            return;
        }
        if (isNaN(reactance) || reactanceInput === '') {
            showError('请输入有效的线路电抗');
            return;
        }
        if (isNaN(voltage) || voltage <= 0 || voltageInput === '') {
            showError('请输入有效的受电端电压');
            return;
        }
        if (!reactivePower && (!cosPhi || cosPhi <= 0 || cosPhi > 1)) {
            showError('请提供无功功率或功率因数');
            return;
        }
        
        params.power = power;
        params.resistance = resistance;
        params.reactance = reactance;
        params.voltage = voltage;
        if (reactivePower) {
            params.reactive_power = reactivePower;
        } else if (cosPhi) {
            params.cos_phi = cosPhi;
        }
    } else {
        const currentInput = document.getElementById('vllv_current_input').value.trim();
        const current = parseFloat(currentInput);
        const resistanceInput = document.getElementById('vllv_resistance2').value.trim();
        const resistance = parseFloat(resistanceInput);
        const reactanceInput = document.getElementById('vllv_reactance2').value.trim();
        const reactance = parseFloat(reactanceInput);
        const cosPhiInput = document.getElementById('vllv_cos_phi2').value.trim();
        const cosPhi = parseFloat(cosPhiInput);
        
        if (isNaN(current) || current <= 0 || currentInput === '') {
            showError('请输入有效的电流');
            return;
        }
        if (isNaN(resistance) || resistance <= 0 || resistanceInput === '') {
            showError('请输入有效的线路电阻');
            return;
        }
        if (isNaN(reactance) || reactanceInput === '') {
            showError('请输入有效的线路电抗');
            return;
        }
        if (isNaN(cosPhi) || cosPhi <= 0 || cosPhi > 1 || cosPhiInput === '') {
            showError('请输入有效的功率因数');
            return;
        }
        
        params.current = current;
        params.resistance = resistance;
        params.reactance = reactance;
        params.cos_phi = cosPhi;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', params);
        document.getElementById('vllv_result_value').textContent = formatNumber(result.result);
        document.getElementById('vllv_result_unit').textContent = result.unit;
        renderFormula('vllv_result_formula', result.formula);
        document.getElementById('vllv_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 18. 电压损失率公式计算 (后端计算)
 */
async function calculateVoltageLossPercentFormula() {
    const powerInput = document.getElementById('vlpf_power').value.trim();
    const power = parseFloat(powerInput);
    const resistanceInput = document.getElementById('vlpf_resistance').value.trim();
    const resistance = parseFloat(resistanceInput);
    const reactanceInput = document.getElementById('vlpf_reactance').value.trim();
    const reactance = parseFloat(reactanceInput);
    const cosPhiInput = document.getElementById('vlpf_cos_phi').value.trim();
    const cosPhi = parseFloat(cosPhiInput);
    const ueInput = document.getElementById('vlpf_ue').value.trim();
    const ue = parseFloat(ueInput);
    
    if (isNaN(power) || power <= 0 || powerInput === '') {
        showError('请输入有效的有功功率');
        return;
    }
    if (isNaN(resistance) || resistance <= 0 || resistanceInput === '') {
        showError('请输入有效的线路电阻');
        return;
    }
    if (isNaN(reactance) || reactanceInput === '') {
        showError('请输入有效的线路电抗');
        return;
    }
    if (isNaN(cosPhi) || cosPhi <= 0 || cosPhi > 1 || cosPhiInput === '') {
        showError('请输入有效的功率因数');
        return;
    }
    if (isNaN(ue) || ue <= 0 || ueInput === '') {
        showError('请输入有效的线路额定电压（单位：KV）');
        return;
    }
    
    try {
        const result = await apiRequest('/api/tools/current-calc/calculate', 'POST', {
            scenario: 'voltage_loss_percent_formula',
            power: power,
            resistance: resistance,
            reactance: reactance,
            cos_phi: cosPhi,
            ue_kv: ue
        });
        
        document.getElementById('vlpf_result_value').textContent = formatNumber(result.result);
        document.getElementById('vlpf_result_unit').textContent = result.unit;
        renderFormula('vlpf_result_formula', result.formula);
        document.getElementById('vlpf_result').style.display = 'block';
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

/**
 * 绘制电压矢量图
 */
function drawVoltagePhasorDiagram(params, result) {
        const svg = document.getElementById('vlel_phasor_svg');
        if (!svg) return;
        
        // 清空SVG
        svg.innerHTML = '';
        
        // 获取参数
        let U2, I, R, X, cosPhi, sinPhi, phi;
        
        if (params.current !== undefined) {
            // 使用电流计算方式
            I = params.current;
            R = params.resistance;
            X = params.reactance;
            cosPhi = params.cos_phi;
            sinPhi = Math.sqrt(1 - cosPhi * cosPhi);
            phi = Math.acos(cosPhi);
            // 如果提供了电压，使用它；否则使用默认值220V（相电压）
            // 注意：根据公式说明，这里应该是相电压
            U2 = params.voltage || 220; // 相电压默认220V
        } else {
            // 使用功率计算方式
            const P = params.power * 1000; // 转换为W
            const U = params.voltage; // 相电压（根据公式说明，这是相电压）
            
            // 如果有无功功率，从无功功率计算cosPhi
            if (params.reactive_power) {
                const Q = params.reactive_power * 1000; // 转换为Var
                const S = Math.sqrt(P * P + Q * Q); // 视在功率
                cosPhi = P / S;
            } else {
                cosPhi = params.cos_phi || 0.85;
            }
            
            sinPhi = Math.sqrt(1 - cosPhi * cosPhi);
            phi = Math.acos(cosPhi);
            R = params.resistance;
            X = params.reactance;
            
            // 计算电流：P = U × I × cosφ (单相，相电压)
            U2 = U; // 相电压
            I = P / (U2 * cosPhi);
        }
        
        // 验证参数
        if (!U2 || !I || !R || isNaN(X) || !cosPhi) {
            console.error('绘制矢量图参数错误:', { U2, I, R, X, cosPhi, params });
            return;
        }
        
        // 调试信息
        console.log('绘制矢量图参数:', { U2, I, R, X, cosPhi, sinPhi, phi: phi * 180 / Math.PI });
        
        // 计算各个分量
        const IR = I * R;  // 电阻压降
        const IX = I * X;  // 电抗压降
        const IRcosPhi = IR * cosPhi;  // IR的水平分量
        const IRsinPhi = IR * sinPhi;  // IR的垂直分量
        const IXcosPhi = IX * cosPhi;  // IX的垂直分量
        const IXsinPhi = IX * sinPhi;  // IX的水平分量
        
        // 计算U1（送电端电压）
        // U1 = U2 + IR + IX（矢量相加）
        const U1x = U2 + IRcosPhi + IXsinPhi;  // U1的水平分量
        const U1y = IXcosPhi - IRsinPhi;  // U1的垂直分量（向上为正）
        const U1 = Math.sqrt(U1x * U1x + U1y * U1y);
        
        // SVG坐标系设置
        const originX = 100;
        const originY = 350;
        
        // 动态计算缩放因子，使图形适合SVG（宽度约500px）
        // 找到最大的矢量长度作为参考
        const maxLength = Math.max(U2, U1, IR, IX, I * 10);
        const scale = 400 / maxLength;  // 使最大矢量约400px
        
        // 计算U2的长度（水平向右）
        const U2Length = U2 * scale;
        
        // 计算I的角度（相对于U2，向下为正角度）
        const IAngle = phi;  // φ角，I在U2下方
        const ILength = I * scale * 0.5;  // 电流矢量长度（适当缩放以便显示）
        
        // 计算IR和IX的长度
        const IRLength = IR * scale;
        const IXLength = IX * scale;
        
        // 绘制坐标轴
        const axisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        axisGroup.setAttribute('class', 'axis-group');
        
        // 水平轴（U2方向）
        const xAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        xAxis.setAttribute('x1', originX - 50);
        xAxis.setAttribute('y1', originY);
        xAxis.setAttribute('x2', originX + 500);
        xAxis.setAttribute('y2', originY);
        xAxis.setAttribute('stroke', '#ccc');
        xAxis.setAttribute('stroke-width', '1');
        xAxis.setAttribute('stroke-dasharray', '3,3');
        axisGroup.appendChild(xAxis);
        
        // 垂直轴
        const yAxis = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        yAxis.setAttribute('x1', originX);
        yAxis.setAttribute('y1', originY - 200);
        yAxis.setAttribute('x2', originX);
        yAxis.setAttribute('y2', originY + 50);
        yAxis.setAttribute('stroke', '#ccc');
        yAxis.setAttribute('stroke-width', '1');
        yAxis.setAttribute('stroke-dasharray', '3,3');
        axisGroup.appendChild(yAxis);
        
        svg.appendChild(axisGroup);
        
        // 绘制U2（水平向右）
        const U2Group = drawPhasor(svg, originX, originY, U2Length, 0, '#3498db', 'U₂', 'end');
        
        // 绘制I（与U2夹角φ，向下）
        const IEndX = originX + ILength * Math.cos(IAngle);
        const IEndY = originY + ILength * Math.sin(IAngle);
        const IGroup = drawPhasor(svg, originX, originY, ILength, IAngle, '#e74c3c', 'I', 'end');
        
        // 绘制IR（从U2末端开始，与I平行）
        const U2EndX = originX + U2Length;
        const U2EndY = originY;
        const IREndX = U2EndX + IRLength * Math.cos(IAngle);
        const IREndY = U2EndY + IRLength * Math.sin(IAngle);
        const IRGroup = drawPhasor(svg, U2EndX, U2EndY, IRLength, IAngle, '#27ae60', 'IR', 'middle');
        
        // 绘制IX（从IR末端开始）
        // 根据公式：U1x = U2 + IRcosφ + IXsinφ, U1y = IXcosφ - IRsinφ
        // 说明IX在U2方向的分量是IXsinφ（正方向），垂直方向的分量是IXcosφ（向上，Y值减小）
        // 如果I的角度是φ（向下），IX的角度应该是使得：
        //   IX_x = IX * cos(IXAngle) = IXsinφ  => cos(IXAngle) = sinφ
        //   IX_y = IX * sin(IXAngle) = -IXcosφ (向上，Y值减小) => sin(IXAngle) = -cosφ
        // 验证：cos(φ - π/2) = sin(φ), sin(φ - π/2) = -cos(φ)
        // 所以：IXAngle = IAngle - Math.PI/2 = φ - π/2
        const IXAngle = IAngle - Math.PI / 2;  // 使得cos(IXAngle)=sinφ, sin(IXAngle)=-cosφ
        const IXEndX = IREndX + IXLength * Math.cos(IXAngle);
        const IXEndY = IREndY + IXLength * Math.sin(IXAngle);
        const IXGroup = drawPhasor(svg, IREndX, IREndY, IXLength, IXAngle, '#3498db', 'IX', 'middle');
        
        // 绘制U1（从原点到IX末端，即U2 + IR + IX的合成）
        const U1Angle = Math.atan2(IXEndY - originY, IXEndX - originX);
        const U1Length = U1 * scale;
        const U1Group = drawPhasor(svg, originX, originY, U1Length, U1Angle, '#9b59b6', 'U₁', 'end');
        
        // 绘制分量线（虚线）
        // IR的水平分量
        const IRcosPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        IRcosPhiLine.setAttribute('x1', U2EndX);
        IRcosPhiLine.setAttribute('y1', U2EndY);
        IRcosPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale);
        IRcosPhiLine.setAttribute('y2', U2EndY);
        IRcosPhiLine.setAttribute('stroke', '#27ae60');
        IRcosPhiLine.setAttribute('stroke-width', '1.5');
        IRcosPhiLine.setAttribute('stroke-dasharray', '5,5');
        IRcosPhiLine.setAttribute('opacity', '0.6');
        svg.appendChild(IRcosPhiLine);
        
        // IR的垂直分量
        const IRsinPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        IRsinPhiLine.setAttribute('x1', U2EndX + IRcosPhi * scale);
        IRsinPhiLine.setAttribute('y1', U2EndY);
        IRsinPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale);
        IRsinPhiLine.setAttribute('y2', U2EndY + IRsinPhi * scale);
        IRsinPhiLine.setAttribute('stroke', '#27ae60');
        IRsinPhiLine.setAttribute('stroke-width', '1.5');
        IRsinPhiLine.setAttribute('stroke-dasharray', '5,5');
        IRsinPhiLine.setAttribute('opacity', '0.6');
        svg.appendChild(IRsinPhiLine);
        
        // IX的水平分量
        const IXsinPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        IXsinPhiLine.setAttribute('x1', U2EndX + IRcosPhi * scale);
        IXsinPhiLine.setAttribute('y1', U2EndY);
        IXsinPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale + IXsinPhi * scale);
        IXsinPhiLine.setAttribute('y2', U2EndY);
        IXsinPhiLine.setAttribute('stroke', '#f39c12');
        IXsinPhiLine.setAttribute('stroke-width', '1.5');
        IXsinPhiLine.setAttribute('stroke-dasharray', '5,5');
        IXsinPhiLine.setAttribute('opacity', '0.6');
        svg.appendChild(IXsinPhiLine);
        
        // IX的垂直分量
        const IXcosPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        IXcosPhiLine.setAttribute('x1', U2EndX + IRcosPhi * scale + IXsinPhi * scale);
        IXcosPhiLine.setAttribute('y1', U2EndY);
        IXcosPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale + IXsinPhi * scale);
        IXcosPhiLine.setAttribute('y2', U2EndY - IXcosPhi * scale);
        IXcosPhiLine.setAttribute('stroke', '#f39c12');
        IXcosPhiLine.setAttribute('stroke-width', '1.5');
        IXcosPhiLine.setAttribute('stroke-dasharray', '5,5');
        IXcosPhiLine.setAttribute('opacity', '0.6');
        svg.appendChild(IXcosPhiLine);
        
        // 标注分量
        addLabel(svg, U2EndX + IRcosPhi * scale / 2, U2EndY - 10, 'IRcosφ', '#27ae60', 12);
        addLabel(svg, U2EndX + IRcosPhi * scale + 5, U2EndY + IRsinPhi * scale / 2, 'IRsinφ', '#27ae60', 12);
        addLabel(svg, U2EndX + IRcosPhi * scale + IXsinPhi * scale / 2, U2EndY - 10, 'IXsinφ', '#f39c12', 12);
        addLabel(svg, U2EndX + IRcosPhi * scale + IXsinPhi * scale + 5, U2EndY - IXcosPhi * scale / 2, 'IXcosφ', '#f39c12', 12);
        
        // 绘制角度φ
        const phiArcRadius = 40;
        const phiArc = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const phiArcStartX = originX + phiArcRadius;
        const phiArcStartY = originY;
        const phiArcEndX = originX + phiArcRadius * Math.cos(IAngle);
        const phiArcEndY = originY + phiArcRadius * Math.sin(IAngle);
        phiArc.setAttribute('d', `M ${phiArcStartX} ${phiArcStartY} A ${phiArcRadius} ${phiArcRadius} 0 0 1 ${phiArcEndX} ${phiArcEndY}`);
        phiArc.setAttribute('stroke', '#7f8c8d');
        phiArc.setAttribute('stroke-width', '1.5');
        phiArc.setAttribute('fill', 'none');
        svg.appendChild(phiArc);
        
        // 标注角度φ
        addLabel(svg, originX + phiArcRadius * 1.3 * Math.cos(IAngle / 2), originY + phiArcRadius * 1.3 * Math.sin(IAngle / 2), 'φ', '#7f8c8d', 14);
        
        // 标注原点O
        addLabel(svg, originX - 20, originY + 5, 'O', '#2c3e50', 14);
        
        // 添加图例
        const legendX = 600;
        const legendY = 50;
        const legendGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        legendGroup.setAttribute('class', 'legend');
        
        const legendItems = [
            { color: '#3498db', label: 'U₂ - 受电端电压' },
            { color: '#9b59b6', label: 'U₁ - 送电端电压' },
            { color: '#e74c3c', label: 'I - 电流' },
            { color: '#27ae60', label: 'IR - 电阻压降' },
            { color: '#f39c12', label: 'IX - 电抗压降' }
        ];
        
        legendItems.forEach((item, index) => {
            const legendLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            legendLine.setAttribute('x1', legendX);
            legendLine.setAttribute('y1', legendY + index * 25);
            legendLine.setAttribute('x2', legendX + 30);
            legendLine.setAttribute('y2', legendY + index * 25);
            legendLine.setAttribute('stroke', item.color);
            legendLine.setAttribute('stroke-width', '3');
            legendGroup.appendChild(legendLine);
            
            const legendText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            legendText.setAttribute('x', legendX + 35);
            legendText.setAttribute('y', legendY + index * 25 + 5);
            legendText.setAttribute('fill', '#2c3e50');
            legendText.setAttribute('font-size', '12');
            legendText.textContent = item.label;
            legendGroup.appendChild(legendText);
        });
        
        svg.appendChild(legendGroup);
    
    /**
     * 绘制一个矢量（带箭头和标签）
     */
    function drawPhasor(svg, x1, y1, length, angle, color, label, labelPos) {
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        
        const x2 = x1 + length * Math.cos(angle);
        const y2 = y1 + length * Math.sin(angle);
        
        // 绘制矢量线
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', color);
        line.setAttribute('stroke-width', '3');
        line.setAttribute('class', 'phasor-line');
        group.appendChild(line);
        
        // 绘制箭头
        const arrowLength = 10;
        const arrowAngle = Math.PI / 6;
        const arrow1X = x2 - arrowLength * Math.cos(angle - arrowAngle);
        const arrow1Y = y2 - arrowLength * Math.sin(angle - arrowAngle);
        const arrow2X = x2 - arrowLength * Math.cos(angle + arrowAngle);
        const arrow2Y = y2 - arrowLength * Math.sin(angle + arrowAngle);
        
        const arrow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        arrow.setAttribute('d', `M ${x2} ${y2} L ${arrow1X} ${arrow1Y} L ${arrow2X} ${arrow2Y} Z`);
        arrow.setAttribute('fill', color);
        arrow.setAttribute('class', 'phasor-arrow');
        group.appendChild(arrow);
        
        // 添加标签
        let labelX, labelY;
        if (labelPos === 'end') {
            labelX = x2 + 10 * Math.cos(angle);
            labelY = y2 + 10 * Math.sin(angle);
        } else if (labelPos === 'middle') {
            labelX = (x1 + x2) / 2 + 10 * Math.cos(angle + Math.PI / 2);
            labelY = (y1 + y2) / 2 + 10 * Math.sin(angle + Math.PI / 2);
        } else {
            labelX = x1 + 10 * Math.cos(angle);
            labelY = y1 + 10 * Math.sin(angle);
        }
        
        addLabel(svg, labelX, labelY, label, color, 14);
        
        svg.appendChild(group);
        return group;
    }
    
    /**
     * 添加文本标签
     */
    function addLabel(svg, x, y, text, color, fontSize) {
        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', x);
        label.setAttribute('y', y);
        label.setAttribute('fill', color || '#2c3e50');
        label.setAttribute('font-size', fontSize || '14');
        label.setAttribute('font-weight', '500');
        label.setAttribute('class', 'phasor-label');
        
        // 处理下标（如U₂）
        if (text.includes('₂') || text.includes('₁')) {
            const tspan1 = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
            tspan1.textContent = text.substring(0, text.length - 1);
            label.appendChild(tspan1);
            
            const tspan2 = document.createElementNS('http://www.w3.org/2000/svg', 'tspan');
            tspan2.setAttribute('baseline-shift', 'sub');
            tspan2.setAttribute('font-size', (fontSize * 0.7) + 'px');
            tspan2.textContent = text.substring(text.length - 1);
            label.appendChild(tspan2);
        } else {
            label.textContent = text;
        }
        
        svg.appendChild(label);
        return label;
    }
}

/**
 * 绘制固定说明用的电压矢量图（使用示例参数）
 */
function drawFixedPhasorDiagram() {
    const svg = document.getElementById('fixed_phasor_diagram');
    if (!svg) return;
    
    // 清空SVG
    svg.innerHTML = '';
    
    // 使用示例参数进行计算
    const U2 = 220;  // 受电端电压 (V)
    const I = 100;   // 电流 (A)
    const R = 0.1;   // 电阻 (Ω)
    const X = 0.05;  // 电抗 (Ω)
    const cosPhi = 0.85;  // 功率因数
    const sinPhi = Math.sqrt(1 - cosPhi * cosPhi);
    const phi = Math.acos(cosPhi);
    
    // 根据公式计算各个分量
    const IR = I * R;  // 电阻压降
    const IX = I * X;  // 电抗压降
    const IRcosPhi = IR * cosPhi;  // IR的水平分量
    const IRsinPhi = IR * sinPhi;  // IR的垂直分量
    const IXcosPhi = IX * cosPhi;  // IX的垂直分量
    const IXsinPhi = IX * sinPhi;  // IX的水平分量
    
    // 计算U1（送电端电压）
    // U1 = U2 + IR + IX（矢量相加）
    const U1x = U2 + IRcosPhi + IXsinPhi;  // U1的水平分量
    const U1y = IXcosPhi - IRsinPhi;  // U1的垂直分量（向上为正）
    const U1 = Math.sqrt(U1x * U1x + U1y * U1y);
    
    // SVG坐标系设置
    const originX = 100;
    const originY = 300;
    
    // 动态计算缩放因子，使图形适合SVG
    const maxLength = Math.max(U2, U1, IR, IX, I * 0.5);
    const scale = 350 / maxLength;  // 使最大矢量约350px
    
        // 根据图片重新理解：I是参考矢量（水平向右），U2滞后I角度φ
        // 在SVG坐标系中，Y轴向下为正，角度逆时针为正
        // I：水平向右（角度0）
        // U2：滞后I角度φ（向上向右，角度为-φ）
        // IR：与I同相（水平向右，角度0）
        // IX：超前IR 90度（垂直向上，角度-π/2）
        
        const IAngle = 0;  // I是参考矢量，水平向右
        const U2Angle = -phi;  // U2滞后I角度φ（向上向右，负角度）
        const IRAngle = 0;  // IR与I同相（水平向右）
        const IXAngle = -Math.PI / 2;  // IX超前IR 90度（垂直向上）
        
        const U2Length = U2 * scale;
        const ILength = I * scale * 0.3;  // 电流矢量长度（适当缩放）
        const IRLength = IR * scale;
        const IXLength = IX * scale;
        const U1Length = U1 * scale;
    
    // 定义和标记
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    
    // 网格背景
    const gridPattern = document.createElementNS('http://www.w3.org/2000/svg', 'pattern');
    gridPattern.setAttribute('id', 'fixed-grid');
    gridPattern.setAttribute('width', '20');
    gridPattern.setAttribute('height', '20');
    gridPattern.setAttribute('patternUnits', 'userSpaceOnUse');
    const gridPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    gridPath.setAttribute('d', 'M 20 0 L 0 0 0 20');
    gridPath.setAttribute('fill', 'none');
    gridPath.setAttribute('stroke', '#e0e0e0');
    gridPath.setAttribute('stroke-width', '0.5');
    gridPattern.appendChild(gridPath);
    defs.appendChild(gridPattern);
    
    // 箭头标记
    const markers = [
        { id: 'fixed-arrow-blue', color: '#3498db' },
        { id: 'fixed-arrow-green', color: '#27ae60' },
        { id: 'fixed-arrow-purple', color: '#9b59b6' },
        { id: 'fixed-arrow-red', color: '#e74c3c', size: 8 }
    ];
    
    markers.forEach(m => {
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', m.id);
        marker.setAttribute('markerWidth', m.size || 10);
        marker.setAttribute('markerHeight', m.size || 10);
        marker.setAttribute('refX', (m.size || 10) - 1);
        marker.setAttribute('refY', (m.size || 10) / 2);
        marker.setAttribute('orient', 'auto');
        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        const size = m.size || 10;
        polygon.setAttribute('points', `0 0, ${size} ${size/2}, 0 ${size}`);
        polygon.setAttribute('fill', m.color);
        marker.appendChild(polygon);
        defs.appendChild(marker);
    });
    
    svg.appendChild(defs);
    
    // 绘制网格背景
    const gridRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    gridRect.setAttribute('width', '100%');
    gridRect.setAttribute('height', '100%');
    gridRect.setAttribute('fill', 'url(#fixed-grid)');
    svg.appendChild(gridRect);
    
    // 绘制坐标原点
    const originCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    originCircle.setAttribute('cx', originX);
    originCircle.setAttribute('cy', originY);
    originCircle.setAttribute('r', '4');
    originCircle.setAttribute('fill', '#2c3e50');
    svg.appendChild(originCircle);
    
    const originText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    originText.setAttribute('x', originX - 15);
    originText.setAttribute('y', originY + 15);
    originText.setAttribute('fill', '#2c3e50');
    originText.setAttribute('font-size', '14');
    originText.setAttribute('font-weight', 'bold');
    originText.textContent = 'O';
    svg.appendChild(originText);
    
    // 绘制I（参考矢量，水平向右）
    const IEndX = originX + ILength;
    const IEndY = originY;
    const ILine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    ILine.setAttribute('x1', originX);
    ILine.setAttribute('y1', originY);
    ILine.setAttribute('x2', IEndX);
    ILine.setAttribute('y2', IEndY);
    ILine.setAttribute('stroke', '#3498db');
    ILine.setAttribute('stroke-width', '3');
    ILine.setAttribute('marker-end', 'url(#fixed-arrow-blue)');
    svg.appendChild(ILine);
    
    const ILabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    ILabel.setAttribute('x', IEndX + 10);
    ILabel.setAttribute('y', IEndY + 5);
    ILabel.setAttribute('fill', '#3498db');
    ILabel.setAttribute('font-size', '16');
    ILabel.setAttribute('font-weight', 'bold');
    ILabel.textContent = 'I';
    svg.appendChild(ILabel);
    
    // 绘制U2（滞后I角度φ，向上向右）
    const U2EndX = originX + U2Length * Math.cos(U2Angle);
    const U2EndY = originY + U2Length * Math.sin(U2Angle);
    const U2Line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    U2Line.setAttribute('x1', originX);
    U2Line.setAttribute('y1', originY);
    U2Line.setAttribute('x2', U2EndX);
    U2Line.setAttribute('y2', U2EndY);
    U2Line.setAttribute('stroke', '#9b59b6');
    U2Line.setAttribute('stroke-width', '3');
    U2Line.setAttribute('marker-end', 'url(#fixed-arrow-purple)');
    svg.appendChild(U2Line);
    
    const U2Label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    U2Label.setAttribute('x', U2EndX + 10);
    U2Label.setAttribute('y', U2EndY - 5);
    U2Label.setAttribute('fill', '#9b59b6');
    U2Label.setAttribute('font-size', '16');
    U2Label.setAttribute('font-weight', 'bold');
    U2Label.textContent = 'U₂';
    svg.appendChild(U2Label);
    
    // 绘制角度φ（从I到U2）
    const phiArcRadius = 30;
    const phiArc = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const phiArcStartX = originX + phiArcRadius;
    const phiArcStartY = originY;
    const phiArcEndX = originX + phiArcRadius * Math.cos(U2Angle);
    const phiArcEndY = originY + phiArcRadius * Math.sin(U2Angle);
    phiArc.setAttribute('d', `M ${phiArcStartX} ${phiArcStartY} A ${phiArcRadius} ${phiArcRadius} 0 0 0 ${phiArcEndX} ${phiArcEndY}`);
    phiArc.setAttribute('stroke', '#7f8c8d');
    phiArc.setAttribute('stroke-width', '1.5');
    phiArc.setAttribute('fill', 'none');
    svg.appendChild(phiArc);
    
    const phiLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    phiLabel.setAttribute('x', originX + phiArcRadius * 1.3 * Math.cos(U2Angle / 2));
    phiLabel.setAttribute('y', originY + phiArcRadius * 1.3 * Math.sin(U2Angle / 2));
    phiLabel.setAttribute('fill', '#7f8c8d');
    phiLabel.setAttribute('font-size', '14');
    phiLabel.textContent = 'φ';
    svg.appendChild(phiLabel);
    
    // 绘制IR（从U2末端开始，与I同相，水平向右）
    const IREndX = U2EndX + IRLength;
    const IREndY = U2EndY;
    const IRLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IRLine.setAttribute('x1', U2EndX);
    IRLine.setAttribute('y1', U2EndY);
    IRLine.setAttribute('x2', IREndX);
    IRLine.setAttribute('y2', IREndY);
    IRLine.setAttribute('stroke', '#27ae60');
    IRLine.setAttribute('stroke-width', '3');
    IRLine.setAttribute('marker-end', 'url(#fixed-arrow-green)');
    svg.appendChild(IRLine);
    
    const IRLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IRLabel.setAttribute('x', IREndX + 10);
    IRLabel.setAttribute('y', IREndY + 15);
    IRLabel.setAttribute('fill', '#27ae60');
    IRLabel.setAttribute('font-size', '16');
    IRLabel.setAttribute('font-weight', 'bold');
    IRLabel.textContent = 'IR';
    svg.appendChild(IRLabel);
    
    // 绘制IX（从IR末端开始，垂直向上）
    const IXEndX = IREndX;
    const IXEndY = IREndY + IXLength * Math.sin(IXAngle);  // IXAngle = -π/2，sin(-π/2) = -1，所以Y值减小（向上）
    const IXLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IXLine.setAttribute('x1', IREndX);
    IXLine.setAttribute('y1', IREndY);
    IXLine.setAttribute('x2', IXEndX);
    IXLine.setAttribute('y2', IXEndY);
    IXLine.setAttribute('stroke', '#3498db');
    IXLine.setAttribute('stroke-width', '3');
    IXLine.setAttribute('marker-end', 'url(#fixed-arrow-blue)');
    svg.appendChild(IXLine);
    
    const IXLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IXLabel.setAttribute('x', IXEndX + 10);
    IXLabel.setAttribute('y', IXEndY - 5);
    IXLabel.setAttribute('fill', '#3498db');
    IXLabel.setAttribute('font-size', '16');
    IXLabel.setAttribute('font-weight', 'bold');
    IXLabel.textContent = 'IX';
    svg.appendChild(IXLabel);
    
    // 绘制U1（从原点到IX末端）
    const U1Angle = Math.atan2(IXEndY - originY, IXEndX - originX);
    const U1Line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    U1Line.setAttribute('x1', originX);
    U1Line.setAttribute('y1', originY);
    U1Line.setAttribute('x2', IXEndX);
    U1Line.setAttribute('y2', IXEndY);
    U1Line.setAttribute('stroke', '#9b59b6');
    U1Line.setAttribute('stroke-width', '3');
    U1Line.setAttribute('marker-end', 'url(#fixed-arrow-purple)');
    svg.appendChild(U1Line);
    
    const U1Label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    U1Label.setAttribute('x', IXEndX + 10);
    U1Label.setAttribute('y', IXEndY - 15);
    U1Label.setAttribute('fill', '#9b59b6');
    U1Label.setAttribute('font-size', '16');
    U1Label.setAttribute('font-weight', 'bold');
    U1Label.textContent = 'U₁';
    svg.appendChild(U1Label);
    
    // 绘制虚线投影线
    const projectionLines = [
        { x1: U2EndX, y1: U2EndY, x2: U2EndX, y2: 450 },  // U2垂直向下
        { x1: IREndX, y1: IREndY, x2: IREndX, y2: 450 },  // IR垂直向下
        { x1: IXEndX, y1: IXEndY, x2: IXEndX, y2: 450 },  // IX垂直向下
        { x1: U2EndX, y1: U2EndY, x2: 750, y2: U2EndY },  // U2水平向右
        { x1: IREndX, y1: IREndY, x2: 750, y2: IREndY },  // IR水平向右
        { x1: IXEndX, y1: IXEndY, x2: 750, y2: IXEndY }   // IX水平向右
    ];
    
    projectionLines.forEach(line => {
        const projLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        projLine.setAttribute('x1', line.x1);
        projLine.setAttribute('y1', line.y1);
        projLine.setAttribute('x2', line.x2);
        projLine.setAttribute('y2', line.y2);
        projLine.setAttribute('stroke', '#666');
        projLine.setAttribute('stroke-width', '1');
        projLine.setAttribute('stroke-dasharray', '5,5');
        projLine.setAttribute('opacity', '0.6');
        svg.appendChild(projLine);
    });
    
    // 绘制红色分量标注
    const componentY1 = U2EndY + 60;  // IRcosφ和IXsinφ的位置
    const componentY2 = U2EndY + 80;  // 第二个水平分量位置
    
    // IRcosφ
    const IRcosPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IRcosPhiLine.setAttribute('x1', U2EndX);
    IRcosPhiLine.setAttribute('y1', componentY1);
    IRcosPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale);
    IRcosPhiLine.setAttribute('y2', componentY1);
    IRcosPhiLine.setAttribute('stroke', '#e74c3c');
    IRcosPhiLine.setAttribute('stroke-width', '2');
    IRcosPhiLine.setAttribute('marker-end', 'url(#fixed-arrow-red)');
    svg.appendChild(IRcosPhiLine);
    
    const IRcosPhiLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IRcosPhiLabel.setAttribute('x', U2EndX + IRcosPhi * scale / 2);
    IRcosPhiLabel.setAttribute('y', componentY1 - 5);
    IRcosPhiLabel.setAttribute('fill', '#e74c3c');
    IRcosPhiLabel.setAttribute('font-size', '12');
    IRcosPhiLabel.setAttribute('font-weight', 'bold');
    IRcosPhiLabel.setAttribute('text-anchor', 'middle');
    IRcosPhiLabel.textContent = 'IRcosφ';
    svg.appendChild(IRcosPhiLabel);
    
    // IXsinφ
    const IXsinPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IXsinPhiLine.setAttribute('x1', U2EndX + IRcosPhi * scale);
    IXsinPhiLine.setAttribute('y1', componentY2);
    IXsinPhiLine.setAttribute('x2', U2EndX + IRcosPhi * scale + IXsinPhi * scale);
    IXsinPhiLine.setAttribute('y2', componentY2);
    IXsinPhiLine.setAttribute('stroke', '#e74c3c');
    IXsinPhiLine.setAttribute('stroke-width', '2');
    IXsinPhiLine.setAttribute('marker-end', 'url(#fixed-arrow-red)');
    svg.appendChild(IXsinPhiLine);
    
    const IXsinPhiLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IXsinPhiLabel.setAttribute('x', U2EndX + IRcosPhi * scale + IXsinPhi * scale / 2);
    IXsinPhiLabel.setAttribute('y', componentY2 - 5);
    IXsinPhiLabel.setAttribute('fill', '#e74c3c');
    IXsinPhiLabel.setAttribute('font-size', '12');
    IXsinPhiLabel.setAttribute('font-weight', 'bold');
    IXsinPhiLabel.setAttribute('text-anchor', 'middle');
    IXsinPhiLabel.textContent = 'IXsinφ';
    svg.appendChild(IXsinPhiLabel);
    
    // IRsinφ（垂直向下）
    const IRsinPhiX = U2EndX + IRcosPhi * scale + 20;
    const IRsinPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IRsinPhiLine.setAttribute('x1', IRsinPhiX);
    IRsinPhiLine.setAttribute('y1', U2EndY);
    IRsinPhiLine.setAttribute('x2', IRsinPhiX);
    IRsinPhiLine.setAttribute('y2', U2EndY + IRsinPhi * scale);
    IRsinPhiLine.setAttribute('stroke', '#e74c3c');
    IRsinPhiLine.setAttribute('stroke-width', '2');
    IRsinPhiLine.setAttribute('marker-end', 'url(#fixed-arrow-red)');
    svg.appendChild(IRsinPhiLine);
    
    const IRsinPhiLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IRsinPhiLabel.setAttribute('x', IRsinPhiX + 10);
    IRsinPhiLabel.setAttribute('y', U2EndY + IRsinPhi * scale / 2);
    IRsinPhiLabel.setAttribute('fill', '#e74c3c');
    IRsinPhiLabel.setAttribute('font-size', '12');
    IRsinPhiLabel.setAttribute('font-weight', 'bold');
    IRsinPhiLabel.textContent = 'IRsinφ';
    svg.appendChild(IRsinPhiLabel);
    
    // IXcosφ（垂直向上）
    const IXcosPhiX = U2EndX + IRcosPhi * scale + IXsinPhi * scale + 20;
    const IXcosPhiLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    IXcosPhiLine.setAttribute('x1', IXcosPhiX);
    IXcosPhiLine.setAttribute('y1', U2EndY);
    IXcosPhiLine.setAttribute('x2', IXcosPhiX);
    IXcosPhiLine.setAttribute('y2', U2EndY - IXcosPhi * scale);
    IXcosPhiLine.setAttribute('stroke', '#e74c3c');
    IXcosPhiLine.setAttribute('stroke-width', '2');
    IXcosPhiLine.setAttribute('marker-end', 'url(#fixed-arrow-red)');
    svg.appendChild(IXcosPhiLine);
    
    const IXcosPhiLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    IXcosPhiLabel.setAttribute('x', IXcosPhiX + 10);
    IXcosPhiLabel.setAttribute('y', U2EndY - IXcosPhi * scale / 2);
    IXcosPhiLabel.setAttribute('fill', '#e74c3c');
    IXcosPhiLabel.setAttribute('font-size', '12');
    IXcosPhiLabel.setAttribute('font-weight', 'bold');
    IXcosPhiLabel.textContent = 'IXcosφ';
    svg.appendChild(IXcosPhiLabel);
    
    // 绘制虚线弧线（从U2到U1）
    const arcPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const midX = (U2EndX + IXEndX) / 2;
    const midY = (U2EndY + IXEndY) / 2;
    arcPath.setAttribute('d', `M ${U2EndX} ${U2EndY} Q ${midX} ${midY} ${IXEndX} ${IXEndY}`);
    arcPath.setAttribute('fill', 'none');
    arcPath.setAttribute('stroke', '#999');
    arcPath.setAttribute('stroke-width', '1.5');
    arcPath.setAttribute('stroke-dasharray', '8,4');
    arcPath.setAttribute('opacity', '0.7');
    svg.appendChild(arcPath);
}

// 页面加载时绘制固定矢量图
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', drawFixedPhasorDiagram);
} else {
    drawFixedPhasorDiagram();
}
