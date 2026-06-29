import json

def get_difficulty_stats(data: dict) -> dict:
    """
    Extracts Easy, Medium, Hard solved counts and returns them as a dict.
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return {"Easy": 0, "Medium": 0, "Hard": 0}
    
    submissions = matched_user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
    stats = {"Easy": 0, "Medium": 0, "Hard": 0}
    for item in submissions:
        diff = item.get("difficulty")
        if diff in stats:
            stats[diff] = item.get("count", 0)
    return stats

def get_topic_stats(data: dict) -> list:
    """
    Extracts topic tag names and problems solved, returns a sorted list from weakest to strongest.
    Filters out topics with problems solved less than 3, and only keeps allowed DSA topics.
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return []
    
    tag_counts = matched_user.get("tagProblemCounts", {})
    all_topics = []
    
    allowed_topics = {
        "Array", "String", "Dynamic Programming", "Tree", "Graph", 
        "Binary Search", "Linked List", "Stack", "Queue", "Heap", 
        "Recursion", "Backtracking", "Sorting", "Hashing", "Math"
    }
    
    for category in ["advanced", "intermediate", "fundamental"]:
        topics = tag_counts.get(category) or []
        for topic in topics:
            tag_name = topic.get("tagName")
            solved = topic.get("problemsSolved", 0)
            
            # Map actual LeetCode tag names to the allowed list names
            display_name = tag_name
            if tag_name == "Hash Table":
                display_name = "Hashing"
            elif tag_name == "Heap (Priority Queue)":
                display_name = "Heap"
                
            if display_name in allowed_topics and solved >= 3:
                all_topics.append({
                    "tagName": display_name,
                    "problemsSolved": solved
                })
            
    # Sort from weakest to strongest (ascending by problemsSolved)
    all_topics.sort(key=lambda x: x["problemsSolved"])
    return all_topics

def get_submission_calendar(data: dict) -> dict:
    """
    Extracts submissionCalendar string and parses it into a dict of {timestamp: count}.
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return {}
    
    calendar_str = matched_user.get("userCalendar", {}).get("submissionCalendar", "{}")
    try:
        return json.loads(calendar_str)
    except Exception:
        return {}

def get_summary(data: dict) -> dict:
    """
    Returns a combined dict with difficulty stats, topic stats, and submission calendar.
    """
    return {
        "difficulty": get_difficulty_stats(data),
        "topics": get_topic_stats(data),
        "calendar": get_submission_calendar(data)
    }
