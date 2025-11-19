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


/**
 * 收集表单数据为简单对象
 */
function collectFormData(formElement) {
    const formData = new FormData(formElement);
    const payload = {};
    for (const [key, value] of formData.entries()) {
        if (value !== "") {
            payload[key] = isNaN(value) ? value : Number(value);
        }
    }
    return payload;
}

/**
 * 基于字段定义进行基础校验
 */
function validateFields(fields, payload) {
    for (const field of fields) {
        const value = payload[field.name];
        if (field.required && (value === undefined || value === null || value === "")) {
            return { valid: false, message: `${field.label} 为必填项` };
        }
        if (field.type === "number" && value !== undefined) {
            if (typeof value !== "number" || Number.isNaN(value)) {
                return { valid: false, message: `${field.label} 必须是数字` };
            }
            if (field.min !== null && field.min !== undefined && value < field.min) {
                return { valid: false, message: `${field.label} 不能小于 ${field.min}` };
            }
            if (field.max !== null && field.max !== undefined && value > field.max) {
                return { valid: false, message: `${field.label} 不能大于 ${field.max}` };
            }
        }
    }
    return { valid: true };
}

/**
 * 渲染通用结果面板
 */
function renderResult(container, contentElement, response) {
    if (!container || !contentElement) return;
    const details = [
        `<div><strong>结果：</strong>${response.result}</div>`,
        `<div><strong>单位：</strong>${response.unit || ""}</div>`,
        `<div><strong>公式：</strong>${response.formula || ""}</div>`,
    ];
    if (response.scenario_name) {
        details.push(`<div><strong>场景：</strong>${response.scenario_name}</div>`);
    }
    if (response.extra) {
        details.push(`<pre>${JSON.stringify(response.extra, null, 2)}</pre>`);
    }
    contentElement.innerHTML = details.join("\n");
    container.style.display = "block";
}

function getValueByPath(obj, path) {
    if (!obj || !path) return undefined;
    return path.split('.').reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), obj);
}

function parseFieldValue(input, field) {
    const raw = input.value.trim();
    if (raw === '') {
        return { valid: !field.required, value: null, message: `${field.label}不能为空` };
    }

    if (field.type === 'select') {
        return { valid: true, value: raw };
    }

    const numeric = parseFloat(raw);
    if (isNaN(numeric)) {
        return { valid: false, value: null, message: `${field.label}必须是数字` };
    }
    if (field.min !== undefined && numeric < field.min) {
        return { valid: false, value: null, message: `${field.label}不能小于${field.min}` };
    }
    if (field.max !== undefined && numeric > field.max) {
        return { valid: false, value: null, message: `${field.label}不能大于${field.max}` };
    }
    return { valid: true, value: numeric };
}

function renderResultCard(resultConfig, response, formatters = {}) {
    if (!resultConfig) return;
    const container = document.getElementById(resultConfig.id);
    if (!container) return;

    (resultConfig.items || []).forEach(item => {
        const target = document.getElementById(item.id);
        if (!target) return;
        let value = getValueByPath(response, item.source || 'result');
        if (item.formatter && typeof formatters[item.formatter] === 'function') {
            value = formatters[item.formatter](value, response, item);
        } else if (typeof value === 'number') {
            value = formatNumber(value, item.decimals || 4);
        } else if (value === undefined || value === null || value === '') {
            value = 'N/A';
        }
        target.innerHTML = value;
    });

    if (resultConfig.formula_id && response.formula) {
        renderFormula(resultConfig.formula_id, response.formula);
    }
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function initTabbedTool(config) {
    const tabGroup = document.getElementById(config.tabGroupId);
    const sections = config.sections || [];
    const sectionClass = config.sectionClass || 'tab-content';

    if (tabGroup) {
        tabGroup.querySelectorAll('.sub-tab').forEach(button => {
            button.addEventListener('click', () => {
                const target = button.getAttribute('data-target');
                document.querySelectorAll(`.${sectionClass}`).forEach(div => {
                    div.classList.remove('active');
                });
                document.querySelectorAll(`#${config.tabGroupId} .sub-tab`).forEach(btn => btn.classList.remove('active'));
                const tabContent = document.getElementById(target);
                if (tabContent) tabContent.classList.add('active');
                button.classList.add('active');
            });
        });
    }

    sections.forEach(section => {
        const submitButton = document.querySelector(`[data-submit="${section.id}"]`);
        if (!submitButton) return;
        submitButton.addEventListener('click', async () => {
            const payload = { scenario: section.scenario };
            for (const field of section.section.fields || []) {
                const input = document.getElementById(field.id);
                if (!input) continue;
                const { valid, value, message } = parseFieldValue(input, field);
                if (!valid) {
                    showError(message);
                    return;
                }
                if (value !== null && value !== undefined) {
                    payload[field.name || field.id] = value;
                }
            }

            try {
                const response = await apiRequest(section.section.apiPath || config.apiPath, 'POST', payload);
                renderResultCard(section.section.result, response, config.formatters);
            } catch (error) {
                showError(error.message || '计算失败，请检查输入');
            }
        });
    });
}

