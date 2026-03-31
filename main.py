from fastmcp import FastMCP  # ❌ Was: from fastmcp import FastMCP
import random

mcp = FastMCP("simple calculator server")

@mcp.tool()  # ✅ Need parentheses ()
def add(a: int, b: int) -> int:
    """Add two numbers
    Args: 
        a: First number
        b: Second number
    Returns:
        The sum of a and b
    """
    return a + b

@mcp.tool()  # ✅ Need parentheses ()
def get_random_number(min: int, max: int) -> int:
    """Get a random number between min and max
    Args: 
        min: Minimum value
        max: Maximum value
    Returns:
        A random number between min and max
    """
    return random.randint(min, max)

@mcp.resource("info") # ✅ Need parentheses ()
def server_info() -> dict:
    """Get server information
    Returns:
        A dictionary containing server information
    """
    return {
        "name": "simple calculator server",
        "version": "1.0.0",
        "description": "A simple calculator server",
        "tools": ["add", "get_random_number"]
    }

if __name__ == "__main__":
    # mcp.run()  # ✅ FastMCP defaults to stdio (remove transport/host/port for local test)

    mcp.run(
        transport="http",
        host="[IP_ADDRESS]",
        port=8000,
    )