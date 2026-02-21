#!/usr/bin/env bash
#
# KobraStocks setup & launch script for macOS / Linux
# Usage: ./setup.sh
#
set -e

PYTHON_VERSION="3.12"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/Backend"
CLIENT_DIR="$ROOT_DIR/client"

echo "============================================"
echo "  KobraStocks Setup & Launch"
echo "============================================"
echo ""

# ── 1. Check / install Python ────────────────────────────────────────────────
find_python() {
    for cmd in "python${PYTHON_VERSION}" "python3.12" "python3.13" "python3.11" "python3"; do
        if command -v "$cmd" &>/dev/null; then
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
            major=$("$cmd" -c "import sys; print(sys.version_info.major)")
            minor=$("$cmd" -c "import sys; print(sys.version_info.minor)")
            if [ "$major" = "3" ] && [ "$minor" -ge 11 ] && [ "$minor" -le 13 ]; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON_CMD=$(find_python) || true

if [ -z "$PYTHON_CMD" ]; then
    echo "Python 3.11-3.13 not found."
    if command -v brew &>/dev/null; then
        echo "Installing Python $PYTHON_VERSION via Homebrew..."
        brew install "python@${PYTHON_VERSION}"
        PYTHON_CMD=$(find_python)
    else
        echo "ERROR: Please install Python 3.11, 3.12, or 3.13 from https://www.python.org/downloads/"
        echo "       Python 3.14+ is NOT supported (missing package wheels)."
        exit 1
    fi
fi

echo "Using Python: $PYTHON_CMD ($($PYTHON_CMD --version))"
echo ""

# ── 2. Check Node.js ─────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
    echo "Node.js not found."
    if command -v brew &>/dev/null; then
        echo "Installing Node.js via Homebrew..."
        brew install node
    else
        echo "ERROR: Please install Node.js 18+ from https://nodejs.org/"
        exit 1
    fi
fi

echo "Using Node.js: $(node --version)"
echo ""

# ── 3. Backend setup ─────────────────────────────────────────────────────────
echo "Setting up backend..."
cd "$BACKEND_DIR"

if [ ! -d "venv" ] || [ ! -f "venv/pyvenv.cfg" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
else
    # Check if existing venv uses a supported Python version
    VENV_PYTHON="$BACKEND_DIR/venv/bin/python"
    if [ -f "$VENV_PYTHON" ]; then
        VENV_MINOR=$("$VENV_PYTHON" -c "import sys; print(sys.version_info.minor)" 2>/dev/null || echo "0")
        if [ "$VENV_MINOR" -gt 13 ] || [ "$VENV_MINOR" -lt 11 ]; then
            echo "Existing venv uses unsupported Python version. Recreating..."
            rm -rf venv
            $PYTHON_CMD -m venv venv
        fi
    fi
fi

source venv/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt

# ── 4. Environment file ──────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file with defaults..."
    cat > .env <<'ENVEOF'
SECRET_KEY=change-me-to-a-random-secret
SQLALCHEMY_DATABASE_URI=sqlite:///kobrastocks.db
JWT_SECRET_KEY=change-me-to-a-random-jwt-secret
OPENAI_API_KEY=
NEWS_API_KEY=
ENVEOF
    echo "  .env created with SQLite (no PostgreSQL required for dev)."
    echo "  Edit Backend/.env to add your API keys and customize settings."
fi

# ── 5. Initialize database ───────────────────────────────────────────────────
echo ""
echo "Initializing database..."
flask db upgrade 2>/dev/null || {
    echo "  Running initial migration..."
    flask db init 2>/dev/null || true
    flask db migrate -m "initial" 2>/dev/null || true
    flask db upgrade 2>/dev/null || true
}

# ── 6. Frontend setup ────────────────────────────────────────────────────────
echo ""
echo "Setting up frontend..."
cd "$CLIENT_DIR"

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
else
    echo "node_modules exists. Running npm install to sync..."
    npm install
fi

# ── 7. Launch both servers ────────────────────────────────────────────────────
echo ""
echo "============================================"
echo "  Starting KobraStocks"
echo "============================================"
echo ""
echo "  Backend  → http://127.0.0.1:5000"
echo "  Frontend → http://localhost:8080"
echo ""
echo "  Press Ctrl+C to stop both servers."
echo ""

# Start backend in background
cd "$BACKEND_DIR"
source venv/bin/activate
flask run &
BACKEND_PID=$!

# Start frontend in foreground
cd "$CLIENT_DIR"
npm run serve &
FRONTEND_PID=$!

# Trap Ctrl+C to kill both
cleanup() {
    echo ""
    echo "Shutting down..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID 2>/dev/null || true
    wait $FRONTEND_PID 2>/dev/null || true
    echo "Done."
}
trap cleanup INT TERM

# Wait for both
wait
