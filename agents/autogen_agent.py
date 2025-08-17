from autogen_core.models import UserMessage
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from dotenv import load_dotenv
import json
load_dotenv()
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from collections.abc import AsyncGenerator

server=Server()

@server.agent(name="autogen_agent",description="This agent is usefull for divide of 2 numbers")
async def AutoGenAgent(inputs:list[Message])->AsyncGenerator[RunYield,RunYieldResume]:
    server_params=StdioServerParams(
      command="uv",
      args=["run","../mcp_servers/mcp_server4.py"]
    )
    div_tools=await mcp_server_tools(server_params)
    print(div_tools)
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash-lite",
        model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True),
        api_key="",
    )
    question=inputs[0].parts[0].content
    print
    agent=AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=div_tools,
        system_message="Use tools to solve tasks. You will give 2 numbers take it as first and second number",
        )
    result = await agent.run(task=question)
    raw_content = result.messages[-1].results[0].content
    parsed = json.loads(raw_content)  # turns it into a Python list/dict
    final_answer = parsed[0]["text"]

    print(final_answer)  # -> 1
    yield MessagePart(content=str(final_answer))

server.run(port=8002)
