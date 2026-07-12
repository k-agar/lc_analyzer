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
    print(f"Loaded GEMINI_API_KEY: {GEMINI_API_KEY}")
    if not topic_stats:
        return "No topics available to generate a study plan."
        
    weakest_topics = topic_stats[:5]
    strongest_topics = topic_stats[-3:]
    
    weakest_names = [topic.get("tagName") for topic in weakest_topics if topic.get("tagName")]
    strongest_names = [topic.get("tagName") for topic in strongest_topics if topic.get("tagName")]
    
    prompt = (
        "You are an expert technical interview coach.\n"
        f"Strongest topics: {', '.join(strongest_names)}\n"
        f"Weakest topics: {', '.join(weakest_names)}\n\n"
        "Please perform the following:\n"
        "1. Identify the top 3 strongest topics (last 3 in the list) and mention them.\n"
        "2. Identify the top 5 weakest topics (first 5 in the list) and focus on them.\n"
        "3. Generate a 7-day study plan with specific problem types to practice each day.\n"
        "4. Keep the response concise and structured with clear Day 1, Day 2... headings."
    )
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
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
            print("Error response:", e.response.text)
            return "Study plan temporarily unavailable, please try again later"
        result = response.json()
        
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return "Error parsing response from Gemini API."
