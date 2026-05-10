param(
  [string]$ProjectRoot = "."
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path $ProjectRoot
Set-Location $root

$requiredFiles = @(
  "main.py",
  "requirements.txt",
  "Procfile",
  "render.yaml",
  "backend/__init__.py",
  "backend/main.py",
  "backend/requirements.txt",
  "backend/app/__init__.py",
  "backend/app/main.py",
  "backend/app/routes/__init__.py",
  "backend/app/routes/pdf.py"
)

$requiredPackages = @("fastapi", "uvicorn", "python-multipart", "pydantic")
$requiredRoutes = @(
  "/",
  "/health",
  "/ready",
  "/docs",
  "/openapi.json",
  "/api/meta",
  "/api/pdf/compress",
  "/api/pdf/merge",
  "/api/pdf/split",
  "/api/pdf/rearrange",
  "/api/pdf/pdf-to-word",
  "/api/pdf/pdf-to-image",
  "/api/pdf/image-to-pdf",
  "/api/pdf/watermark",
  "/api/pdf/protect"
)

$missingFiles = $requiredFiles | Where-Object { -not (Test-Path $_) }
if ($missingFiles.Count -gt 0) {
  throw "Missing required deployment files: $($missingFiles -join ', ')"
}

$requirements = Get-Content "backend/requirements.txt"
$missingPackages = $requiredPackages | Where-Object {
  $package = $_
  -not ($requirements | Where-Object { $_ -match "^$([Regex]::Escape($package))(\b|[=<>~\[])" })
}
if ($missingPackages.Count -gt 0) {
  throw "Missing required backend requirements: $($missingPackages -join ', ')"
}

$renderYaml = Get-Content "render.yaml" -Raw
if ($renderYaml -notmatch "rootDir:\s*backend") {
  throw "render.yaml must set rootDir: backend"
}
if ($renderYaml -notmatch "python -m uvicorn app\.main:app --host 0\.0\.0\.0 --port \`$PORT") {
  throw "render.yaml startCommand must use app.main:app with Render `$PORT"
}

$procfile = Get-Content "Procfile" -Raw
if ($procfile -notmatch "python -m uvicorn backend\.app\.main:app --host 0\.0\.0\.0 --port \`$PORT") {
  throw "Procfile must use backend.app.main:app with Render `$PORT"
}

$routeScript = @"
from backend.app.main import app
required = $($requiredRoutes | ConvertTo-Json -Compress)
paths = {getattr(route, 'path', '') for route in app.routes}
missing = sorted(set(required) - paths)
print('Registered routes:')
for path in sorted(paths):
    print(path)
if missing:
    raise SystemExit(f'Missing required routes: {missing}')
print('Backend deployment structure verification passed.')
"@

$routeScript | python -
