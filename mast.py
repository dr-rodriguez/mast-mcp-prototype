# Prototype for MAST MCP server

from collections import Counter

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

    # Group by obs_collection and count
    obs_collections = obs_table['obs_collection']
    counts = Counter(obs_collections)

    # Prepare output: mission (obs_collection) and count
    lines = [f"{'mission':<10}count"]
    for mission, count in counts.items():
        lines.append(f"{mission:<10}{count}")
    text_table = '\n'.join(lines)

    text_output = f"Observation counts by mission for target: {target} within radius: {radius}:\n"
    text_output += text_table

    return text_output


# Tool: Observation details --
@mcp.tool(
        title="Get MAST Observation Details", 
        description="Get details for a specific MAST observation by obs_id."
        )
async def mast_observation_details(obs_id: str) -> str:
    """Get details for a specific MAST observation by obs_id."""

    # The actual query
    obs_table = Observations.query_criteria(obs_id=obs_id)

    if len(obs_table) == 0:
        return f"No observation found with obs_id: {obs_id}"

    print(f"Found observation with obs_id: {obs_id}")

    # Prepare output: key details of the observation
    details = obs_table[0]  # There should be only one entry for a unique obs_id
    lines = [f"{key}: {details[key]}" for key in details.colnames]
    text_output = f"Details for observation ID: {obs_id}:\n"
    text_output += '\n'.join(lines)

    return text_output


# --- Entry point ---
if __name__ == "__main__":
    mcp.run(transport="stdio")