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
    """
    matched_user = data.get("data", {}).get("matchedUser")
    if not matched_user:
        return []
    
    tag_counts = matched_user.get("tagProblemCounts", {})
    all_topics = []
    
    for category in ["advanced", "intermediate", "fundamental"]:
        topics = tag_counts.get(category) or []
        for topic in topics:
            all_topics.append({
                "tagName": topic.get("tagName"),
                "problemsSolved": topic.get("problemsSolved", 0)
            })
            
    # Sort from weakest to strongest (ascending by problemsSolved)
    all_topics.sort(key=lambda x: x["problemsSolved"])
    return all_topics

def get_summary(data: dict) -> dict:
    """
    Returns a combined dict with both difficulty stats and topic stats.
    """
    return {
        "difficulty": get_difficulty_stats(data),
        "topics": get_topic_stats(data)
    }
