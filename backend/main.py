from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from leetcode import fetch_user_data
from analytics import get_summary
from recommender import generate_study_plan

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analyze/{username}")
async def analyze_user(username: str):
    data = await fetch_user_data(username)
    if not data.get("data", {}).get("matchedUser"):
        raise HTTPException(status_code=404, detail="User not found")
    summary = get_summary(data)
    study_plan_7 = await generate_study_plan(summary["topics"], plan_type="7_days")
    study_plan_30 = await generate_study_plan(summary["topics"], plan_type="1_month")
    summary["study_plan_7"] = study_plan_7
    summary["study_plan_30"] = study_plan_30
    summary["study_plan"] = study_plan_7
    return summary


