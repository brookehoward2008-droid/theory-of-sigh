# InDesign MCP Server

A Model Context Protocol (MCP) server that lets Claude Code (or any MCP-compatible agent) control Adobe InDesign directly.

## What it does

When running on your Windows machine alongside InDesign, this server exposes tools that agents can call:

| Tool | Description |
|------|-------------|
| `run_jsx` | Execute arbitrary ExtendScript in InDesign |
| `run_jsx_file` | Run a .jsx file in InDesign |
| `build_handoff` | Full handoff package → InDesign document pipeline |
| `get_document_info` | Get active document metadata (pages, links, frames) |
| `export_pdf` | Export to PDF with configurable preset |
| `place_image` | Place an image at exact coordinates (mm) |
| `add_text_frame` | Add text at exact coordinates (mm) |
| `list_pages` | List all pages with item counts |
| `new_document` | Create a new document with specs |
| `save_document` | Save the active document |
| `close_document` | Close the active document |

## Setup (one-time)

### 1. Install dependencies

```powershell
pip install mcp pywin32
```

If `pywin32` has issues, also run:
```powershell
python -m pywin32_postinstall -install
```

### 2. Register with Claude Code

Copy the MCP config into your Claude Code settings:

**Option A: Edit the config file directly**

Open (or create) `%APPDATA%\Claude\claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "indesign": {
      "command": "python",
      "args": ["C:/Users/toddl/OneDrive/Documents/GitHub/theory-of-sigh/scripts/indesign_mcp_server.py"],
      "env": {
        "PYTHONPATH": "C:/Users/toddl/OneDrive/Documents/GitHub/theory-of-sigh/scripts"
      }
    }
  }
}
```

**Option B: Use the 1-Click MCP Installer VS Code extension**

You already have `veduis.1-click-mcp-installer` — use it to register the server path.

### 3. Launch InDesign

Make sure Adobe InDesign is running before starting a Claude Code session. The MCP server connects via COM when a tool is first called.

## Usage with Claude Code

Once registered, start a Claude Code session and you can say things like:

```
"Build the handoff package into InDesign"
→ calls build_handoff("C:\Users\toddl\Desktop\handoff_package_final")

"Show me info about the current document"
→ calls get_document_info()

"Place an image at x=40mm y=20mm on page 3"
→ calls place_image(3, 40, 20, 100, 80, "C:\path\to\image.png")

"Export the current document to PDF"
→ calls export_pdf()

"Run this script in InDesign: app.activeDocument.pages.length"
→ calls run_jsx("app.activeDocument.pages.length")
```

## How it works

```
Claude Code  ←stdio→  indesign_mcp_server.py  ←COM→  Adobe InDesign
```

- Claude Code spawns `indesign_mcp_server.py` as a subprocess
- They communicate via stdin/stdout using the MCP protocol (JSON-RPC)
- The server translates tool calls into InDesign COM automation via `pywin32`
- InDesign executes ExtendScript and returns results

## Troubleshooting

**"InDesign COM automation requires Windows"**
→ The server must run on Windows with InDesign installed.

**"Could not connect to InDesign over COM"**
→ Make sure InDesign is open. The server tries multiple COM ProgIDs (2021-2024).

**"pywin32" import error**
→ Run: `python -m pip install --upgrade pywin32 && python -m pywin32_postinstall -install`

**Server not appearing in Claude Code**
→ Check that `claude_desktop_config.json` has the correct path to the script.
→ Restart Claude Code after editing the config.
