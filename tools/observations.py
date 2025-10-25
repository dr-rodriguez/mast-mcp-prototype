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


# --- Tool: List available missions ---
@mcp.tool(
    title="List Available MAST Missions",
    description="List all data missions archived by MAST and available through astroquery.",
)
async def list_mast_missions() -> str:
    """List all available MAST missions."""
    missions = Observations.list_missions()
    return f"Available MAST missions:\n{', '.join(missions)}"


# --- Tool: Get MAST metadata ---
@mcp.tool(
    title="Get MAST Metadata",
    description="Get metadata about MAST observations or products.",
)
async def get_mast_metadata(data_type: str) -> str:
    """Get MAST metadata for observations or products.
    
    Parameters
    ----------
    data_type : str
        Type of metadata to retrieve: 'observations' or 'products'
    """
    meta_table = Observations.get_metadata(data_type)
    lines = [f"{row['Column Name']}: {row['Column Label']}" for row in meta_table]
    text_output = f"Metadata fields for {data_type}:\n"
    text_output += "\n".join(lines)
    return text_output


# --- Tool: Query observations ---
@mcp.tool(
    title="Query MAST Observations",
    description="Query MAST observations for a specified target and/or any additional criteria.",
)
async def mast_observation_query(
    target: str = "",
    radius: str = "0.02 deg",
    mission_name: str = None,
    dataproduct_type: str = None,
    instrument_name: str = None,
    filters: str = None,
    hlsp_name: str = None,
    proposal_id: str = None,
    wavelength_region: str = None,
) -> str:
    """Query MAST observations for for specified target or by criteria.

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
    proposal_id : str, optional
        Filter by proposal ID (optional).
    wavelength_region : str, optional
        Filter by wavelength region (optional).
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
    if proposal_id is not None and proposal_id != "":
        kwargs["proposal_id"] = proposal_id
    if wavelength_region is not None and wavelength_region != "":
        kwargs["wavelength_region"] = f"*{wavelength_region}*"

    # The actual query
    if len(kwargs) == 0:
        obs_table = Observations.query_object(target, radius=radius)
    elif target == "":
        # If no target, use query_criteria only
        obs_table = Observations.query_criteria(**kwargs)
    else:
        # Use query_criteria with additional filters
        obs_table = Observations.query_criteria(
            objectname=target,
            radius=radius,
            **kwargs,
        )

    if len(obs_table) == 0:
        return f"No observations found for target: {target} within radius: {radius}"
    
    # Only consider some columns
    col_list = [
        "obs_id",
        "obs_collection",
        "dataproduct_type",
        "instrument_name",
        "filters",
        "t_exptime",
        "s_ra",
        "s_dec",
        "obs_title",
        "wavelength_region",
        "target_name",
        "target_classification",
        "proposal_id",
        "obsid",
    ]
    obs_table = obs_table[col_list]
    # Rename obsid to avoid confusion with obs_id
    obs_table.rename_column("obsid", "obs_numeric_id")

    print(f"Found {len(obs_table)} observations for target: {target}")

    # Return full table if results are 100 or fewer
    if len(obs_table) <= 100:
        text_table = obs_table.pformat(max_lines=-1, max_width=-1)
        text_table = "\n".join(text_table)
        text_output = f"Found {len(obs_table)} observations found for target: {target} within radius: {radius}:\n"
        text_output += text_table
        return text_output

    # Make a summary count by mission if more than 100 results

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
    """Get details for a specific MAST observation by obs_id.
    
    Parameters
    ----------
    obs_id : str
        The observation ID to get details for.
    """

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


@mcp.tool(
    title="Get MAST Product/File List",
    description="Get product/file list for given observation numeric IDs.",
)
async def mast_get_product_list(obs_numeric_id_list: list[int]) -> str:
    """Get product list for given observation IDs.
    
    Parameters
    ----------
    obs_numeric_id_list : list[int]
        List of observation numeric IDs to get products for.
    """

    # Converting to a list of strings, but still using the number IDs (obsid)
    if isinstance(obs_numeric_id_list, str):
        # String of comma-separated IDs
        obs_numeric_id_list = [x for x in obs_numeric_id_list.split(",")]
    elif isinstance(obs_numeric_id_list, list) and len(obs_numeric_id_list) > 0 and isinstance(obs_numeric_id_list[0], int):
        # List of integers
        obs_numeric_id_list = [str(x) for x in obs_numeric_id_list]
    else:
        # Single value
        obs_numeric_id_list = [str(obs_numeric_id_list)]

    products = Observations.get_unique_product_list(obs_numeric_id_list)
    if len(products) == 0:
        return "No products found for the given observation IDs."

    if len(products) > 100:
        # Group by obs_id and count
        obs_ids = [prod["obs_id"] for prod in products]
        counts = Counter(obs_ids)
        # Prepare output: obs_id and count
        lines = [
            f"Found {len(products)} products for the given observation IDs. Summary by obs_id:"
        ]
        lines.append(f"{'obs_id':<50}count")
        for obs_id, count in counts.items():
            lines.append(f"{obs_id:<50}{count}")
    else:
        # Prepare output: key details of the products
        lines = [
            f"Found {len(products)} products for the given observation IDs. Details:"
        ]
        for product in products:
            line = f"File: {product['productFilename']}, Type: {product['productType']}, URI: {product['dataURI']}"
            lines.append(line)

    text_output = "Products for the given observation IDs:\n"
    text_output += "\n".join(lines)

    return text_output
