#
# KobraStocks setup & launch script for Windows (PowerShell)
# Usage: .\setup.ps1
#
$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RootDir "Backend"
$ClientDir = Join-Path $RootDir "client"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  KobraStocks Setup & Launch" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Python ──────────────────────────────────────────────────────────
$PythonCmd = $null

foreach ($cmd in @("python3.12", "python3.13", "python3.11", "python", "python3")) {
    try {
        $ver = & $cmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>$null
        if ($ver -match "^3\.(1[1-3])$") {
            $PythonCmd = $cmd
            break
        }
    } catch {}
}

if (-not $PythonCmd) {
    Write-Host "ERROR: Python 3.11, 3.12, or 3.13 is required." -ForegroundColor Red
    Write-Host "       Python 3.14+ is NOT supported (missing package wheels)." -ForegroundColor Red
    Write-Host "       Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "       Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    exit 1
}

$PythonVersion = & $PythonCmd --version
Write-Host "Using Python: $PythonCmd ($PythonVersion)"
Write-Host ""

# ── 2. Check Node.js ─────────────────────────────────────────────────────────
try {
    $NodeVersion = & node --version 2>$null
    Write-Host "Using Node.js: $NodeVersion"
} catch {
    Write-Host "ERROR: Node.js is required." -ForegroundColor Red
    Write-Host "       Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# ── 3. Backend setup ─────────────────────────────────────────────────────────
Write-Host "Setting up backend..."
Set-Location $BackendDir

$VenvDir = Join-Path $BackendDir "venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvActivate = Join-Path $VenvDir "Scripts\Activate.ps1"

$NeedNewVenv = $false
if (-not (Test-Path $VenvDir)) {
    $NeedNewVenv = $true
} elseif (Test-Path $VenvPython) {
    try {
        $VenvMinor = & $VenvPython -c "import sys; print(sys.version_info.minor)" 2>$null
        if ([int]$VenvMinor -gt 13 -or [int]$VenvMinor -lt 11) {
            Write-Host "Existing venv uses unsupported Python. Recreating..."
            Remove-Item -Recurse -Force $VenvDir
            $NeedNewVenv = $true
        }
    } catch {
        $NeedNewVenv = $true
    }
}

if ($NeedNewVenv) {
    Write-Host "Creating virtual environment..."
    & $PythonCmd -m venv venv
}

# Activate venv
& $VenvActivate

Write-Host "Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt

# ── 4. Environment file ──────────────────────────────────────────────────────
$EnvFile = Join-Path $BackendDir ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Host ""
    Write-Host "Creating .env file with defaults..."
    @"
SECRET_KEY=change-me-to-a-random-secret
SQLALCHEMY_DATABASE_URI=sqlite:///kobrastocks.db
JWT_SECRET_KEY=change-me-to-a-random-jwt-secret
OPENAI_API_KEY=
NEWS_API_KEY=
"@ | Out-File -FilePath $EnvFile -Encoding utf8
    Write-Host "  .env created with SQLite (no PostgreSQL required for dev)."
    Write-Host "  Edit Backend\.env to add your API keys and customize settings."
}

# ── 5. Initialize database ───────────────────────────────────────────────────
Write-Host ""
Write-Host "Initializing database..."
try {
    flask db upgrade 2>$null
} catch {
    Write-Host "  Running initial migration..."
    try { flask db init 2>$null } catch {}
    try { flask db migrate -m "initial" 2>$null } catch {}
    try { flask db upgrade 2>$null } catch {}
}

# ── 6. Frontend setup ────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Setting up frontend..."
Set-Location $ClientDir

Write-Host "Installing npm dependencies..."
npm install

# ── 7. Launch both servers ────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Starting KobraStocks" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Backend  -> http://127.0.0.1:5000"
Write-Host "  Frontend -> http://localhost:8080"
Write-Host ""
Write-Host "  Press Ctrl+C to stop both servers." -ForegroundColor Yellow
Write-Host ""

# Start backend as a background job
Set-Location $BackendDir
& $VenvActivate
$BackendJob = Start-Job -ScriptBlock {
    param($dir, $activate)
    Set-Location $dir
    & $activate
    flask run
} -ArgumentList $BackendDir, $VenvActivate

# Start frontend in foreground
Set-Location $ClientDir
try {
    npm run serve
} finally {
    Write-Host ""
    Write-Host "Shutting down backend..."
    Stop-Job $BackendJob -ErrorAction SilentlyContinue
    Remove-Job $BackendJob -ErrorAction SilentlyContinue
    Write-Host "Done."
}
