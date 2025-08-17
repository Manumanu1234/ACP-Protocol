import asyncio

from acp_sdk.client import Client
from acp_sdk.models import (
    Message,
    MessagePart,
)
from fasacp import AgentCollection
from Routing_agent import AgentExecuter
async def example() -> None:
    async with Client(base_url="http://localhost:8001") as client1,Client(base_url="http://localhost:8002") as client2,Client(base_url="http://localhost:8003") as client3,Client(base_url="http://localhost:8004") as client4:
        agent_collection=await AgentCollection.from_acp(client1,client2,client3,client4)
        acp_agents={agent.name:{'agent':agent,'client':client} for client,agent in agent_collection.agents}
        my_list=[]
        for client,agent in agent_collection.agents:
            agent_name=agent.name
            agent_desc=agent.description
            combine=f"{agent_name} : {agent_desc}"
            my_list.append(combine)
        agent_available="\n".join(my_list)
        print(agent_available)
        instance=AgentExecuter()
        query="""
        what is 2 add 2 
        multiply the result with 10
        and again add with 2
        """
        await instance.AgentCreation(available_agent=agent_available,query=query)
        # run = await client.run_sync(agent="agno_agent", input=[Message(parts=[MessagePart(content="Howdy!")])])
        # print(run)
        
        

if __name__ == "__main__":
    asyncio.run(example())