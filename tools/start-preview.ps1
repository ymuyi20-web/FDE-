$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$port = 8765
$url = "http://127.0.0.1:$port/"

function Test-PreviewServer {
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 1
        return $response.StatusCode -eq 200
    }
    catch {
        return $false
    }
}

if (-not (Test-PreviewServer)) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show(
            "Python was not found. The local preview server cannot start.",
            "FDE Learning Console"
        ) | Out-Null
        exit 1
    }

    $arguments = @(
        "-m", "http.server", "$port",
        "--bind", "127.0.0.1",
        "--directory", "`"$projectRoot`""
    )

    Start-Process -FilePath $python.Source -ArgumentList $arguments -WindowStyle Hidden

    $ready = $false
    for ($attempt = 0; $attempt -lt 20; $attempt++) {
        Start-Sleep -Milliseconds 250
        if (Test-PreviewServer) {
            $ready = $true
            break
        }
    }

    if (-not $ready) {
        Add-Type -AssemblyName PresentationFramework
        [System.Windows.MessageBox]::Show(
            "The local preview server did not start. Please try again.",
            "FDE Learning Console"
        ) | Out-Null
        exit 1
    }
}

Start-Process $url
