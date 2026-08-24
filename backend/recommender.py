import os
import random
import httpx
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

async def query_flan_t5(prompt: str) -> str:
    """
    Queries google/flan-t5-base via Hugging Face Inference API.
    """
    if not HF_API_KEY:
        print("HF_API_KEY not found in environment.")
        return ""
    
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5,
        }
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                if isinstance(res_data, list) and len(res_data) > 0:
                    return res_data[0].get("generated_text", "").strip()
                elif isinstance(res_data, dict):
                    return res_data.get("generated_text", "").strip()
            print(f"HF API returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Failed to query Flan-T5 model: {e}")
    return ""

async def generate_study_plan(topic_stats: list, plan_type: str = "7_days") -> str:
    """
    Takes the sorted weak topics list from analytics.py,
    picks the top 5 weakest topics, and generates a personalized
    LeetCode study plan (either 7-day or 1-month/30-day) using Flan-T5 recommendations.
    """
    if not topic_stats:
        return "No topics available to generate a study plan."
        
    weakest_topics = topic_stats[:5]
    strongest_topics = topic_stats[-3:]
    
    weakest_names = [topic.get("tagName") for topic in weakest_topics if topic.get("tagName")]
    strongest_names = [topic.get("tagName") for topic in strongest_topics if topic.get("tagName")]
    
    # Fallback to defaults if list is too small
    unique_weak = list(dict.fromkeys(weakest_names)) if weakest_names else ["Arrays", "Strings", "Hash Tables", "Dynamic Programming", "Sorting"]
    unique_strong = list(dict.fromkeys(strongest_names)) if strongest_names else ["Trees", "Graphs", "Binary Search"]
    
    # Pad out topics if we have fewer than 5
    dsa_fallbacks = ["Arrays", "Strings", "Hash Tables", "Dynamic Programming", "Sorting", "Trees", "Graphs"]
    while len(unique_weak) < 5:
        for fb in dsa_fallbacks:
            if fb not in unique_weak:
                unique_weak.append(fb)
                break
        else:
            unique_weak.append("Algorithms")
            
    # Call HF model
    if plan_type == "7_days":
        hf_prompt = f"Create a short 7-day LeetCode study focus sequence for weak areas: {', '.join(unique_weak)}."
    else:
        hf_prompt = f"Create a short 4-week LeetCode study focus summary for weak areas: {', '.join(unique_weak)}."
        
    hf_response = await query_flan_t5(hf_prompt)
    
    # We will build a beautiful structured response
    plan_lines = []
    
    if plan_type == "7_days":
        plan_lines.extend([
            "## 🤖 AI-Generated LeetCode 7-Day Sprint Plan",
            "This personalized 7-day study plan targets your weaker topics while leveraging your strengths.",
            ""
        ])
        if hf_response:
            plan_lines.extend([
                "### 💡 AI Model Focus (google/flan-t5-base)",
                f"> {hf_response}",
                ""
            ])
        plan_lines.extend([
            f"**Current Strengths:** {', '.join(unique_strong)}",
            f"**Target Growth Areas (Weak Topics):** {', '.join(unique_weak)}",
            "",
            "---",
            "",
            "### 📅 7-Day Day-by-Day Focus",
            ""
        ])
        
        # Build 7 days
        days_topics = []
        for day in range(7):
            last_topic = days_topics[-1] if days_topics else None
            choices = [t for t in unique_weak if t != last_topic]
            if not choices:
                choices = unique_weak
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
        
        for day in range(1, 8):
            topic = days_topics[day - 1]
            task = practice_tasks[day - 1]
            plan_lines.extend([
                f"#### Day {day}: Focus on **{topic}**",
                f"- **Objective**: {task}",
                f"- **Recommended Practice**: Search for standard interview questions tagged with `{topic}` and aim for optimal $O(N)$ or $O(\\log N)$ solutions.",
                ""
            ])
            
    else: # 1_month
        plan_lines.extend([
            "## 🤖 AI-Generated LeetCode 1-Month Deep Dive Plan",
            "This structured 4-week curriculum is designed to rebuild your confidence in weak areas and prep you for interviews.",
            ""
        ])
        if hf_response:
            plan_lines.extend([
                "### 💡 AI Model Focus (google/flan-t5-base)",
                f"> {hf_response}",
                ""
            ])
        plan_lines.extend([
            f"**Current Strengths:** {', '.join(unique_strong)}",
            f"**Target Growth Areas (Weak Topics):** {', '.join(unique_weak)}",
            "",
            "---",
            ""
        ])
        
        # Build 1 month (4 weeks)
        plan_lines.extend([
            "### 📅 Week 1: Foundation Building (Focus: **" + unique_weak[0] + "** & **" + unique_weak[1] + "**)",
            f"- **Day 1**: Learn basic patterns for **{unique_weak[0]}** and solve 2 Easy problems.",
            f"- **Day 2**: Tackle 2 Medium-level problems on **{unique_weak[0]}** using optimal space/time complexity.",
            f"- **Day 3**: Switch to **{unique_weak[1]}**, review basic properties and solve 2 Easy problems.",
            f"- **Day 4**: Implement the core data structure/algorithm for **{unique_weak[1]}** from scratch and solve 1 Medium problem.",
            f"- **Day 5**: Solve 2 Medium problems combining **{unique_weak[0]}** and **{unique_weak[1]}**.",
            f"- **Day 6**: Mock interview simulation: choose 1 Medium problem on **{unique_weak[0]}** and solve it under 35 minutes.",
            "- **Day 7**: Weekly reflection: document your mistakes in an error log.",
            "",
            "### 📅 Week 2: Intermediate Expansion (Focus: **" + unique_weak[2] + "** & **" + unique_weak[3] + "**)",
            f"- **Day 8**: Dive into **{unique_weak[2]}** concepts and solve 2 Easy problems.",
            f"- **Day 9**: Solve 2 Medium-level problems on **{unique_weak[2]}** focusing on space-time efficiency.",
            f"- **Day 10**: Introduce **{unique_weak[3]}**, understand edge cases and solve 2 Easy problems.",
            f"- **Day 11**: Solve 2 Medium-level problems on **{unique_weak[3]}** and identify common pitfalls.",
            f"- **Day 12**: Solve 2 mixed Medium problems involving both **{unique_weak[2]}** and **{unique_weak[3]}**.",
            f"- **Day 13**: Time-based assessment: solve 1 Easy and 1 Medium problem in 45 minutes.",
            "- **Day 14**: Review week 2 error logs and re-attempt failed problems.",
            "",
            "### 📅 Week 3: Core Mastery & Strengths (Focus: **" + unique_weak[4] + "** & Strengths)",
            f"- **Day 15**: Dive deep into **{unique_weak[4]}**, review concepts and solve 2 Easy problems.",
            f"- **Day 16**: Solve 2 Medium problems on **{unique_weak[4]}** and check editorial/top solutions.",
            f"- **Day 17**: Challenge yourself with 1 Hard problem on **{unique_weak[4]}** or a highly-rated Medium.",
            f"- **Day 18**: Incorporate strength area **{unique_strong[0]}** with mixed practice (1 Medium problem).",
            f"- **Day 19**: Solve a multi-topic problem containing elements of **{unique_weak[0]}** and **{unique_strong[-1]}**.",
            f"- **Day 20**: Mock Interview: solve 2 random Medium problems with a strict 60-minute timer.",
            "- **Day 21**: Weekly review and revision of conceptual notes.",
            "",
            "### 📅 Week 4: Peak Performance & Interview Simulation",
            "- **Day 22**: Spaced Repetition: Re-solve 3 problems from your Week 1 & 2 error logs.",
            "- **Day 23**: Speed Drill: Solve 3 Easy problems on any weakest topic within 30 minutes.",
            "- **Day 24**: Medium Endurance: Solve 3 Medium problems back-to-back in 75 minutes.",
            "- **Day 25**: Complexity Optimization: Go through your past solutions and reduce runtime/space complexity.",
            "- **Day 26**: Crossover Patterns: Study problems that use multiple DSA concepts simultaneously.",
            "- **Day 27**: Full Assessment: Simulate a LeetCode Online Assessment (2 Medium, 1 Hard) in 90 minutes.",
            "- **Day 28**: Final interview checklist, behavioral review, and mental prep.",
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
