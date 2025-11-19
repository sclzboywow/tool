/**
 * 电动机启动时端电压计算 - 前端计算逻辑
 */

// showError 函数已在 common.js 中定义，使用屏幕中间的模态框显示

/**
 * 电动机启动时端电压计算
 */
async function calculateMotorStartupVoltage() {
    const KiqInput = document.getElementById('Kiq').value.trim();
    const SedInput = document.getElementById('Sed').value.trim();
    const SjhInput = document.getElementById('Sjh').value.trim();
    const SebInput = document.getElementById('Seb').value.trim();
    const ukInput = document.getElementById('uk').value.trim();
    const PedInput = document.getElementById('Ped').value.trim();
    const LInput = document.getElementById('L').value.trim();
    const deltaUxInput = document.getElementById('deltaUx').value.trim();
    
    if (KiqInput === '') {
        showError('请输入启动电流倍数');
        return;
    }
    const Kiq = parseFloat(KiqInput);
    if (isNaN(Kiq) || Kiq <= 0) {
        showError('启动电流倍数必须大于0');
        return;
    }
    
    if (SedInput === '') {
        showError('请输入启动电动机额定容量');
        return;
    }
    const Sed = parseFloat(SedInput);
    if (isNaN(Sed) || Sed <= 0) {
        showError('启动电动机额定容量必须大于0');
        return;
    }
    
    if (SjhInput === '') {
        showError('请输入变压器低压侧其他负荷容量');
        return;
    }
    const Sjh = parseFloat(SjhInput);
    if (isNaN(Sjh) || Sjh < 0) {
        showError('变压器低压侧其他负荷容量必须大于等于0');
        return;
    }
    
    if (SebInput === '') {
        showError('请输入变压器额定容量');
        return;
    }
    const Seb = parseFloat(SebInput);
    if (isNaN(Seb) || Seb <= 0) {
        showError('变压器额定容量必须大于0');
        return;
    }
    
    if (ukInput === '') {
        showError('请输入变压器阻抗电压');
        return;
    }
    const uk = parseFloat(ukInput);
    if (isNaN(uk) || uk <= 0) {
        showError('变压器阻抗电压必须大于0');
        return;
    }
    
    if (PedInput === '') {
        showError('请输入电动机额定功率');
        return;
    }
    const Ped = parseFloat(PedInput);
    if (isNaN(Ped) || Ped <= 0) {
        showError('电动机额定功率必须大于0');
        return;
    }
    
    if (LInput === '') {
        showError('请输入线路长度');
        return;
    }
    const L = parseFloat(LInput);
    if (isNaN(L) || L <= 0) {
        showError('线路长度必须大于0');
        return;
    }
    
    if (deltaUxInput === '') {
        showError('请输入每千瓦公里单位电压损失');
        return;
    }
    const deltaUx = parseFloat(deltaUxInput);
    if (isNaN(deltaUx) || deltaUx < 0) {
        showError('每千瓦公里单位电压损失必须大于等于0');
        return;
    }
    
    const params = {
        scenario: 'motor_startup_voltage',
        Kiq: Kiq,
        Sed: Sed,
        Sjh: Sjh,
        Seb: Seb,
        uk: uk,
        Ped: Ped,
        L: L,
        deltaUx: deltaUx
    };
    
    try {
        const result = await apiRequest('/api/tools/motor-startup-voltage/calculate', 'POST', params);
        if (result.extra && result.extra.Sdm !== undefined) {
            document.getElementById('Sdm_value').textContent = formatNumber(result.extra.Sdm, 2);
        }
        document.getElementById('result_value').textContent = formatNumber(result.result, 4);
        document.getElementById('result_unit').textContent = result.unit;
        renderFormula('result_formula', result.formula);
        document.getElementById('result').style.display = 'block';
        document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

