param(
  [string]$ApiBase = $env:RENDER_API_BASE,
  [string]$ApiOrigin = $env:RENDER_API_ORIGIN,
  [string]$SamplePdf = "backend/uploads/RetinalBloodFlowSimulation_Abhinav_2203140_REPORT.pdf",
  [string]$OutputDir = "logs/deployment-smoke"
)

$ErrorActionPreference = "Stop"

function Trim-Slash([string]$Value) {
  if ($null -eq $Value) {
    return ""
  }
  return $Value.TrimEnd("/")
}

function Resolve-ApiBase {
  if ($ApiBase) {
    return Trim-Slash $ApiBase
  }

  if (-not $ApiOrigin) {
    throw "Set RENDER_API_BASE to the full API base, or RENDER_API_ORIGIN to the Render service origin."
  }

  $origin = Trim-Slash $ApiOrigin

  try {
    $meta = Invoke-RestMethod -Uri "$origin/api/meta" -Method GET -TimeoutSec 30
    if ($meta.pdfPrefix) {
      return "$origin$($meta.pdfPrefix)"
    }
  } catch {
    Write-Warning "Route metadata lookup failed: $($_.Exception.Message)"
  }

  try {
    $openApi = Invoke-RestMethod -Uri "$origin/openapi.json" -Method GET -TimeoutSec 30
    $paths = $openApi.paths.PSObject.Properties.Name
    $compressPath = $paths | Where-Object { $_.EndsWith("/compress") } | Select-Object -First 1
    if ($compressPath) {
      return "$origin$($compressPath.Substring(0, $compressPath.Length - '/compress'.Length))"
    }
  } catch {
    Write-Warning "OpenAPI prefix lookup failed: $($_.Exception.Message)"
  }

  return "$origin/api/pdf"
}

function Invoke-ToolSmoke([string]$Name, [string[]]$CurlArgs) {
  $status = curl.exe -sS -w "%{http_code}" @CurlArgs
  [PSCustomObject]@{
    Endpoint = $Name
    Status = $status
    Passed = $status -eq "200"
  }
}

$resolvedBase = Resolve-ApiBase
$root = Resolve-Path "."
$sample = Resolve-Path $SamplePdf
$out = New-Item -ItemType Directory -Force -Path $OutputDir
$pixel = Join-Path $out.FullName "pixel.png"
$pixelBytes = [Convert]::FromBase64String("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII=")
[IO.File]::WriteAllBytes($pixel, $pixelBytes)

$tests = @(
  @{ Name = "compress"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "quality=55", "$resolvedBase/compress", "-o", (Join-Path $out.FullName "compress.pdf")) },
  @{ Name = "merge"; Args = @("-F", "files=@$sample;type=application/pdf", "-F", "files=@$sample;type=application/pdf", "$resolvedBase/merge", "-o", (Join-Path $out.FullName "merge.pdf")) },
  @{ Name = "split"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "ranges=1", "$resolvedBase/split", "-o", (Join-Path $out.FullName "split.zip")) },
  @{ Name = "rearrange"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "order=1", "$resolvedBase/rearrange", "-o", (Join-Path $out.FullName "rearrange.pdf")) },
  @{ Name = "pdf-to-word"; Args = @("-F", "file=@$sample;type=application/pdf", "$resolvedBase/pdf-to-word", "-o", (Join-Path $out.FullName "converted.docx")) },
  @{ Name = "pdf-to-image"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "dpi=72", "$resolvedBase/pdf-to-image", "-o", (Join-Path $out.FullName "images.zip")) },
  @{ Name = "image-to-pdf"; Args = @("-F", "files=@$pixel;type=image/png", "$resolvedBase/image-to-pdf", "-o", (Join-Path $out.FullName "images.pdf")) },
  @{ Name = "watermark"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "text=TEST", "-F", "opacity=0.18", "$resolvedBase/watermark", "-o", (Join-Path $out.FullName "watermark.pdf")) },
  @{ Name = "protect"; Args = @("-F", "file=@$sample;type=application/pdf", "-F", "password=test1234", "$resolvedBase/protect", "-o", (Join-Path $out.FullName "protect.pdf")) }
)

$results = foreach ($test in $tests) {
  Invoke-ToolSmoke -Name $test.Name -CurlArgs $test.Args
}

$logPath = "logs/deployment-verification.md"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss K"
$lines = @(
  "# Deployment Verification Log";
  "";
  "Generated: $timestamp";
  "";
  "Resolved API base: $resolvedBase";
  "";
  "`| Endpoint `| Status `| Passed `|";
  "`| --- `| --- `| --- `|"
)

foreach ($result in $results) {
  $lines += "`| $($result.Endpoint) `| $($result.Status) `| $($result.Passed) `|"
}

$lines | Set-Content -Path $logPath -Encoding UTF8
$results | Format-Table -AutoSize

if ($results.Passed -contains $false) {
  throw "One or more deployment endpoint checks failed. See $logPath."
}

Write-Host "Deployment verification passed. See $logPath."
