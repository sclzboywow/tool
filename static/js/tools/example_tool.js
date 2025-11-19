// 自动生成的 示例参数计算 前端交互骨架
// 更新请修改 config/tools.json 并重新运行生成脚本

const example_toolFields = [
    {
        "name": "value_a",
        "label": "参数A",
        "type": "number",
        "required": true,
        "min": 0,
        "max": null
    },
    {
        "name": "value_b",
        "label": "参数B",
        "type": "number",
        "required": false,
        "min": null,
        "max": null
    },
    {
        "name": "mode",
        "label": "计算模式",
        "type": "select",
        "required": true,
        "min": null,
        "max": null
    }
];
const example_toolEndpoint = "/api/tools/example-tool/calculate";
const example_toolForm = document.getElementById("example_tool-form");
const example_toolResult = document.getElementById("example_tool-result");
const example_toolResultContent = document.querySelector("#example_tool-result .result-content");

if (example_toolForm) {
    example_toolForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = collectFormData(example_toolForm);
        const validation = validateFields(example_toolFields, payload);
        if (!validation.valid) {
            showError(validation.message);
            return;
        }

        try {
            const response = await apiRequest(example_toolEndpoint, "POST", payload);
            renderResult(example_toolResult, example_toolResultContent, response);
        } catch (error) {
            showError(error.message || "请求失败");
        }
    });
}
