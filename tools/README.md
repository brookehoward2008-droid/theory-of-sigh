# tools/

Standalone utility scripts that are not part of the book/web build pipeline
(which lives in `scripts/`).

## Scan-AIEnvironments.ps1

A read-only PowerShell audit that inventories AI tooling on the machine it
runs on. It reports:

- **Config / tooling** — whether well-known agent, MCP, and local-model
  configuration files exist (Claude Desktop, Claude Code, VS Code, Cursor,
  Continue, Ollama, LM Studio).
- **API keys (env)** — whether common AI-provider API-key environment
  variables are set (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.).

### Privacy

By design the script **never** reads or prints file contents, and **never**
prints API-key values — only whether each item is present (for keys, just the
character length). It makes no network calls; all output stays local.

### Usage

```powershell
# Print the report to the console
.\Scan-AIEnvironments.ps1

# Print and also save as JSON (or .csv)
.\Scan-AIEnvironments.ps1 -ExportPath .\ai-report.json

# Capture report rows for scripting
$rows = .\Scan-AIEnvironments.ps1 -PassThru
```

Requires Windows PowerShell 5.1+ or PowerShell 7+. Windows paths are checked
first, with a `$HOME` fallback so it also runs on macOS / Linux under `pwsh`.
