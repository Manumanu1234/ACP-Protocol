from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp=FastMCP("addition")

@mcp.tool()
def Addition_Two_Numbers(num1:int,num2:int):
    """ 
    This tool is used for add 2 numbers
    
    *Args*:
    num1 integer
    num2 integer
    
    *Return the result as integer*
    """
    
    return num1+num2

if __name__ == "__main__":
    mcp.run(transport='stdio')