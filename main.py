"""
ScholAI — AI-Powered College Advisor
FastAPI backend with Anthropic Claude integration
"""

import os
import json
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import httpx

load_dotenv()

app = FastAPI(title="ScholAI", description="AI-Powered College Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Anthropic client ──────────────────────────────
def get_client():
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key or key == "sk-ant-your-key-here":
        raise HTTPException(status_code=400, detail="ANTHROPIC_API_KEY not set in .env file")
    return anthropic.Anthropic(api_key=key)

# ── Data ─────────────────────────────────────────
MAJORS = {
    "ce": {
        "title": "Computer Engineering",
        "degree": "B.S. · 4 years",
        "accred": "ABET Accredited",
        "dept": "College of Engineering",
        "desc": "Computer Engineering bridges hardware and software — designing the processors, embedded systems, and digital architectures that power every device. You will build real systems from silicon to operating system.",
        "demand": ["High Demand", "$112k–$165k avg", "Top 5 STEM field"],
        "core": ["Digital Logic Design", "Computer Architecture", "Embedded Systems", "Operating Systems", "Signals & Systems", "VLSI Design", "Computer Networks", "Compilers"],
        "skills": ["C / C++", "FPGA & RTL (Verilog)", "Python", "PCB Design", "Linux Kernel", "Assembly", "MATLAB"],
        "careers": [["Hardware Engineer", "$118k"], ["FPGA Engineer", "$135k"], ["Embedded Systems", "$112k"], ["Firmware Engineer", "$122k"], ["Chip Designer", "$148k"], ["SoC Architect", "$165k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$95k"}, {"l": "Job Placement", "v": "94%"}, {"l": "Median Mid-Career", "v": "$128k"}, {"l": "Programs in USA", "v": "380+"}]
    },
    "cs": {
        "title": "Computer Science",
        "degree": "B.S. · 4 years",
        "accred": "ABET / CSAB Accredited",
        "dept": "College of Computing",
        "desc": "Computer Science is the study of computation, algorithms, and software systems — from building web applications to training large language models. The most versatile technical degree.",
        "demand": ["Very High Demand", "$115k–$200k avg", "#1 STEM major by hiring"],
        "core": ["Data Structures & Algorithms", "Theory of Computation", "Operating Systems", "Computer Networks", "Database Systems", "Machine Learning", "Programming Languages", "Software Engineering"],
        "skills": ["Python", "Java / Kotlin", "React / TypeScript", "SQL & NoSQL", "Git & CI/CD", "Docker / Kubernetes", "Cloud (AWS/GCP)"],
        "careers": [["Software Engineer", "$145k"], ["ML / AI Engineer", "$158k"], ["Backend Engineer", "$135k"], ["Staff Engineer", "$210k"], ["Data Engineer", "$130k"], ["Product Eng.", "$148k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$108k"}, {"l": "Job Placement", "v": "97%"}, {"l": "Median Mid-Career", "v": "$145k"}, {"l": "Programs in USA", "v": "2,400+"}]
    },
    "ee": {
        "title": "Electrical Engineering",
        "degree": "B.S. · 4 years",
        "accred": "ABET Accredited",
        "dept": "College of Engineering",
        "desc": "Electrical Engineering underpins modern civilization — from power grids and electric vehicles to 5G networks and radar systems. EE graduates are highly sought across energy, defense, and semiconductors.",
        "demand": ["Stable Demand", "$98k–$145k avg", "Critical infrastructure role"],
        "core": ["Circuit Analysis", "Electromagnetics", "Power Systems", "Control Theory", "Signal Processing", "RF Design", "Power Electronics", "Digital Communications"],
        "skills": ["MATLAB / Simulink", "Cadence / Altium", "SPICE", "Python", "PCB Design", "LabVIEW", "FPGA basics"],
        "careers": [["Power Engineer", "$102k"], ["RF Engineer", "$122k"], ["Controls Engineer", "$115k"], ["Signal Processing", "$120k"], ["Power Electronics", "$118k"], ["Telecom Engineer", "$108k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$88k"}, {"l": "Job Placement", "v": "91%"}, {"l": "Median Mid-Career", "v": "$115k"}, {"l": "Programs in USA", "v": "340+"}]
    },
    "ds": {
        "title": "Data Science",
        "degree": "B.S. · 4 years",
        "accred": "Regional Accreditation",
        "dept": "College of Computing / Statistics",
        "desc": "Data Science extracts insight and builds predictive systems from large datasets. Combining statistics, machine learning, and domain expertise — data scientists are critical to every major organization.",
        "demand": ["Explosive Demand", "$110k–$175k avg", "Fastest-growing field"],
        "core": ["Statistics & Probability", "Machine Learning", "Data Visualization", "Big Data (Spark)", "Deep Learning", "SQL & Databases", "Causal Inference", "NLP"],
        "skills": ["Python (pandas, sklearn)", "R", "Apache Spark", "Tableau / Power BI", "TensorFlow / PyTorch", "SQL", "Experiment Design"],
        "careers": [["Data Scientist", "$128k"], ["ML Engineer", "$148k"], ["Data Analyst", "$88k"], ["AI Researcher", "$165k"], ["Quant Analyst", "$145k"], ["Analytics Mgr.", "$130k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$98k"}, {"l": "Job Placement", "v": "95%"}, {"l": "Median Mid-Career", "v": "$130k"}, {"l": "Programs in USA", "v": "900+"}]
    },
    "bio": {
        "title": "Biomedical Engineering",
        "degree": "B.S. · 4 years",
        "accred": "ABET Accredited",
        "dept": "College of Engineering / Medicine",
        "desc": "Biomedical Engineering applies engineering principles to medicine and biology — developing medical devices, prosthetics, imaging systems, and regenerative therapies.",
        "demand": ["Growing Demand", "$78k–$120k avg", "Healthcare sector boom"],
        "core": ["Biomechanics", "Bioelectronics", "Medical Imaging", "Physiology", "Biomaterials", "Drug Delivery", "Regulatory Affairs", "Bioinformatics"],
        "skills": ["MATLAB", "SolidWorks / CAD", "Python", "LabVIEW", "FEA (ANSYS)", "Signal Processing", "FDA Regulatory"],
        "careers": [["Medical Device Eng.", "$98k"], ["BME Researcher", "$92k"], ["Clinical Eng.", "$88k"], ["R&D Engineer", "$105k"], ["Regulatory Affairs", "$95k"], ["Tissue Engineer", "$90k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$72k"}, {"l": "Job Placement", "v": "88%"}, {"l": "Median Mid-Career", "v": "$100k"}, {"l": "Programs in USA", "v": "250+"}]
    },
    "me": {
        "title": "Mechanical Engineering",
        "degree": "B.S. · 4 years",
        "accred": "ABET Accredited",
        "dept": "College of Engineering",
        "desc": "Mechanical Engineering covers the design, analysis, and manufacturing of physical systems — from jet engines to robotics. Foundational to aerospace, automotive, energy, and manufacturing.",
        "demand": ["Stable Demand", "$88k–$135k avg", "Evergreen discipline"],
        "core": ["Statics & Dynamics", "Thermodynamics", "Fluid Mechanics", "Materials Science", "Heat Transfer", "Machine Design", "Manufacturing", "Robotics & Control"],
        "skills": ["SolidWorks / CATIA", "ANSYS FEA", "AutoCAD", "MATLAB", "Python", "GD&T", "CNC / Machining"],
        "careers": [["Mechanical Engineer", "$92k"], ["Aerospace Eng.", "$112k"], ["Robotics Eng.", "$118k"], ["HVAC Eng.", "$82k"], ["Automotive Eng.", "$95k"], ["Nuclear Eng.", "$105k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$80k"}, {"l": "Job Placement", "v": "90%"}, {"l": "Median Mid-Career", "v": "$108k"}, {"l": "Programs in USA", "v": "600+"}]
    },
    "fin": {
        "title": "Finance",
        "degree": "B.S. · 4 years",
        "accred": "AACSB Accredited",
        "dept": "Business School",
        "desc": "Finance studies the management of money, investments, risk, and capital markets. Graduates work in investment banking, asset management, corporate treasury, fintech, and private equity.",
        "demand": ["High Demand", "$85k–$200k+ avg", "Strong in major metros"],
        "core": ["Corporate Finance", "Investments & Portfolio Theory", "Financial Modeling", "Derivatives & Risk", "Accounting", "Econometrics", "Fixed Income", "M&A and Valuation"],
        "skills": ["Excel / VBA", "Bloomberg Terminal", "Python / R", "SQL", "DCF Modeling", "Financial Statements", "CFA Prep"],
        "careers": [["Investment Banking", "$180k+ (all-in)"], ["Portfolio Manager", "$120k"], ["Financial Analyst", "$88k"], ["Quant Analyst", "$155k"], ["Private Equity", "$200k+"], ["CFO (senior)", "$250k+"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$78k"}, {"l": "Job Placement", "v": "92%"}, {"l": "Median Mid-Career", "v": "$120k"}, {"l": "Programs in USA", "v": "1,800+"}]
    },
    "psy": {
        "title": "Psychology",
        "degree": "B.S. or B.A. · 4 years",
        "accred": "APA Guidelines",
        "dept": "College of Liberal Arts / Sciences",
        "desc": "Psychology is the scientific study of mind and behavior. Strong demand exists in UX research, HR, mental health, and behavioral economics — though graduate school is often advised for clinical paths.",
        "demand": ["Moderate Demand", "$45k–$100k avg", "Grad school often advised"],
        "core": ["Intro to Psychology", "Research Methods & Stats", "Cognitive Psychology", "Developmental Psychology", "Abnormal Psychology", "Social Psychology", "Neuroscience", "Industrial-Org Psych"],
        "skills": ["SPSS / R Statistics", "Survey Design", "Qualitative Research", "Clinical Assessment", "MATLAB (neuro)", "Writing & Communication", "User Research (UX)"],
        "careers": [["UX Researcher", "$98k"], ["HR / People Ops", "$72k"], ["Clinical Psychologist", "$82k (PhD)"], ["School Counselor", "$60k"], ["Market Researcher", "$65k"], ["Behavioral Analyst", "$62k"]],
        "stats": [{"l": "Avg Starting Salary", "v": "$40k"}, {"l": "Job Placement", "v": "78%"}, {"l": "Median Mid-Career", "v": "$68k"}, {"l": "Programs in USA", "v": "3,000+"}]
    }
}

COLLEGES = [
    {"id": 1,  "name": "MIT",                  "city": "Cambridge",      "state": "MA", "tuition": 59000, "admit": 4,  "sat": 1545, "gpa": 4.15, "gradRate": 95, "earnings": 112000, "abet": True,  "size": "Medium", "score": 97, "tier": "reach"},
    {"id": 2,  "name": "Stanford University",  "city": "Palo Alto",      "state": "CA", "tuition": 62000, "admit": 4,  "sat": 1530, "gpa": 4.0,  "gradRate": 96, "earnings": 118000, "abet": True,  "size": "Medium", "score": 96, "tier": "reach"},
    {"id": 3,  "name": "Caltech",              "city": "Pasadena",       "state": "CA", "tuition": 60000, "admit": 6,  "sat": 1560, "gpa": 4.2,  "gradRate": 93, "earnings": 105000, "abet": True,  "size": "Small",  "score": 95, "tier": "reach"},
    {"id": 4,  "name": "Carnegie Mellon",      "city": "Pittsburgh",     "state": "PA", "tuition": 62000, "admit": 15, "sat": 1510, "gpa": 3.95, "gradRate": 91, "earnings": 108000, "abet": True,  "size": "Medium", "score": 93, "tier": "reach"},
    {"id": 5,  "name": "Georgia Tech",         "city": "Atlanta",        "state": "GA", "tuition": 33800, "admit": 21, "sat": 1455, "gpa": 3.9,  "gradRate": 87, "earnings": 92000,  "abet": True,  "size": "Large",  "score": 88, "tier": "reach"},
    {"id": 6,  "name": "UC Berkeley",          "city": "Berkeley",       "state": "CA", "tuition": 44000, "admit": 14, "sat": 1440, "gpa": 3.9,  "gradRate": 91, "earnings": 98000,  "abet": True,  "size": "Large",  "score": 87, "tier": "reach"},
    {"id": 7,  "name": "University of Michigan","city": "Ann Arbor",     "state": "MI", "tuition": 52000, "admit": 20, "sat": 1430, "gpa": 3.85, "gradRate": 92, "earnings": 90000,  "abet": True,  "size": "Large",  "score": 86, "tier": "reach"},
    {"id": 8,  "name": "Cornell University",   "city": "Ithaca",         "state": "NY", "tuition": 60000, "admit": 11, "sat": 1480, "gpa": 3.9,  "gradRate": 93, "earnings": 96000,  "abet": True,  "size": "Large",  "score": 85, "tier": "reach"},
    {"id": 9,  "name": "UIUC",                 "city": "Champaign",      "state": "IL", "tuition": 36000, "admit": 62, "sat": 1390, "gpa": 3.8,  "gradRate": 85, "earnings": 86000,  "abet": True,  "size": "XLarge", "score": 84, "tier": "match"},
    {"id": 10, "name": "Purdue University",    "city": "West Lafayette",  "state": "IN", "tuition": 28800, "admit": 62, "sat": 1330, "gpa": 3.7,  "gradRate": 83, "earnings": 78000,  "abet": True,  "size": "Large",  "score": 79, "tier": "match"},
    {"id": 11, "name": "UC San Diego",         "city": "La Jolla",       "state": "CA", "tuition": 45000, "admit": 30, "sat": 1385, "gpa": 3.8,  "gradRate": 87, "earnings": 82000,  "abet": True,  "size": "Large",  "score": 82, "tier": "match"},
    {"id": 12, "name": "UT Austin",            "city": "Austin",         "state": "TX", "tuition": 37000, "admit": 31, "sat": 1360, "gpa": 3.8,  "gradRate": 84, "earnings": 80000,  "abet": True,  "size": "XLarge", "score": 80, "tier": "match"},
    {"id": 13, "name": "Texas A&M",            "city": "College Station", "state": "TX", "tuition": 30000, "admit": 58, "sat": 1290, "gpa": 3.6,  "gradRate": 81, "earnings": 72000,  "abet": True,  "size": "XLarge", "score": 75, "tier": "match"},
    {"id": 14, "name": "Cal Poly SLO",         "city": "San Luis Obispo","state": "CA", "tuition": 26000, "admit": 28, "sat": 1350, "gpa": 3.8,  "gradRate": 82, "earnings": 74000,  "abet": True,  "size": "Medium", "score": 76, "tier": "match"},
    {"id": 15, "name": "NC State",             "city": "Raleigh",        "state": "NC", "tuition": 27000, "admit": 45, "sat": 1300, "gpa": 3.6,  "gradRate": 79, "earnings": 71000,  "abet": True,  "size": "Large",  "score": 73, "tier": "match"},
    {"id": 16, "name": "University of Washington","city": "Seattle",     "state": "WA", "tuition": 42000, "admit": 52, "sat": 1350, "gpa": 3.7,  "gradRate": 84, "earnings": 88000,  "abet": True,  "size": "Large",  "score": 78, "tier": "match"},
    {"id": 17, "name": "Ohio State",           "city": "Columbus",       "state": "OH", "tuition": 33000, "admit": 68, "sat": 1310, "gpa": 3.7,  "gradRate": 83, "earnings": 72000,  "abet": True,  "size": "XLarge", "score": 71, "tier": "safety"},
    {"id": 18, "name": "Arizona State",        "city": "Tempe",          "state": "AZ", "tuition": 32000, "admit": 88, "sat": 1200, "gpa": 3.4,  "gradRate": 64, "earnings": 62000,  "abet": True,  "size": "XLarge", "score": 60, "tier": "safety"},
    {"id": 19, "name": "University of Houston","city": "Houston",        "state": "TX", "tuition": 24000, "admit": 65, "sat": 1210, "gpa": 3.5,  "gradRate": 55, "earnings": 60000,  "abet": True,  "size": "Large",  "score": 58, "tier": "safety"},
    {"id": 20, "name": "Boston University",    "city": "Boston",         "state": "MA", "tuition": 58000, "admit": 57, "sat": 1390, "gpa": 3.7,  "gradRate": 86, "earnings": 76000,  "abet": True,  "size": "Large",  "score": 72, "tier": "match"},
]

# ── Request Models ────────────────────────────────
class ChatRequest(BaseModel):
    messages: list
    system: Optional[str] = None

class RankRequest(BaseModel):
    weights: dict
    gpa: float = 3.7
    sat: int = 1380

class MajorAIRequest(BaseModel):
    major_key: str

class CollegeFilterRequest(BaseModel):
    state: Optional[str] = None
    max_tuition: Optional[int] = None
    min_admit: Optional[int] = None
    abet_only: bool = False
    tier: Optional[str] = None
    size: Optional[str] = None

# ── Helper ────────────────────────────────────────
def normalise(val, mn, mx):
    if mx == mn:
        return 0
    return max(0.0, min(1.0, (val - mn) / (mx - mn)))

def score_college(college: dict, weights: dict, gpa: float, sat: int) -> float:
    total = sum(weights.values()) or 100
    w = [weights.get(k, 0) / total for k in ["Program Quality", "Employment Outcome", "Graduation Rate", "Cost / Value", "Admission Fit"]]
    pq = normalise(college["score"], 50, 100) * 100
    em = normalise(college["earnings"], 40000, 120000) * 100
    gr = college["gradRate"]
    cv = normalise(college["earnings"] / college["tuition"], 0.5, 5) * 100
    gpa_fit = max(0, 100 - abs(college["gpa"] - gpa) / 0.5 * 30)
    sat_fit = max(0, 100 - abs(college["sat"] - sat) / 200 * 30)
    af = (gpa_fit + sat_fit) / 2
    scores = [pq, em, gr, cv, af]
    return round(sum(s * wt for s, wt in zip(scores, w)))

# ── API Routes ────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.get("/api/majors")
async def get_majors():
    return {"majors": {k: {"title": v["title"], "dept": v["dept"]} for k, v in MAJORS.items()}}

@app.get("/api/majors/{major_key}")
async def get_major(major_key: str):
    if major_key not in MAJORS:
        raise HTTPException(status_code=404, detail="Major not found")
    return MAJORS[major_key]

@app.post("/api/colleges/filter")
async def filter_colleges(req: CollegeFilterRequest):
    results = COLLEGES
    if req.state:
        results = [c for c in results if c["state"] == req.state]
    if req.max_tuition:
        results = [c for c in results if c["tuition"] <= req.max_tuition]
    if req.min_admit:
        results = [c for c in results if c["admit"] >= req.min_admit]
    if req.abet_only:
        results = [c for c in results if c["abet"]]
    if req.tier:
        results = [c for c in results if c["tier"] == req.tier]
    if req.size:
        results = [c for c in results if c["size"] == req.size]
    return {"colleges": results, "total": len(results)}

@app.post("/api/rank")
async def rank_colleges(req: RankRequest):
    scored = []
    for c in COLLEGES:
        composite = score_college(c, req.weights, req.gpa, req.sat)
        scored.append({**c, "composite": composite})
    scored.sort(key=lambda x: x["composite"], reverse=True)
    return {"ranked": scored}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    client = get_client()
    system = req.system or """You are ScholAI, an expert college admissions and career advisor.
You help students find the best colleges for their major, profile, and goals.
You know U.S. college admissions, financial aid, rankings, ABET accreditation, and career outcomes.
Be specific, practical, and encouraging. Use markdown formatting with **bold** for key terms.
Keep responses focused and under 300 words unless asked for more."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system,
            messages=req.messages
        )
        return {"response": response.content[0].text}
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key. Check your ANTHROPIC_API_KEY in .env")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit hit. Please wait a moment and try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/major-ai")
async def major_ai(req: MajorAIRequest):
    if req.major_key not in MAJORS:
        raise HTTPException(status_code=404, detail="Major not found")
    client = get_client()
    m = MAJORS[req.major_key]
    prompt = f"""You are an expert academic and career advisor. Provide a deep dive analysis of the {m['title']} major in 3 paragraphs covering:
1. What makes this major unique and what studying it day-to-day is like
2. Emerging specializations and hot research areas in 2024-2025
3. What separates elite candidates in the job market, and honest pros and cons

Be specific, insightful, and practical. Max 250 words."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.content[0].text}
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid API key. Check your ANTHROPIC_API_KEY in .env")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status():
    key = os.getenv("ANTHROPIC_API_KEY", "")
    has_key = bool(key) and key != "sk-ant-your-key-here"
    return {"status": "ok", "ai_ready": has_key}
