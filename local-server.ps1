[CmdletBinding()]
param([switch]$NoBrowser)
$ErrorActionPreference = "Stop"
$siteRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "dist"))
if (-not (Test-Path -LiteralPath (Join-Path $siteRoot "index.html"))) {
  Write-Host "Built site not found. Run npm install and npm run build first." -ForegroundColor Red
  Read-Host "Press Enter to exit"
  exit 1
}
$port = 4174
$url = "http://127.0.0.1:$port/"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$mimeTypes = @{ ".html"="text/html; charset=utf-8"; ".css"="text/css; charset=utf-8"; ".js"="text/javascript; charset=utf-8"; ".json"="application/json; charset=utf-8"; ".svg"="image/svg+xml"; ".webp"="image/webp"; ".png"="image/png"; ".jpg"="image/jpeg"; ".jpeg"="image/jpeg"; ".glb"="model/gltf-binary"; ".woff2"="font/woff2"; ".pdf"="application/pdf"; ".txt"="text/plain; charset=utf-8"; ".md"="text/markdown; charset=utf-8"; ".wav"="audio/wav" }
try {
  $listener.Start()
  Write-Host "SEE / SHOW DESIGN STUDIO is running at $url" -ForegroundColor Green
  Write-Host "Close this window to stop the local site."
  if (-not $NoBrowser) { Start-Process $url }
  while ($listener.IsListening) {
    $context = $listener.GetContext()
    $relativePath = [System.Uri]::UnescapeDataString($context.Request.Url.AbsolutePath.TrimStart("/"))
    if ([string]::IsNullOrWhiteSpace($relativePath)) { $relativePath = "index.html" }
    $requestedPath = [System.IO.Path]::GetFullPath((Join-Path $siteRoot $relativePath))
    if (-not $requestedPath.StartsWith($siteRoot, [System.StringComparison]::OrdinalIgnoreCase)) { $context.Response.StatusCode=403; $context.Response.Close(); continue }
    if (-not (Test-Path -LiteralPath $requestedPath -PathType Leaf)) { $context.Response.StatusCode=404; $context.Response.Close(); continue }
    $bytes = [System.IO.File]::ReadAllBytes($requestedPath)
    $extension = [System.IO.Path]::GetExtension($requestedPath).ToLowerInvariant()
    $context.Response.ContentType = if ($mimeTypes.ContainsKey($extension)) { $mimeTypes[$extension] } else { "application/octet-stream" }
    $context.Response.ContentLength64 = $bytes.Length
    if ($context.Request.HttpMethod -ne "HEAD") { $context.Response.OutputStream.Write($bytes,0,$bytes.Length) }
    $context.Response.OutputStream.Close()
  }
} finally { if ($listener.IsListening) { $listener.Stop() }; $listener.Close() }


