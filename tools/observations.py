# Prototype for Observations MCP

from collections import Counter

from fastmcp import FastMCP
from astroquery import __version__
from astroquery.mast import Observations

mcp = FastMCP("Observations MCP")


# Static resource: astroquery version
@mcp.resource("config://astroquery-version")
def get_astroquery_version():
    return f"astroquery version: {__version__}"


# --- Tool: Query observations ---
@mcp.tool(
    title="Query MAST Observations",
    description="Query MAST observations for a specified target and radius.",
)
async def mast_observation_query(
    target: str,
    radius: str = "0.02 deg",
    mission_name: str = None,
    dataproduct_type: str = None,
    instrument_name: str = None,
    filters: str = None,
    hlsp_name: str = None,
) -> str:
    """Query MAST observations for specified target.

    Parameters
    ----------
    target : str
        Name of the target object to query.
    radius : str
        Search radius around the target (default is "0.02 deg").
    mission_name : str, optional
        Filter by mission/collection name, such as JWST, TESS, HST (optional).
    dataproduct_type : str, optional
        Filter by data product type, such as image, timeseries, spectra (optional).
    instrument_name : str, optional
        Filter by instrument name (optional).
    filters : str, optional
        Astronomical filters to search on (optional).
    hlsp_name : str, optional
        Filter by High-Level Science Product name. Also known as provenance_name (optional).
    """

    kwargs = {}

    # Making some fields wildcard searches if provided
    if instrument_name is not None and instrument_name != "":
        ins_name = f"*{instrument_name}*"
        kwargs["instrument_name"] = ins_name

    if filters is not None and filters != "":
        filt_names = f"*{filters}*"
        kwargs["filters"] = filt_names

    # Only add to kwargs if not None or empty
    if mission_name is not None and mission_name != "":
        kwargs["obs_collection"] = mission_name
    if dataproduct_type is not None and dataproduct_type != "":
        kwargs["dataproduct_type"] = dataproduct_type
    if hlsp_name is not None and hlsp_name != "":
        kwargs["provenance_name"] = hlsp_name

    # The actual query
    obs_table = Observations.query_criteria(
        objectname=target,
        radius=radius,
        **kwargs,
    )

    if len(obs_table) == 0:
        return f"No observations found for target: {target} within radius: {radius}"

    print(f"Found {len(obs_table)} observations for target: {target}")

    # Group by obs_collection and count
    obs_collections = obs_table["obs_collection"]
    counts = Counter(obs_collections)

    # Prepare output: mission (obs_collection) and count
    lines = [f"{'mission':<10}count"]
    for mission, count in counts.items():
        lines.append(f"{mission:<10}{count}")
    text_table = "\n".join(lines)

    text_output = (
        f"Observation counts by mission for target: {target} within radius: {radius}:\n"
    )
    text_output += text_table

    return text_output


# --- Tool: Observation details ---
@mcp.tool(
    title="Get MAST Observation Details",
    description="Get details for a specific MAST observation by obs_id.",
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
    text_output += "\n".join(lines)

    return text_output
