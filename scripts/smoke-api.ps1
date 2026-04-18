param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$base = $BaseUrl.TrimEnd('/')

$targets = @(
    "$base/health",
    "$base/events?page=1&size=10",
    "$base/events/5",
    "$base/docs"
)

$allOk = $true

foreach ($url in $targets) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 30
        Write-Host "[OK] $url -> $($response.StatusCode)"
    }
    catch {
        $allOk = $false
        if ($_.Exception.Response) {
            $statusCode = [int]$_.Exception.Response.StatusCode
            Write-Host "[FAIL] $url -> $statusCode"
        }
        else {
            Write-Host "[FAIL] $url -> $($_.Exception.Message)"
        }
    }
}

if (-not $allOk) {
    exit 1
}
