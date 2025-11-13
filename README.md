# MAST MCP Prototype

## What is MCP?

MCP (Model Context Protocol) is a protocol for building AI agents that can access external tools and data sources. 
We are using [FastMCP](https://gofastmcp.com/getting-started/welcome) to build a few simple calls to the MAST Archive..

## Setup

Install requirements (eg, `uv sync`) for the app.   
You will need to have `uv` installed for clients to access it. You can do this with `brew install uv`.

You can test it with `fastmcp run src/server.py` but to best use it you want to install it to a client.   
To do this, use the `fastmcp install` commands. For example: 
```bash
fastmcp install cursor src/server.py -n MAST-MCP
```
Depending on your setup, you may need to add `--project` to run within a particular project directory ensuring `uv` finds the correct environment.

For VSCode you may need to produce the mcp-json format, which may look something like:
```json
{
  "MAST-MCP": {
    "command": "uv",
    "args": [
      "run",
      "--project",
      "C:\\Users\\strak\\Projects\\mast-mcp-prototype",
      "--with",
      "fastmcp",
      "fastmcp",
      "run",
      "C:\\Users\\strak\\Projects\\mast-mcp-prototype\\src\\server.py"
    ]
  }
}
```

### Streamable HTTP version

If you want to use the MCP in a streamable HTTP version, you can use the `server_http.py` file.
This will allow you to host the MCP on a web server and access it via HTTP.

```bash
uvicorn src.server_http:api --reload
```

## Example

Get the properties of a given exoplanet by name:
```
What is the orbital separation for exoplanet HR-8799b?
```

Generate prompt to summarize the properties after fetching them (exact call will vary depending on the client):
```
/MAST-MCP/Summarize exoplanet properties 
```

Get observations for a given target:
```
What observations exist in MAST for V4046 Sgr? Use a radius of 0 degrees.
```

Get product list for a given observation:
```
What products exist in MAST for TW Hya? Use a radius of 0 degrees and only consider HST observations using the COS instrument.
```
