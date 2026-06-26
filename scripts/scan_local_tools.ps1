# scan_local_tools.ps1
# Scans your Windows PC for all AI agents, LLMs, dev tools, extensions,
# and capabilities relevant to InDesign automation.
# Run: powershell -ExecutionPolicy Bypass -File scripts/scan_local_tools.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  LOCAL AGENT & TOOLS SCANNER" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$report = @{}

# --- 1. AI/LLM CLI Tools ---
Write-Host "[1/8] Scanning AI/LLM CLI tools..." -ForegroundColor Yellow
$aiTools = @("claude", "ollama", "aider", "interpreter", "copilot", "cursor",
             "goose", "opencode", "amp", "letta", "mux", "chatgpt",
             "gemini", "openai", "anthropic", "litellm", "vllm")
$foundTools = @()
foreach ($tool in $aiTools) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        $foundTools += [PSCustomObject]@{
            Name = $tool
            Path = $cmd.Source
            Version = try { & $tool --version 2>$null | Select-Object -First 1 } catch { "unknown" }
        }
    }
}
$report["ai_cli_tools"] = $foundTools
Write-Host "  Found: $($foundTools.Count) AI CLI tools" -ForegroundColor Green
$foundTools | Format-Table Name, Path -AutoSize

# --- 2. Ollama Models ---
Write-Host "[2/8] Scanning Ollama models..." -ForegroundColor Yellow
$ollamaModels = @()
try {
    $models = ollama list 2>$null
    if ($models) {
        $ollamaModels = $models | Select-Object -Skip 1
        Write-Host "  Found: $(($ollamaModels | Measure-Object).Count) models" -ForegroundColor Green
        $models | Write-Host
    }
} catch {
    Write-Host "  Ollama not running or not installed" -ForegroundColor Red
}
$report["ollama_models"] = $ollamaModels

# --- 3. VS Code Extensions (AI/Agent related) ---
Write-Host "`n[3/8] Scanning VS Code extensions..." -ForegroundColor Yellow
$patterns = "claude|copilot|continue|cody|cursor|aider|openai|ollama|mcp|indesign|extend|agent|ai-|gpt|gemini|anthropic|interpreter"
try {
    $allExtensions = code --list-extensions 2>$null
    $aiExtensions = $allExtensions | Select-String -Pattern $patterns
    $report["vscode_ai_extensions"] = $aiExtensions
    Write-Host "  Found: $(($aiExtensions | Measure-Object).Count) AI/agent extensions" -ForegroundColor Green
    $aiExtensions | ForEach-Object { Write-Host "    $_" }
} catch {
    Write-Host "  VS Code CLI not available" -ForegroundColor Red
}

# --- 4. MCP Server Configurations ---
Write-Host "`n[4/8] Scanning MCP configurations..." -ForegroundColor Yellow
$mcpPaths = @(
    "$env:APPDATA\Claude\claude_desktop_config.json",
    "$HOME\.claude\claude_desktop_config.json",
    "$HOME\.config\claude\config.json",
    "$HOME\.cursor\mcp.json",
    ".\.mcp.json",
    ".\mcp.json"
)
$foundMcp = @()
foreach ($p in $mcpPaths) {
    if (Test-Path $p) {
        $foundMcp += $p
        Write-Host "  Found: $p" -ForegroundColor Green
        try {
            $content = Get-Content $p -Raw | ConvertFrom-Json
            if ($content.mcpServers) {
                $content.mcpServers.PSObject.Properties | ForEach-Object {
                    Write-Host "    Server: $($_.Name) -> $($_.Value.command) $($_.Value.args -join ' ')" -ForegroundColor White
                }
            }
        } catch {}
    }
}
if ($foundMcp.Count -eq 0) {
    Write-Host "  No MCP configs found (you haven't registered any MCP servers yet)" -ForegroundColor DarkYellow
}
$report["mcp_configs"] = $foundMcp

# --- 5. Python Packages (AI/automation related) ---
Write-Host "`n[5/8] Scanning Python packages..." -ForegroundColor Yellow
$pyPackages = @("pywin32", "win32com", "mcp", "open-interpreter", "openai",
                "anthropic", "ollama", "langchain", "autogen", "crewai",
                "pillow", "reportlab", "pypdf", "fastapi", "flask", "httpx")
