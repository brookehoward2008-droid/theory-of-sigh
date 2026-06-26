#Requires -Version 5.1
<#
.SYNOPSIS
    Inventories locally installed AI tooling, agent / MCP configuration files,
    and which AI-provider API-key environment variables are set.

.DESCRIPTION
    A read-only audit for your own machine. It reports the *presence* of
    well-known AI configuration files and API-key environment variables.

    For privacy and safety the script deliberately:
      * NEVER reads, prints, or transmits the contents of any config file.
      * NEVER prints the value of any API key - only whether one is set.
      * Makes no network calls. Results stay on the local machine.

    Output is written to the console as a table. Optionally the same data can
    be written to a local JSON or CSV file (-ExportPath) and/or emitted to the
    pipeline (-PassThru) for further processing.

.PARAMETER ExportPath
    Optional path to save the report. The format is inferred from the file
    extension: ".json" writes JSON, ".csv" writes CSV. Any other extension
    falls back to JSON.

.PARAMETER PassThru
    Emit the report rows as objects to the pipeline in addition to printing.

.EXAMPLE
    .\Scan-AIEnvironments.ps1
    Print the full report to the console.

.EXAMPLE
    .\Scan-AIEnvironments.ps1 -ExportPath .\ai-report.json
    Print the report and also save it as JSON.

.EXAMPLE
    $rows = .\Scan-AIEnvironments.ps1 -PassThru
    Capture the report rows for scripting.

.NOTES
    Targets Windows paths first (%APPDATA%, %USERPROFILE%) and falls back to
    $HOME so it also runs under PowerShell 7 on macOS / Linux.
#>
[CmdletBinding()]
param(
    [string] $ExportPath,
    [switch] $PassThru
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Resolve a home / appdata base that works on Windows PowerShell and pwsh alike.
$HomeDir = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$AppData = if ($env:APPDATA)     { $env:APPDATA }     else { Join-Path $HomeDir '.config' }

# ---------------------------------------------------------------------------
# Report accumulator. Each row: Category / Name / Status / Detail.
# ---------------------------------------------------------------------------
$Report = [System.Collections.Generic.List[pscustomobject]]::new()

function Add-Finding {
    param(
        [Parameter(Mandatory)][string] $Category,
        [Parameter(Mandatory)][string] $Name,
        [Parameter(Mandatory)][string] $Status,
        [string] $Detail = ''
    )
    $Report.Add([pscustomobject]@{
        Category = $Category
        Name     = $Name
        Status   = $Status
        Detail   = $Detail
    })
}

Write-Host "Scanning this PC for AI environments and configurations..." -ForegroundColor Cyan
Write-Host "(read-only: file contents and key values are never read or printed)" -ForegroundColor DarkGray

# ---------------------------------------------------------------------------
# 1. Model Context Protocol (MCP), agent, and local-model configurations.
# ---------------------------------------------------------------------------
$PathsToScan = [ordered]@{
    'Claude Desktop config' = Join-Path $AppData  'Claude\claude_desktop_config.json'
    'Claude Code config'    = Join-Path $HomeDir  '.claude.json'
    'Claude Code directory' = Join-Path $HomeDir  '.claude'
    'VS Code MCP config'    = Join-Path $HomeDir  '.vscode\mcp.json'
    'Cursor MCP config'     = Join-Path $HomeDir  '.cursor\mcp.json'
    'Continue config'       = Join-Path $HomeDir  '.continue\config.json'
    'Ollama models'         = Join-Path $HomeDir  '.ollama'
    'LM Studio directory'   = Join-Path $HomeDir  '.lmstudio'
}

foreach ($name in $PathsToScan.Keys) {
    $target = $PathsToScan[$name]
    if (Test-Path -LiteralPath $target) {
        Add-Finding -Category 'Config / Tooling' -Name $name -Status 'Found' -Detail $target
    } else {
        Add-Finding -Category 'Config / Tooling' -Name $name -Status 'Not present'
    }
}

# ---------------------------------------------------------------------------
# 2. AI-provider API-key environment variables (presence only, never values).
# ---------------------------------------------------------------------------
Write-Host "`nChecking AI-provider API-key environment variables..." -ForegroundColor Yellow
$TargetKeys = @(
    'ANTHROPIC_API_KEY'
    'OPENAI_API_KEY'
    'OPENROUTER_API_KEY'
    'GOOGLE_API_KEY'
    'GEMINI_API_KEY'
    'MISTRAL_API_KEY'
    'GROQ_API_KEY'
    'COHERE_API_KEY'
    'HF_TOKEN'
)

foreach ($key in $TargetKeys) {
    $value = [Environment]::GetEnvironmentVariable($key)
    if (-not [string]::IsNullOrWhiteSpace($value)) {
        # Report length only - enough to confirm it is set without leaking it.
        Add-Finding -Category 'API key (env)' -Name $key -Status 'Set' `
            -Detail ("length {0}" -f $value.Length)
    } else {
        Add-Finding -Category 'API key (env)' -Name $key -Status 'Not set'
    }
}

# ---------------------------------------------------------------------------
# 3. Output.
# ---------------------------------------------------------------------------
Write-Host "`nSystem AI inventory:" -ForegroundColor Green
$Report | Format-Table -AutoSize

if ($ExportPath) {
    $ext = [System.IO.Path]::GetExtension($ExportPath).ToLowerInvariant()
    switch ($ext) {
        '.csv'  { $Report | Export-Csv -LiteralPath $ExportPath -NoTypeInformation -Encoding UTF8 }
        default { $Report | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $ExportPath -Encoding UTF8 }
    }
    Write-Host ("Report saved to {0}" -f (Resolve-Path -LiteralPath $ExportPath)) -ForegroundColor Cyan
}

if ($PassThru) {
    $Report
}
