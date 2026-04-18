param(
    [switch]$OnlyBase,
    [switch]$OnlyLocalDb
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Wait-Http200 {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Url,
        [int]$Attempts = 80,
        [int]$DelayMs = 500,
        [int]$TimeoutSec = 3
    )

    for ($i = 0; $i -lt $Attempts; $i++) {
        try {
            $resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec $TimeoutSec
            if ($resp.StatusCode -eq 200) {
                return $true
            }
        }
        catch {
            # Retry until timeout budget is consumed.
        }

        [System.Threading.Thread]::Sleep($DelayMs)
    }

    return $false
}

function Run-BaseMode {
    Write-Host "[smoke] compose base (sin DB local)"
    docker compose down -v --remove-orphans | Out-Null
    docker compose up -d --build api php-client | Out-Null

    if (-not (Wait-Http200 -Url 'http://127.0.0.1:8000/health')) {
        throw "API /health no respondió 200 en modo base"
    }

    $eventsOk = Wait-Http200 -Url 'http://127.0.0.1:8000/events?page=1&size=5'
    if (-not $eventsOk) {
        throw "API /events no respondió 200 en modo base"
    }

    if (-not (Wait-Http200 -Url 'http://127.0.0.1:8080/index.php')) {
        throw "Demo PHP no respondió 200 en modo base"
    }

    docker compose down | Out-Null
    Write-Host "[ok] compose base"
}

function Run-LocalDbMode {
    Write-Host "[smoke] compose + local-db"
    docker compose -f docker-compose.yml -f docker-compose.local-db.yml down -v --remove-orphans | Out-Null
    docker compose -f docker-compose.yml -f docker-compose.local-db.yml up -d --build api db php-client | Out-Null

    if (-not (Wait-Http200 -Url 'http://127.0.0.1:8000/ready' -Attempts 120 -TimeoutSec 4)) {
        throw "API /ready no respondió 200 en modo local-db"
    }

    if (-not (Wait-Http200 -Url 'http://127.0.0.1:8000/events?page=1&size=5' -Attempts 120 -TimeoutSec 4)) {
        throw "API /events no respondió 200 en modo local-db"
    }

    if (-not (Wait-Http200 -Url 'http://127.0.0.1:8080/index.php')) {
        throw "Demo PHP no respondió 200 en modo local-db"
    }

    docker compose -f docker-compose.yml -f docker-compose.local-db.yml down | Out-Null
    Write-Host "[ok] compose + local-db"
}

if ($OnlyBase -and $OnlyLocalDb) {
    throw "No puedes usar -OnlyBase y -OnlyLocalDb al mismo tiempo"
}

if ($OnlyBase) {
    Run-BaseMode
}
elseif ($OnlyLocalDb) {
    Run-LocalDbMode
}
else {
    Run-BaseMode
    Run-LocalDbMode
}

Write-Host "[ok] smoke docker compose completo"