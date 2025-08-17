import asyncio
import os
import sys
import tempfile
import traceback

from dotenv import load_dotenv
from beeai_framework.backend.chat import ChatModel
from beeai_framework.adapters.groq.backend.chat import GroqChatModel
from beeai_framework.agents.react import ReActAgent
from beeai_framework.errors import FrameworkError
from beeai_framework.memory import UnconstrainedMemory
from dotenv import load_dotenv
from mcp import StdioServerParameters,ClientSession
from mcp.client.stdio import stdio_client
from beeai_framework.tools.mcp_tools import MCPTool
load_dotenv()

from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

server=Server()

@server.agent(name="beeai_agent",description="This agent is usefull for adding of 2 numbers")
async def main(inputs:list[Message]) -> AsyncGenerator[RunYield,RunYieldResume]:
    llm = GroqChatModel(model_id="llama3-70b-8192")
    server_params = StdioServerParameters(
        command="uv",
        args=["run","../mcp_servers/mcp_server2.py"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()

    print(tools.tools)   
    print(type(tools.tools))

    converted_tools = [MCPTool(tool=tool,server_params=server_params) for tool in tools.tools]

    agent = ReActAgent(
        llm=llm,
        tools=converted_tools,
        memory=UnconstrainedMemory(),
        stream=True
    )
    result = await agent.run(inputs[0].parts[0].content)
    print(result.result.text)
    yield MessagePart(content=str(result.result.text))

server.run(port=8003)