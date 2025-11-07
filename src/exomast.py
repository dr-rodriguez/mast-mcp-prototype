# ExoMAST MCP - Exoplanet Data Access

import requests
import urllib.parse
from typing import Optional, Dict, Any
from fastmcp import FastMCP
import yaml

HTTP_ROOT = "https://exo.mast.stsci.edu/"

mcp = FastMCP("ExoMAST MCP")


@mcp.resource("config://exomast-version")
def get_exomast_version():
    return "ExoMAST API v0.1"


@mcp.tool(title="Search for an exoplanet by its name and get properties", description="Search for an exoplanet by its name and get properties")
async def search_exoplanet_properties(
    name: str,
) -> str:
    """Search for an exoplanet by its name and get properties"""

    # Step 1: Get planet identifiers
    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/identifiers/?name={urllib.parse.quote(name)}"
    response = requests.get(url)
    response.raise_for_status()
    identifiers = response.json()

    # Step 2: Get the canonical name, if present
    canonical_name = identifiers.get("canonicalName")
    if canonical_name is None:
        canonical_name = name

    params = {
        "flatten_response": False,
        "raw": False,
        "include_info": True,
        "format": "json"
    }

    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/resolver/{urllib.parse.quote(canonical_name)}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Extract the exoplanetID from the data
    if len(data) == 0 or len(data[0]) == 0:
        yaml_data = yaml.dump(data)
        return f"Error fetching exoplanet with name: {name}.\nData: {yaml_data}"
    else:
        exoplanet_id = data[0].get("exoplanetID")

    # Step 3: Get the exoplanet properties
    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/{exoplanet_id}/properties"
    response = requests.get(url, params=params)
    response.raise_for_status()

    # Convert json to yaml
    result_yaml = yaml.dump(response.json())

    return result_yaml

@mcp.prompt("Summarize-exoplanet-properties")
async def summarize_exoplanet_properties() -> str:
    """Summarize exoplanet properties from ExoMAST"""
    prompt = "Summarize the planet properties by producing a table for each survey (eg, NexScI, TESS, etc.)"
    prompt += "Each table should have (if provided) the planet name, orbital period, orbital separation, planet radius, planet mass, and provide references for each."
    return prompt
