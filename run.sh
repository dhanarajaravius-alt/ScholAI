#!/bin/bash
# ScholAI — Startup Script

echo ""
echo "╔══════════════════════════════════════╗"
echo "║       ScholAI — AI College Advisor   ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "❌  Python 3 is required. Install from python.org"
  exit 1
fi

# Install dependencies if needed
if ! python3 -c "import fastapi" 2>/dev/null; then
  echo "📦  Installing dependencies..."
  pip3 install -r requirements.txt --quiet
fi

# Check API key
if grep -q "sk-ant-your-key-here" .env 2>/dev/null; then
  echo "⚠️   No API key set. Edit .env and add your ANTHROPIC_API_KEY."
  echo "     AI features will be disabled until you do."
  echo ""
fi

echo "🚀  Starting server at http://localhost:8000"
echo "    Press Ctrl+C to stop"
echo ""

python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
