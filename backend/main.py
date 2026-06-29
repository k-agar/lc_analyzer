from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from leetcode import fetch_user_data
from analytics import get_summary

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
    return get_summary(data)

