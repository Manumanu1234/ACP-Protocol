# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

server=Server()

@server.agent(name="langchain_agent",description="This agent is usefull for subtract of 2 numbers")
async def Langchain_Server(inputs:list[Message])->AsyncGenerator[RunYield,RunYieldResume]:
    server_params = StdioServerParameters(
            command="uv",
            args=["run","../mcp_servers/mcp_server3.py"]
        )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            llm=ChatGroq(
                model="openai/gpt-oss-20b",
                api_key="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"
            )
            agent = create_react_agent(model=llm,tools=tools,prompt="You must use appropriate tool for the user query")
            agent_response = await agent.ainvoke({"messages": inputs[0].parts[0].content})
            print(agent_response['messages'][-1].content)
            yield MessagePart(content=str(agent_response['messages'][-1].content))

server.run(port=8004)