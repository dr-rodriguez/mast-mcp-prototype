# Prototype for MAST MCP server
# Main file to organize all the tools

from src import observations, exomast
from fastmcp import FastMCP

mcp = FastMCP(name="MAST MCP")

mcp.mount(observations.mcp)
mcp.mount(exomast.mcp)

# --- Entry point ---
if __name__ == "__main__":
    mcp.run(transport="stdio")
