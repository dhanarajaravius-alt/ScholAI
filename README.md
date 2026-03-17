<div align="center">

# 🎓 ScholAI — AI-Powered College Advisor

**Making expert college guidance accessible to every student.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Claude AI](https://img.shields.io/badge/Claude-Anthropic-C9A84C?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com)

> A full-stack AI application that helps students find, compare, and get personalized recommendations for U.S. college programs — powered by Claude AI and real college data.

---

</div>

## 📋 Project Proposal

### Problem Statement

Every year, over **2 million high school students** in the United States apply to colleges — many of them overwhelmed, underprepared, and underserved by the tools available to them.

Students from well-resourced families hire private college counselors at **$200–$500 per hour**. Everyone else relies on:

- 📚 Overworked school counselors managing hundreds of students
- 📊 Generic ranking websites that ignore personal goals
- 💬 Informal advice from family and social networks

| Problem | Impact |
|---|---|
| Information overload | 4,000+ U.S. colleges with no easy way to compare by major or profile |
| One-size-fits-all rankings | US News rankings ignore tuition budget, career goals, or admission fit |
| No personalized guidance | Students can't easily ask nuanced, profile-specific questions |
| Access gap | Private counseling unavailable to most students who need it |

---

### Why This Project Matters

**🏫 Equity in Education**
> Students in under-resourced schools deserve the same quality of college guidance as those who can afford private counselors. ScholAI democratizes access — free, 24/7, personalized.

**🎯 Better Outcomes Through Personalization**
> ScholAI lets students rank colleges based on their own priorities — program quality, cost-to-earnings ratio, graduation rate, or admission fit based on their GPA and SAT.

**🤖 Practical AI Application**
> ScholAI demonstrates how large language models can solve a real-world problem with measurable social impact.

---

### 🛠 Tools & Frameworks

| Component | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3 + FastAPI | REST API, routing, request handling |
| **AI Engine** | Anthropic Claude API | Natural language Q&A, college matching |
| **Frontend** | HTML / CSS / JavaScript | Single-page app served by FastAPI |
| **Data** | Built-in + College Scorecard | 20 U.S. colleges with real admissions data |
| **Server** | Uvicorn (ASGI) | High-performance async Python server |
| **Deployment** | Render.com | Cloud hosting with secure environment variables |
| **Version Control** | Git + GitHub | Source control and deployment pipeline |
| **Secrets** | python-dotenv | Secure API key management via `.env` |

---

### 🖥 Expected Output & User Interaction

The app has **4 fully functional modules:**

#### 1. 🔍 Major Explorer
- Browse 8 majors: Computer Engineering, CS, EE, Data Science, Biomedical Eng., Mechanical Eng., Finance, Psychology
- View core subjects, skills gained, career paths, and median salaries
- **"Ask Claude ✦"** generates an AI deep dive on any major

#### 2. 🏫 College Finder
- 20 U.S. colleges with real data: tuition, admission rate, SAT median, graduation rate, earnings
- Live filters by state, tuition, ABET accreditation, tier, and campus size
- Click any college → AI Advisor opens with pre-loaded context

#### 3. 🏆 Ranking Engine
- Drag 5 weighted sliders: Program Quality, Employment Outcome, Graduation Rate, Cost/Value, Admission Fit
- Colleges re-rank in real time using a composite scoring algorithm
- Personalized by your GPA and SAT score

#### 4. 🤖 AI Advisor (Chat)
- Full conversational chat powered by **Claude claude-sonnet-4-6**
- Maintains conversation history for multi-turn dialogue
- Sidebar shows your profile and saved schools

**Example questions:**
```
"Build me a college list. GPA 3.7, SAT 1380, Computer Engineering, budget $40k/yr, Texas."
"Why is Georgia Tech a better fit for me than MIT?"
"What salary can I expect after graduating from UCSD's CE program?"
"Is ABET accreditation required for government engineering jobs?"
```

---

## 🚀 Getting Started
```bash
# 1. Clone the repo
git clone https://github.com/dhanarajaravius-alt/ScholAI.git
cd ScholAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# 4. Run the app
python -m uvicorn main:app --reload

# 5. Open in browser → http://localhost:8000
```

---

## 🔐 Security

| Location | How key is stored |
|---|---|
| Local dev | `.env` file (excluded by `.gitignore`) |
| Production | Render's encrypted environment variables |
| Browser | Never — all AI calls go server-side only |

---

<div align="center">

**ScholAI — Making expert college guidance accessible to every student.**

Made by [Dhana](https://github.com/dhanarajaravius-alt)

</div>