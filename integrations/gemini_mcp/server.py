"""Expose a small, privacy-conscious Gemini client to Codex through MCP."""

from __future__ import annotations

import os

from google import genai
from google.genai.errors import ClientError
from mcp.server.fastmcp import FastMCP


DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

mcp = FastMCP(
    "FDE Gemini Learning Assistant",
    instructions=(
        "Only send the text explicitly supplied to a Gemini tool. "
        "Do not scan the workspace or read project files automatically."
    ),
)


def _api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError(
            "没有找到 GEMINI_API_KEY。请把密钥保存为 Windows 用户环境变量，"
            "然后彻底退出并重新打开 Codex。"
        )
    return key


@mcp.tool()
def gemini_connection_status() -> str:
    """Check local Gemini configuration without revealing or using the API key."""
    configured = bool(
        os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    )
    if configured:
        return f"Gemini 密钥已被连接器识别；默认模型：{DEFAULT_MODEL}。"
    return "Gemini 密钥尚未被连接器识别。"


@mcp.tool()
def gemini_generate_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Ask Gemini to generate text from only the prompt explicitly provided."""
    clean_prompt = prompt.strip()
    if not clean_prompt:
        raise ValueError("prompt 不能为空。")

    client = genai.Client(api_key=_api_key())
    try:
        response = client.models.generate_content(
            model=model or DEFAULT_MODEL,
            contents=clean_prompt,
        )
    except ClientError as error:
        if error.code == 403:
            raise RuntimeError(
                "Gemini 已收到请求，但 Google 拒绝了这个 Cloud 项目的访问权限。"
                "请检查项目状态、账号验证和服务支持地区；这不是密钥格式错误。"
            ) from error
        raise RuntimeError(f"Gemini API 调用失败：{error}") from error
    if not response.text:
        raise RuntimeError("Gemini 返回了空内容。")
    return response.text


if __name__ == "__main__":
    mcp.run(transport="stdio")
