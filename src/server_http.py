# Prototype for MAST MCP server
# Main file to organize all the tools
# Streamable HTTP version

from src import observations, exomast
from starlette.responses import JSONResponse
from fastmcp import FastMCP
from fastapi import FastAPI

# ---------
# MCP Server
mcp = FastMCP(name="MAST MCP")
mcp.mount(observations.mcp)
mcp.mount(exomast.mcp)

mcp_app = mcp.http_app(path="/mcp")

# ---------
# API
api = FastAPI(lifespan=mcp_app.lifespan)

# Health check
@api.get("/api/status")
def status():
    return {"status": "ok"}

# Mounting MCP to API
api.mount("/mcp", mcp_app)

# ---------
# Run with uvicorn: 
# uvicorn src.server_http:api --host 0.0.0.0 --port 8000