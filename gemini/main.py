from mcp.server.fastmcp import FastMCP

# create server
mcp = FastMCP("adder")

# an adding single tool
@mcp.tool()
def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b

if __name__ == "__main__":
    mcp.run()        # stdio transport by default