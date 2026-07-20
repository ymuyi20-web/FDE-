# FDE Gemini MCP 连接器

这个本地连接器让 Codex 可以按需调用 Gemini 生成第二版学习笔记。

## 隐私边界

- 不会自动扫描 FDE 项目。
- 只会把工具调用中明确提供的文字发送给 Gemini。
- API 密钥只从 Windows 环境变量读取，不写入代码和项目文件。

## 当前工具

- `gemini_connection_status`：只检查密钥是否被连接器识别，不访问 Gemini。
- `gemini_generate_text`：把明确提供的提示词交给 Gemini生成文字。

## 环境变量

必需：`GEMINI_API_KEY`

可选：`GEMINI_MODEL`，默认使用 `gemini-2.5-flash`。

## 当前验证结果

- 本地 MCP 服务可以正常启动。
- Codex 可以识别两个 Gemini 工具。
- Windows 环境变量可以安全转发给连接器。
- 如果 Google 返回“project has been denied access”，需要在 Google 侧处理项目权限或地区限制。
