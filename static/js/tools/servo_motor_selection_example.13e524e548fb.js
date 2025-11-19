/**
 * 伺服电机选型举例 - 前端计算逻辑
 */

/**
 * 计算伺服电机选型
 */
async function calculate() {
    // 获取输入参数
    const M = document.getElementById("M").value.trim();
    const P = document.getElementById("P").value.trim();
    const D = document.getElementById("D").value.trim();
    const MB = document.getElementById("MB").value.trim();
    const mu = document.getElementById("mu").value.trim();
    const G = document.getElementById("G").value.trim();
    const eta = document.getElementById("eta").value.trim();
    const V = document.getElementById("V").value.trim();
    const L = document.getElementById("L").value.trim();
    const tS = document.getElementById("tS").value.trim();
    const tA = document.getElementById("tA").value.trim();
    const AP = document.getElementById("AP").value.trim();
    
    // 可选参数
    const JM = document.getElementById("JM").value.trim();
    const TM = document.getElementById("TM").value.trim();
    const Tmax_motor = document.getElementById("Tmax_motor").value.trim();
    const Nmax_motor = document.getElementById("Nmax_motor").value.trim();
    
    // 验证必需参数
    const requiredParams = {
        "M": M,
        "P": P,
        "D": D,
        "MB": MB,
        "mu": mu,
        "G": G,
        "eta": eta,
        "V": V,
        "L": L,
        "tS": tS,
        "tA": tA,
        "AP": AP
    };
    
    for (const [name, value] of Object.entries(requiredParams)) {
        if (value === '') {
            showError(`请输入${name}`);
            return;
        }
        const numValue = parseFloat(value);
        if (isNaN(numValue)) {
            showError(`${name}必须是有效数字`);
            return;
        }
        if (numValue <= 0) {
            showError(`${name}必须大于0`);
            return;
        }
    }
    
    // 验证行程时间必须 >= 2 × 加减速时间
    const tS_num = parseFloat(tS);
    const tA_num = parseFloat(tA);
    if (tS_num < 2 * tA_num) {
        showError(`行程时间tS (${tS_num})必须大于等于2倍的加减速时间tA (${tA_num})`);
        return;
    }
    
    // 构建请求参数
    const params = {
        M: parseFloat(M),
        P: parseFloat(P),
        D: parseFloat(D),
        MB: parseFloat(MB),
        mu: parseFloat(mu),
        G: parseFloat(G),
        eta: parseFloat(eta),
        V: parseFloat(V),
        L: parseFloat(L),
        tS: parseFloat(tS),
        tA: parseFloat(tA),
        AP: parseFloat(AP)
    };
    
    // 添加可选参数
    if (JM !== '') {
        const jmValue = parseFloat(JM);
        if (!isNaN(jmValue) && jmValue > 0) {
            params.JM = jmValue;
        }
    }
    if (TM !== '') {
        const tmValue = parseFloat(TM);
        if (!isNaN(tmValue) && tmValue > 0) {
            params.TM = tmValue;
        }
    }
    if (Tmax_motor !== '') {
        const tmaxValue = parseFloat(Tmax_motor);
        if (!isNaN(tmaxValue) && tmaxValue > 0) {
            params.Tmax_motor = tmaxValue;
        }
    }
    if (Nmax_motor !== '') {
        const nmaxValue = parseFloat(Nmax_motor);
        if (!isNaN(nmaxValue) && nmaxValue > 0) {
            params.Nmax_motor = nmaxValue;
        }
    }
    
    // 调用API
    try {
        const result = await apiRequest('/api/tools/servo-motor-selection-example/calculate', 'POST', params);
        
        // 显示结果
        document.getElementById('result_value').textContent = formatNumber(result.result, 6);
        document.getElementById('result_unit').textContent = result.unit;
        renderFormula('result_formula', result.formula);
        document.getElementById('result').style.display = 'block';
        
        // 滚动到结果区域
        document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (error) {
        showError(error.message || '计算失败，请检查输入参数');
    }
}

