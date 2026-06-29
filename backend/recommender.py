import os
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

async def generate_study_plan(topic_stats: list) -> str:
    """
    Takes the sorted weak topics list from analytics.py,
    picks the top 5 weakest topics, and generates a 7-day personalized
    LeetCode study plan using the OpenAI API.
    """
    # Pick the top 5 weakest topics (which are the first 5 in the sorted list)
    weakest_topics = topic_stats[:5]
    topic_names = [topic.get("tagName") for topic in weakest_topics if topic.get("tagName")]
    
    if not topic_names:
        return "No topics available to generate a study plan."
    
    prompt = (
        f"Generate a 7-day personalized LeetCode study plan focused on these topics: {', '.join(topic_names)}.\n"
        "Please provide a daily breakdown outlining what to study and the type of problems to practice."
    )
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant and coding interview coach."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENAI_URL,
            headers=headers,
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        result = response.json()
        
    return result["choices"][0]["message"]["content"]
