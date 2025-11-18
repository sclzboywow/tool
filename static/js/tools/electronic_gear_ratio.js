/**
 * 伺服电机电子齿轮比计算
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
 * 方式一：正向计算（已知负载移动距离和电机转数）
 */
async function calculateMethod1() {
    // 获取输入参数
    const encoderResolution = document.getElementById("m1_encoder_resolution").value;
    const mechanicalRatio = document.getElementById("m1_mechanical_ratio").value;
    const loadDistance = document.getElementById("m1_load_distance").value;
    const motorRevolutions = document.getElementById("m1_motor_revolutions").value;
    
    // 验证必需参数
    if (!encoderResolution || isNaN(encoderResolution) || parseFloat(encoderResolution) <= 0) {
        showError("编码器分辨率必须大于0");
        return;
    }
    
    if (!mechanicalRatio || isNaN(mechanicalRatio) || parseFloat(mechanicalRatio) <= 0) {
        showError("机械减速比必须大于0");
        return;
    }
    
    if (!loadDistance || isNaN(loadDistance) || parseFloat(loadDistance) <= 0) {
        showError("负载移动距离必须大于0");
        return;
    }
    
    if (!motorRevolutions || isNaN(motorRevolutions) || parseFloat(motorRevolutions) <= 0) {
        showError("电机转数必须大于0");
        return;
    }
    
    // 构建请求参数
    const params = {
        encoder_resolution: parseFloat(encoderResolution),
        mechanical_ratio: parseFloat(mechanicalRatio),
        load_distance: parseFloat(loadDistance),
        motor_revolutions: parseFloat(motorRevolutions)
    };
    
    try {
        // 发送API请求
        const response = await fetch("/api/tools/electronic-gear-ratio/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "计算失败");
        }
        
        const result = await response.json();
        
        // 显示计算结果
        document.getElementById("m1_result_value").textContent = result.result.toFixed(6);
        document.getElementById("m1_result_formula").innerHTML = result.formula;
        
        // 显示脉冲当量
        if (result.extra && result.extra.pulse_equivalent_calc !== undefined) {
            document.getElementById("m1_pulse_equivalent_value").textContent = result.extra.pulse_equivalent_calc.toFixed(6);
        }
        
        document.getElementById("m1_result").style.display = "block";
        
    } catch (error) {
        showError(error.message || "计算失败，请检查输入参数");
    }
}

/**
 * 方式二：反向计算（已知脉冲当量）
 */
async function calculateMethod2() {
    // 获取输入参数
    const encoderResolution = document.getElementById("m2_encoder_resolution").value;
    const mechanicalRatio = document.getElementById("m2_mechanical_ratio").value;
    const pulseEquivalent = document.getElementById("m2_pulse_equivalent").value;
    const loadDistance = document.getElementById("m2_load_distance").value;
    
    // 验证必需参数
    if (!encoderResolution || isNaN(encoderResolution) || parseFloat(encoderResolution) <= 0) {
        showError("编码器分辨率必须大于0");
        return;
    }
    
    if (!mechanicalRatio || isNaN(mechanicalRatio) || parseFloat(mechanicalRatio) <= 0) {
        showError("机械减速比必须大于0");
        return;
    }
    
    if (!pulseEquivalent || isNaN(pulseEquivalent) || parseFloat(pulseEquivalent) <= 0) {
        showError("脉冲当量必须大于0");
        return;
    }
    
    // 构建请求参数
    const params = {
        encoder_resolution: parseFloat(encoderResolution),
        mechanical_ratio: parseFloat(mechanicalRatio),
        pulse_equivalent: parseFloat(pulseEquivalent)
    };
    
    // 如果提供了负载移动距离，也加入参数
    if (loadDistance && loadDistance !== "" && !isNaN(loadDistance) && parseFloat(loadDistance) > 0) {
        params.load_distance = parseFloat(loadDistance);
    }
    
    try {
        // 发送API请求
        const response = await fetch("/api/tools/electronic-gear-ratio/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "计算失败");
        }
        
        const result = await response.json();
        
        // 显示计算结果
        document.getElementById("m2_result_value").textContent = result.result.toFixed(6);
        document.getElementById("m2_result_formula").innerHTML = result.formula;
        
        // 显示电机转数（如果存在）
        if (result.extra && result.extra.motor_revolutions_calc !== undefined) {
            document.getElementById("m2_motor_revolutions_value").textContent = result.extra.motor_revolutions_calc.toFixed(6);
            document.getElementById("m2_motor_revolutions_result").style.display = "block";
        } else {
            document.getElementById("m2_motor_revolutions_result").style.display = "none";
        }
        
        document.getElementById("m2_result").style.display = "block";
        
    } catch (error) {
        showError(error.message || "计算失败，请检查输入参数");
    }
}
