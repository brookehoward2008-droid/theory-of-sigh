param(
    [string]$Repository = "https://github.com/brookehoward2008-droid/theory-of-sigh.git"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or is not available on PATH."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "GitHub CLI is missing. Install it from https://cli.github.com/ and run this script again."
    }

    Write-Host "Installing GitHub CLI..." -ForegroundColor Cyan
    winget install --id GitHub.cli --exact --source winget

    $machinePath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = "$machinePath;$userPath"
}

Write-Host "Opening GitHub's secure browser sign-in..." -ForegroundColor Cyan
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git

if (git remote get-url origin 2>$null) {
    git remote set-url origin $Repository
}
else {
    git remote add origin $Repository
}

$branch = git branch --show-current
if (-not $branch) {
    throw "No current Git branch was found."
}

Write-Host "Pushing '$branch' to GitHub..." -ForegroundColor Cyan
git push --set-upstream origin $branch

Write-Host ""
Write-Host "GitHub access is connected and '$branch' is published." -ForegroundColor Green
Write-Host "Repository: $Repository"
