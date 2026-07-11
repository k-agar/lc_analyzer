import httpx

LEETCODE_URL = "https://leetcode.com/graphql"

async def fetch_user_data(username: str):
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        tagProblemCounts {
          advanced { tagName problemsSolved }
          intermediate { tagName problemsSolved }
          fundamental { tagName problemsSolved }
        }
        userCalendar {
          submissionCalendar
        }
        badges {
          id
          name
          displayName
          icon
          hoverText
        }
      }
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage
        badge {
          name
        }
      }
    }
    """
    variables = {"username": username}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            LEETCODE_URL,
            json={"query": query, "variables": variables},
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        response.raise_for_status()
        return response.json()
