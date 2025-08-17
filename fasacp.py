class AgentCollection:
    """
    A collection of agents available on ACP servers.
    Allows users to discover available agents on ACP servers.
    """
    
    def __init__(self):
        self.agents = []
    
    @classmethod
    async def from_acp(cls, *servers) -> 'AgentCollection':
        """
        Creates an AgentCollection by fetching agents from the provided ACP servers.
        
        Args:
            *servers: ACP server client instances to fetch agents from
            
        Returns:
            AgentCollection: Collection containing all discovered agents
        """
        collection = cls()
        
        for server in servers:
            async for agent in server.agents():
                collection.agents.append((server,agent))
        
        return collection