param(
  [switch]$SkipFrontend
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

function Invoke-CheckedNative {
  param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,
    [string[]]$Arguments
  )

  & $FilePath @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "$FilePath failed with exit code $LASTEXITCODE"
  }
}

Write-Host "== Backend structure =="
Invoke-CheckedNative -FilePath powershell -Arguments @("-ExecutionPolicy", "Bypass", "-File", "scripts/verify-backend-structure.ps1")

Write-Host "== Backend API workflows =="
Invoke-CheckedNative -FilePath python -Arguments @("scripts/validate-api.py")

if (-not $SkipFrontend) {
  Write-Host "== Frontend install =="
  Push-Location frontend-web
  try {
    Invoke-CheckedNative -FilePath npm.cmd -Arguments @("install")

    Write-Host "== Frontend build =="
    Invoke-CheckedNative -FilePath npm.cmd -Arguments @("run", "build")

    Write-Host "== Frontend tests =="
    $env:CI = "true"
    Invoke-CheckedNative -FilePath npm.cmd -Arguments @("test", "--", "--watchAll=false")
  } finally {
    Pop-Location
  }
}

Write-Host "Project validation passed."
