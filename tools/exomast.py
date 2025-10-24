# ExoMAST MCP - Exoplanet Data Access

import requests
import urllib.parse
from typing import Optional, Dict, Any
from fastmcp import FastMCP

HTTP_ROOT = "https://exo.mast.stsci.edu/"

mcp = FastMCP("ExoMAST MCP")


@mcp.resource("config://exomast-version")
def get_exomast_version():
    return "ExoMAST API v0.1"


@mcp.tool(title="Search for an exoplanet by its name", description="Search for an exoplanet by its name")
async def search_exoplanet_by_name(
    name: str,
    flatten_response: bool = False,
    format: Optional[str] = None,
    delimiter: Optional[str] = None,
    raw: bool = False,
    include_info: bool = False
) -> str:
    """Search for an exoplanet by its name"""
    params = {
        "flatten_response": flatten_response,
        "raw": raw,
        "include_info": include_info
    }
    if format:
        params["format"] = format
    if delimiter:
        params["delimiter"] = delimiter
    
    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/resolver/{urllib.parse.quote(name)}"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return str(response.json())


@mcp.tool(title="Get exoplanet identifiers", description="Search for an exoplanet by its (possibly non-canonical) name")
async def get_exoplanet_identifiers(name: str) -> str:
    """Search for an exoplanet by its (possibly non-canonical) name"""
    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/identifiers/?name={urllib.parse.quote(name)}"
    response = requests.get(url)
    response.raise_for_status()
    return str(response.json())


@mcp.tool(title="Get exoplanet properties", description="Get exoplanet properties for a given exoplanet ID")
async def get_exoplanet_properties(
    exoplanet_id: str,
    flatten_response: bool = False,
    format: Optional[str] = None,
    delimiter: Optional[str] = None,
    raw: bool = False,
    include_info: bool = False
) -> str:
    """Get exoplanet properties for a given exoplanet ID"""
    params = {
        "flatten_response": flatten_response,
        "raw": raw,
        "include_info": include_info
    }
    if format:
        params["format"] = format
    if delimiter:
        params["delimiter"] = delimiter
    
    url = f"{HTTP_ROOT}/api/v0.1/exoplanets/{urllib.parse.quote(exoplanet_id)}/properties"
    response = requests.get(url, params=params)
    response.raise_for_status()
    return str(response.json())
