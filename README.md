# mast-mcp-prototype
MAST MCP Prototype

Install requirements (eg, `pip install .`) for the app.   
You will need to have `uv` installed for clients to access it. You can do this with `brew install uv`

You can test it with `fastmcp run mast.py` but to best use it you want to install it to a client.   
To do this, use the `fastmcp install` commands. For example: 
```bash
fastmcp install cursor mast.py -n MAST-MCP
```

For VSCode you may need to produce the mcp-json format, which may look something like:
```json
{
  "MAST-MCP": {
    "command": "uv",
    "args": [
      "run",
      "--with",
      "rpds-py==0.27.1",
	    "--with",
      "astroquery",
      "--with",
      "fastmcp",
      "fastmcp",
      "run",
      "C:\\Users\\strak\\Projects\\mast-mcp-prototype\\mast.py"
    ]
  }
}
```
