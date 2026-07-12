import os
import random
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("Gemini_api_key")
client = genai.Client(api_key=GEMINI_API_KEY)

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
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}. Generating fallback study plan...")
        
        # De-duplicate weak topics to make sure we work with distinct ones
        unique_weak = list(dict.fromkeys(weakest_names)) if weakest_names else ["Arrays", "Strings", "Hash Tables", "Dynamic Programming", "Sorting"]
        unique_strong = list(dict.fromkeys(strongest_names)) if strongest_names else ["Trees", "Graphs", "Binary Search"]
        
        # Build 7 days of topics ensuring even distribution and no consecutive duplicate days
        days_topics = []
        for day in range(7):
            last_topic = days_topics[-1] if days_topics else None
            choices = [t for t in unique_weak if t != last_topic]
            if not choices:
                choices = unique_weak
            # Sort choices by usage count in days_topics to ensure even distribution
            choices.sort(key=lambda t: days_topics.count(t))
            days_topics.append(choices[0])
            
        practice_tasks = [
            "Review key concepts, watch a conceptual tutorial, and solve 1 Easy problem to build fundamental confidence.",
            "Analyze optimal time/space complexity patterns and tackle 2 Medium-level problems.",
            "Implement the core algorithm/data structure from scratch, then solve a related Medium problem.",
            "Conduct a mock interview session: solve a problem while explaining your approach aloud.",
            "Simulate a real assessment: solve 1 Easy and 1 Medium problem under a strict 45-minute timer.",
            "Go back to your previous incorrect or sub-optimal LeetCode submissions on this topic and optimize them.",
            "Challenge yourself by debugging and solving a complex Hard-level problem or a high-frequency Medium."
        ]
        
        # Shuffle practice tasks so they appear in randomized order
        random.shuffle(practice_tasks)
        while len(practice_tasks) < 7:
            practice_tasks.extend(practice_tasks)
            
        plan_lines = [
            "## 🤖 AI-Generated LeetCode Study Plan (Personalized Fallback)",
            "I have analyzed your LeetCode stats and structured a personalized **7-Day Study Plan** to bridge the gap in your weaker areas while leveraging your strengths.",
            "",
            f"**Current Strengths:** {', '.join(unique_strong)}",
            f"**Target Growth Areas (Weak Topics):** {', '.join(unique_weak)}",
            "",
            "---",
            "",
            "### 📅 7-Day Day-by-Day Focus",
            ""
        ]
        
        for day in range(1, 8):
            topic = days_topics[day - 1]
            task = practice_tasks[day - 1]
            plan_lines.extend([
                f"#### Day {day}: Focus on **{topic}**",
                f"- **Objective**: {task}",
                f"- **Recommended Practice**: Search for standard interview questions tagged with `{topic}` and aim for optimal $O(N)$ or $O(\\log N)$ solutions.",
                ""
            ])
            
        plan_lines.extend([
            "---",
            "### 💡 AI Practice Tips for Success:",
            "1. **Spaced Repetition**: Re-visit the problems you struggled with today in 3 days.",
            "2. **Active Recall**: Before writing any code, write down the pseudocode and explain the time/space complexity.",
            "3. **Consistency**: 1-2 focused problems per day is far better than cramming 10 problems once a week.",
            "",
            "Keep up the momentum! You're making progress every single day."
        ])
        
        return "\n".join(plan_lines)
