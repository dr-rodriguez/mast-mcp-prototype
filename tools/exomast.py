from fastmcp import FastMCP

mcp = FastMCP("ExoMAST MCP")

@mcp.resource("config://exomast-version")
def get_exomast_version():
    return "Placeholder for ExoMAST version"
