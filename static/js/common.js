/**
 * 公共JavaScript函数
 */

/**
 * 显示错误消息（屏幕中间模态框）
 */
function showError(message) {
    // 移除已存在的错误提示
    const existingModal = document.getElementById('error-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // 创建遮罩层
    const overlay = document.createElement('div');
    overlay.className = 'error-modal-overlay';
    overlay.id = 'error-modal';
    
    // 创建错误提示框
    const errorBox = document.createElement('div');
    errorBox.className = 'error-modal-box';
    
    // 错误图标
    const icon = document.createElement('div');
    icon.className = 'error-modal-icon';
    icon.innerHTML = '⚠️';
    
    // 错误消息
    const messageDiv = document.createElement('div');
    messageDiv.className = 'error-modal-message';
    messageDiv.textContent = message;
    
    // 关闭按钮
    const closeBtn = document.createElement('button');
    closeBtn.className = 'error-modal-close';
    closeBtn.textContent = '确定';
    closeBtn.onclick = () => {
        overlay.remove();
    };
    
    errorBox.appendChild(icon);
    errorBox.appendChild(messageDiv);
    errorBox.appendChild(closeBtn);
    overlay.appendChild(errorBox);
    
    // 添加到页面
    document.body.appendChild(overlay);
    
    // 点击遮罩层也可以关闭
    overlay.onclick = (e) => {
        if (e.target === overlay) {
            overlay.remove();
        }
    };
    
    // 3秒后自动关闭
    setTimeout(() => {
        if (overlay.parentNode) {
            overlay.remove();
        }
    }, 3000);
    
    // 添加动画效果
    setTimeout(() => {
        errorBox.classList.add('show');
    }, 10);
}

/**
 * 显示成功消息
 */
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.textContent = message;
    
    const container = document.querySelector('.main-content .container');
    if (container) {
        container.insertBefore(successDiv, container.firstChild);
        
        // 3秒后自动移除
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
}

/**
 * 格式化数字
 */
function formatNumber(num, decimals = 4) {
    if (num === null || num === undefined || isNaN(num)) {
        return 'N/A';
    }
    return Number(num).toFixed(decimals);
}

/**
 * 发送API请求
 */
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || '请求失败');
        }
        
        return result;
    } catch (error) {
        throw error;
    }
}

/**
 * 渲染数学公式到指定元素（简单文本格式）
 */
function renderFormula(elementId, formulaText) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    // 如果公式文本包含HTML标签（如<br>），使用innerHTML；否则使用textContent
    let displayText = formulaText;
    if (!displayText.startsWith('公式:')) {
        displayText = '公式: ' + displayText;
    }
    
    // 检查是否包含HTML标签
    if (displayText.includes('<br>') || displayText.includes('<sub>') || displayText.includes('<sup>')) {
        element.innerHTML = displayText;
    } else {
        element.textContent = displayText;
    }
}

