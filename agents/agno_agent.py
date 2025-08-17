from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools
from mcp import ClientSession, StdioServerParameters
from agno.models.groq import Groq
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

server=Server()

@server.agent(name="agno_agent",description="This agent is usefull for multiplying of 2 numbers")
async def run_mcp_agent(inputs:list[Message])->AsyncGenerator[RunYield,RunYieldResume]:
    """This agent Usefull for Mutiplication of 2 Numbers"""
    # Initialize the MCP tools
    mcp_tools=StdioServerParameters(
        command="uv",
        args=["run","../mcp_servers/mcp_server1.py"]

    )
    print("*"*100)
    print(inputs)
    print("*"*100)
    async with MultiMCPTools(server_params_list=[mcp_tools],timeout_seconds=30.0) as main_mcp_tools:
        print(main_mcp_tools)
        
        agent = Agent(model=Groq(id="openai/gpt-oss-20b",api_key="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"), tools=[main_mcp_tools])

        # Run the agent
        res=await agent.arun(inputs[0].parts[0].content)
        print(res.content)
        
        yield MessagePart(content=str(res.content))

server.run(port=8001)