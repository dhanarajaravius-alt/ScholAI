# ScholAI — AI-Powered College Advisor

A full Python/FastAPI web app with Claude AI integration.

## Quick Start

### 1. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Add your API key
Edit `.env` and replace the placeholder:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```
Get your key at: https://console.anthropic.com

### 3. Run the app
```bash
# Option A — simple
python3 -m uvicorn main:app --reload

# Option B — use the startup script
chmod +x run.sh && ./run.sh
```

### 4. Open in browser
```
http://localhost:8000
```

---

## Project Structure
```
scholai/
├── main.py           ← FastAPI backend (all API routes + data)
├── templates/
│   └── index.html    ← Full frontend (HTML/CSS/JS)
├── requirements.txt  ← Python dependencies
├── .env              ← Your API key (never commit this)
├── run.sh            ← Startup script
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main app UI |
| GET | `/api/status` | AI readiness check |
| GET | `/api/majors` | List all majors |
| GET | `/api/majors/{key}` | Major detail |
| POST | `/api/colleges/filter` | Filter colleges |
| POST | `/api/rank` | Rank colleges by weights |
| POST | `/api/chat` | AI advisor chat |
| POST | `/api/major-ai` | AI major deep dive |

## Features
- 8 majors with career paths and salaries
- 20 U.S. colleges with real data
- Live filters (state, tuition, admission rate, ABET, tier, size)
- Custom ranking engine with draggable weights
- Full AI chat advisor powered by Claude
- AI deep dive on any major
