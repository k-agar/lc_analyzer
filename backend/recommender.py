import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("Gemini_api_key")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

async def generate_study_plan(topic_stats: list) -> str:
    """
    Takes the sorted weak topics list from analytics.py,
    picks the top 5 weakest topics, and generates a 7-day personalized
    LeetCode study plan using the Gemini API.
    """
    # Pick the top 5 weakest topics (which are the first 5 in the sorted list)
    weakest_topics = topic_stats[:5]
    topic_names = [topic.get("tagName") for topic in weakest_topics if topic.get("tagName")]
    
    if not topic_names:
        return "No topics available to generate a study plan."
    
    prompt = (
        "You are an expert technical interview coach.\n"
        f"Generate a 7-day personalized LeetCode study plan focused on these topics: {', '.join(topic_names)}.\n"
        "Please provide a daily breakdown outlining what to study and the type of problems to practice."
    )
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload,
            timeout=30.0
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return "Study plan temporarily unavailable, please try again in a moment"
            raise e
        result = response.json()
        
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "Error parsing response from Gemini API."
