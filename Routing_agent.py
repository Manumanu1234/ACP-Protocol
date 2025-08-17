from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools import tool
from acp_sdk.client import Client
from acp_sdk.models import (
    Message,
    MessagePart,
)
@tool(name="addition_agent", description="Use this tool ONLY for addition. It adds two numbers together.")
async def AddAgent(query: str) -> str:
    """
    Addition Tool

    Args:
        query (str): A math query that involves **adding two numbers**. 
                     Example: "what is 2 plus 2", "add 10 and 5".
    Returns:
        str: The result of the addition.
    """
    async with Client(base_url="http://localhost:8003") as client:
        run = await client.run_sync(agent="beeai_agent", input=query)
        content = run.output[0].parts[0].content
        print("*" * 100)
        print(content)
        print("*" * 100)
        return str(content)


@tool(name="subtraction", description="Use this tool ONLY for subtraction. It subtracts one number from another.")
async def SubAgent(query: str) -> str:
    """
    Subtraction Tool

    Args:
        query (str): A math query that involves **subtracting one number from another**. 
                     Example: "subtract 5 from 12", "what is 20 minus 7".
    Returns:
        str: The result of the subtraction.
    """
    async with Client(base_url="http://localhost:8004") as client:
        run = await client.run_sync(agent="langchain_agent", input=query)
        content = run.output[0].parts[0].content
        print("*" * 100)
        print(content)
        print("*" * 100)
        return str(content)


@tool(name="multiplication", description="Use this tool ONLY for multiplication. It multiplies two numbers together.")
async def MulAgent(query: str) -> str:
    """
    Multiplication Tool

    Args:
        query (str): A math query that involves **multiplying two numbers**. 
                     Example: "multiply 3 by 7", "what is 8 times 4".
    Returns:
        str: The result of the multiplication.
    """
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(agent="agno_agent", input=query)
        content = run.output[0].parts[0].content
        print("*" * 100)
        print(content)
        print("*" * 100)
        return str(content)


@tool(name="division", description="Use this tool ONLY for division. It divides one number by another.")
async def DivAgent(query: str) -> str:
    """
    Division Tool

    Args:
        query (str): A math query that involves **dividing one number by another**. 
                     Example: "divide 20 by 5", "what is 100 divided by 4".
    Returns:
        str: The result of the division.
    """
    async with Client(base_url="http://localhost:8002") as client:
        run = await client.run_sync(agent="autogen_agent", input=query)
        content = run.output[0].parts[0].content
        print("*" * 100)
        print(content)
        print("*" * 100)
        return str(content)
class AgentExecuter:
    def __init__(self):
        pass

    def PromptFormating(self, available_agents: str) -> str:
        return f"""
        You are a Math Orchestrator Agent.  
        You have the following available agents (tools):  
        {available_agents}

        ### Instructions:
        - Break down the user query into clear **step-by-step operations**.  
        - For each operation, call the **correct agent**:
            - Use `addition_agent` ONLY for addition.
            - Use `subtraction` ONLY for subtraction.
            - Use `multiplication` ONLY for multiplication.
            - Use `division` ONLY for division.
        - Do not reuse the same agent if the step requires a different operation.
        - Execute the steps in order, passing intermediate results into the next tool.  
        - At the end, provide the final result.  

        ### Example
        User: "Take 2 add 2, then multiply the result by 3, then subtract 1, and finally divide by 2."
        Steps:
        1. addition_agent(2 plus 2) → 4
        2. multiplication(4 times 3) → 12
        3. subtraction(12 minus 1) → 11
        4. division(11 divided by 2) → 5.5
        Final Answer: 5.5

        Always follow this structured reasoning process.
        """
        

            
    async def AgentCreation(self,available_agent,query):
            agent = Agent(model=Groq(id="openai/gpt-oss-20b",api_key="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"), tools=[AddAgent,SubAgent,MulAgent,DivAgent],instructions=[self.PromptFormating(available_agents=available_agent)],show_tool_calls=True,markdown=True)
            await agent.aprint_response(query)
    