# mast-mcp-prototype
MAST MCP Prototype

Install requirements then run: 
```bash
fastmcp run mast.py
```

To better use it, you will want to add it to a client, use the `fastmcp install` commands.   
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
