# Prototype for MAST MCP server

from fastmcp import FastMCP
from astroquery import __version__
from astroquery.mast import Observations

mcp = FastMCP("mast")


# Static resource: astroquery version
@mcp.resource("config://version")
def get_version(): 
    return __version__


# --- Tool: Query observations ---
@mcp.tool(
        title="Query MAST Observations", 
        description="Query MAST observations for a specified target and radius."
        )
async def mast_observation_query(target: str, radius: str="0.02 deg") -> str:
    """Query MAST observations for specified target."""

    # The actual query
    obs_table = Observations.query_object(target, radius=radius)

    if len(obs_table) == 0:
        return f"No observations found for target: {target} within radius: {radius}"
    
    print(f"Found {len(obs_table)} observations for target: {target}")

    # Convert table to string representation
    # First convert to string list, then join with newlines
    text_table = '\n'.join(obs_table[:10].pformat(max_width=120))

    text_output = f"Top 10 observations for target: {target} within radius: {radius}:\n"
    text_output += text_table

    return text_output


# --- Entry point ---
if __name__ == "__main__":
    mcp.run(transport="stdio")