/**
 * 角加速度计算 - 使用通用表单渲染与提交流程
 */

document.addEventListener('DOMContentLoaded', () => {
    if (typeof angularAccelerationSchema === 'undefined') {
        console.warn('缺少角加速度配置schema');
        return;
    }

    const sections = angularAccelerationSchema.tabs.map(tab => ({
        id: tab.id,
        scenario: tab.scenario,
        section: { ...tab.section, apiPath: angularAccelerationSchema.apiPath }
    }));

    initTabbedTool({
        tabGroupId: 'sub-tabs-angular',
        sectionClass: 'tab-content',
        sections,
        apiPath: angularAccelerationSchema.apiPath,
        formatters: {}
    });
});
