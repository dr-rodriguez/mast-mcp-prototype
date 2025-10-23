# mast-mcp-prototype
MAST MCP Prototype

Install requirements (eg, `pip install .`) then run: 
```bash
fastmcp run mast.py
```

You will need to have `uv` installed for clients to access it. You can do this with `brew install uv`

To best use it, you will want to add it to a client, use the `fastmcp install` commands.  
For example, `fastmcp install cursor mast.py -n MAST-MCP`.  

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
      "--with-editable",
      "C:\\Users\\strak\\Projects\\mast-mcp-prototype",
      "fastmcp",
      "run",
      "C:\\Users\\strak\\Projects\\mast-mcp-prototype\\mast.py"
    ]
  }
}
```