$installedPy = @()
foreach ($pkg in $pyPackages) {
    $result = pip show $pkg 2>$null
    if ($LASTEXITCODE -eq 0) {
        $version = ($result | Select-String "Version:") -replace "Version: ", ""
        $installedPy += [PSCustomObject]@{ Package = $pkg; Version = $version }
    }
}
Write-Host "  Found: $($installedPy.Count) relevant Python packages" -ForegroundColor Green
$installedPy | Format-Table Package, Version -AutoSize
$report["python_packages"] = $installedPy

# --- 6. Adobe Applications ---
Write-Host "[6/8] Scanning Adobe applications..." -ForegroundColor Yellow
$adobeApps = @()
$adobePaths = @(
    "C:\Program Files\Adobe",
    "C:\Program Files (x86)\Adobe",
    "$env:APPDATA\Adobe"
)
foreach ($ap in $adobePaths) {
    if (Test-Path $ap) {
        Get-ChildItem $ap -Directory -ErrorAction SilentlyContinue | ForEach-Object {
            if ($_.Name -match "InDesign|Photoshop|Illustrator|Acrobat|Bridge|ExtendScript") {
                $adobeApps += $_.FullName
                Write-Host "  Found: $($_.Name)" -ForegroundColor Green
            }
        }
    }
}
# Check COM registration
try {
    $indesignCOM = Get-ItemProperty "HKLM:\SOFTWARE\Classes\InDesign.Application\CLSID" -ErrorAction SilentlyContinue
    if ($indesignCOM) {
        Write-Host "  InDesign COM registered (can automate via pywin32)" -ForegroundColor Green
        $adobeApps += "COM:InDesign.Application"
    }
} catch {}
$report["adobe_apps"] = $adobeApps

# --- 7. Node.js / npm Tools ---
Write-Host "`n[7/8] Scanning Node.js tools..." -ForegroundColor Yellow
$nodeTools = @("node", "npm", "npx", "pnpm", "bun")
$foundNode = @()
foreach ($nt in $nodeTools) {
    $cmd = Get-Command $nt -ErrorAction SilentlyContinue
    if ($cmd) {
        $ver = try { & $nt --version 2>$null | Select-Object -First 1 } catch { "?" }
        $foundNode += [PSCustomObject]@{ Tool = $nt; Version = $ver; Path = $cmd.Source }
    }
}
$foundNode | Format-Table Tool, Version -AutoSize
# Check for global MCP/agent npm packages
try {
    $globalPkgs = npm list -g --depth=0 2>$null
    $agentPkgs = $globalPkgs | Select-String -Pattern "mcp|agent|claude|openai|langchain"
    if ($agentPkgs) {
        Write-Host "  Global npm agent packages:" -ForegroundColor Green
        $agentPkgs | ForEach-Object { Write-Host "    $_" }
    }
} catch {}
$report["node_tools"] = $foundNode

# --- 8. Git & GitHub ---
Write-Host "`n[8/8] Scanning Git/GitHub setup..." -ForegroundColor Yellow
$gitInfo = @{}
try {
    $gitInfo["version"] = git --version 2>$null
    $gitInfo["user"] = git config --global user.name 2>$null
    $gitInfo["email"] = git config --global user.email 2>$null
    $ghCmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($ghCmd) { $gitInfo["gh_cli"] = (gh --version 2>$null | Select-Object -First 1) }
} catch {}
$gitInfo.GetEnumerator() | ForEach-Object { Write-Host "  $($_.Key): $($_.Value)" }
$report["git"] = $gitInfo

# --- Summary ---
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SCAN COMPLETE — SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "AI CLI Tools:        $($foundTools.Count)" -ForegroundColor White
Write-Host "Ollama Models:       $(($ollamaModels | Measure-Object).Count)" -ForegroundColor White
Write-Host "VS Code Extensions:  $(($aiExtensions | Measure-Object).Count) (AI/agent related)" -ForegroundColor White
Write-Host "MCP Configs:         $($foundMcp.Count)" -ForegroundColor White
Write-Host "Python Packages:     $($installedPy.Count) (AI/automation)" -ForegroundColor White
Write-Host "Adobe Apps:          $($adobeApps.Count)" -ForegroundColor White
Write-Host ""

# --- Export to JSON ---
$outputPath = Join-Path (Get-Location) "local-agent-scan-report.json"
try {
    $report | ConvertTo-Json -Depth 4 | Out-File $outputPath -Encoding UTF8
    Write-Host "Full report saved: $outputPath" -ForegroundColor Green
    Write-Host "Share this file with Devin for recommendations.`n" -ForegroundColor DarkYellow
} catch {
    Write-Host "Could not save report file (non-critical)" -ForegroundColor DarkYellow
}
