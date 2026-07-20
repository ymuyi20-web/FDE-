"""Local smoke test for the FDE Gemini MCP server (does not call Gemini)."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).with_name("server.py")
    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
        env=dict(os.environ),
    )

    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("MCP 启动成功")
            print("工具：" + ", ".join(tool.name for tool in tools.tools))
            status = await session.call_tool("gemini_connection_status", {})
            print("状态：" + status.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
