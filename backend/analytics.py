import json

def get_difficulty_stats(data: dict) -> dict:
    """
    Extracts Easy, Medium, Hard solved counts and returns them as a dict.
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}
    
    submissions = matched_user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
    stats = {"All": 0, "Easy": 0, "Medium": 0, "Hard": 0}
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

def get_badges_stats(data: dict) -> list:
    """
    Extracts badges the user got.
    Each badge has id, name, displayName, icon, hoverText.
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return []
    
    badges = matched_user.get("badges", [])
    processed_badges = []
    for badge in badges:
        icon_url = badge.get("icon", "")
        if icon_url and icon_url.startswith("/"):
            icon_url = f"https://leetcode.com{icon_url}"
        
        processed_badges.append({
            "id": badge.get("id"),
            "name": badge.get("name"),
            "displayName": badge.get("displayName"),
            "icon": icon_url,
            "hoverText": badge.get("hoverText")
        })
    return processed_badges

def get_contest_ranking(data: dict) -> dict:
    """
    Extracts user contest ranking.
    """
    contest_data = data.get("data", {}).get("userContestRanking")
    if not contest_data:
        return None
    
    return {
        "attendedContestsCount": contest_data.get("attendedContestsCount"),
        "rating": round(contest_data.get("rating", 0)),
        "globalRanking": contest_data.get("globalRanking"),
        "totalParticipants": contest_data.get("totalParticipants"),
        "topPercentage": contest_data.get("topPercentage"),
        "badge": contest_data.get("badge", {}).get("name") if contest_data.get("badge") else None
    }

def get_summary(data: dict) -> dict:
    """
    Returns a combined dict with difficulty stats, topic stats, submission calendar, badges, and contest ranking.
    """
    return {
        "difficulty": get_difficulty_stats(data),
        "topics": get_topic_stats(data),
        "calendar": get_submission_calendar(data),
        "badges": get_badges_stats(data),
        "contest": get_contest_ranking(data)
    }
