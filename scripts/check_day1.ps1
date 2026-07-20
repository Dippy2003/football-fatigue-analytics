$ErrorActionPreference = "Stop"

$RepositoryRoot = Split-Path -Parent $PSScriptRoot

function Invoke-NativeCheck {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    Write-Host "`n==> $Name" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Name failed with exit code $LASTEXITCODE"
    }
}

Push-Location (Join-Path $RepositoryRoot "backend")
try {
    Invoke-NativeCheck "Backend format" { uv run ruff format --check . }
    Invoke-NativeCheck "Backend lint" { uv run ruff check . }
    Invoke-NativeCheck "Backend types" { uv run mypy }
    Invoke-NativeCheck "Backend tests" { uv run pytest }
}
finally {
    Pop-Location
}

Push-Location (Join-Path $RepositoryRoot "frontend")
try {
    Invoke-NativeCheck "Frontend format" { npm.cmd run format:check }
    Invoke-NativeCheck "Frontend lint" { npm.cmd run lint }
    Invoke-NativeCheck "Frontend types" { npm.cmd run typecheck }
    Invoke-NativeCheck "Frontend tests" { npm.cmd test -- --run }
    Invoke-NativeCheck "Frontend build" { npm.cmd run build }
}
finally {
    Pop-Location
}

Push-Location $RepositoryRoot
try {
    Invoke-NativeCheck "Dataset file policy" {
        uv run --project backend python scripts/check_dataset_files.py
    }
    Invoke-NativeCheck "Docker Compose configuration" { docker compose config --quiet }
}
finally {
    Pop-Location
}

Write-Host "`nDay 1 quality checks passed." -ForegroundColor Green
