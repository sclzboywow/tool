/**
 * 小车驱动电机功率计算 - 前端计算逻辑
 */

// showError 函数已在 common.js 中定义，使用屏幕中间的模态框显示

/**
 * 小车驱动电机功率计算
 */
async function calculateCartDrivePower() {
    const mInput = document.getElementById('m').value.trim();
    const vInput = document.getElementById('v').value.trim();
    const uInput = document.getElementById('u').value.trim();
    const KInput = document.getElementById('K').value.trim();
    const etaInput = document.getElementById('eta').value.trim();
    
    if (mInput === '') {
        showError('请输入质量');
        return;
    }
    const m = parseFloat(mInput);
    if (isNaN(m) || m <= 0) {
        showError('质量必须大于0');
        return;
    }
    
    if (vInput === '') {
        showError('请输入小车速度');
        return;
    }
    const v = parseFloat(vInput);
    if (isNaN(v) || v <= 0) {
        showError('小车速度必须大于0');
        return;
    }
    
    const u = uInput === '' ? 0.1 : parseFloat(uInput);
    if (isNaN(u) || u < 0) {
        showError('摩擦系数必须大于等于0');
        return;
    }
    
    const K = KInput === '' ? 1.25 : parseFloat(KInput);
    if (isNaN(K) || K <= 0) {
        showError('功率系数必须大于0');
        return;
    }
    
    const eta = etaInput === '' ? 0.8 : parseFloat(etaInput);
    if (isNaN(eta) || eta <= 0 || eta > 1) {
        showError('传动效率应在0-1之间');
        return;
    }
    
    const params = {
        scenario: 'cart_drive_power',
        m: m,
        v: v,
        u: u,
        K: K,
        eta: eta
    };
    
    try {
        const result = await apiRequest('/api/tools/cart-drive-power/calculate', 'POST', params);
        if (result.extra) {
            if (result.extra.F !== undefined) {
                document.getElementById('F_value').textContent = formatNumber(result.extra.F, 2);
            }
            if (result.extra.P1 !== undefined) {
                document.getElementById('P1_value').textContent = formatNumber(result.extra.P1, 4);
            }
        }
        document.getElementById('P_value').textContent = formatNumber(result.result, 4);
        renderFormula('result_formula', result.formula);
        document.getElementById('result').style.display = 'block';
        document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入');
    }
}

