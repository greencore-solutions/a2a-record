"""A2A Passport — reference MCP client (streamable-HTTP). Lists the tools, reads passport #1, verifies it on the door.
pip install mcp
"""
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "https://mcp.a2a-passport.ai/mcp"
READ = ("get_passport", {"subject": "03284230006408"})
VERIFY = ("verify_passport", {"passport_id": "gtin-03284230006408"})


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(len(tools.tools), "tools:", ", ".join(t.name for t in tools.tools))
            passport = await session.call_tool(*READ)
            check = await session.call_tool(*VERIFY)
            print(passport.content[0].text[:400]); print(check.content[0].text[:300])


if __name__ == "__main__":
    asyncio.run(main())
