"""
► Final Challenge: Exercise 3 (The API Payload Auditor)
The Scenario:
Sierra's internal security team needs to audit Agent configs. You have to hit an internal HTTP API to fetch these configs.

The API returns paginated JSON: {"next_page_token": "abc", "agents": [...]}.

Inside the agents list, each agent has a context_window string payload.

The Problem: Some engineers accidentally hardcoded email addresses into the context_window prompts.

Your Task:
Write a function find_leaked_emails(api_client) that paginates through the entire API, uses Regex to find any email addresses hidden inside the context_window text, and returns a list of vulnerable agent_ids.

(Assume api_client.get_configs(page_token) exists and returns the JSON dictionary).
"""
import re
from typing import Any, Dict, List

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

class DummyApiClient:
    """A fake API client to simulate pagination and agent configs."""
    def __init__(self, pages):
        self.pages = pages
        
    def get_configs(self, page_token=None):
        if page_token == "token_page_2":
            return self.pages[1]
        elif page_token == "token_page_3":
            return self.pages[2]
        
        # Default to first page
        return self.pages[0]

"""
It protects memory with set()
it protects the CPU with a max_pages circuit breaker
it protects against network crashes with try/except, and 
it respects the API's token contract.
"""
def find_leaked_emails(api_client: Any, max_pages=1000) -> List[str]:
    vulnerable_agents = set()
    
    # Always start with None (or an empty string) for the very first API call
    current_token = None 
    
    # The Circuit Breaker protects against infinite API loops
    for _ in range(max_pages):
        # 1. Pass the actual token we got from the server
        try:
            res = api_client.get_configs(current_token)
        except Exception as e:
            print(f"API Failed: {e}")
            break
            
        # 2. Extract and Search (Your logic here was perfect)
        agents = res.get("agents", [])
        for agent in agents:
            context_window = agent.get("context_window", "")
            if EMAIL_PATTERN.search(context_window):
                vulnerable_agents.add(agent.get("agent_id", "unknown"))

        # 3. Update the token for the NEXT iteration of the loop
        current_token = res.get("next_page_token")
        
        # 4. If the server doesn't give us a token, we reached the end!
        if not current_token:
            break

    return list(vulnerable_agents)
""" ► 6. To defend against a broken API that returns the exact same pagination token in an infinite loop, which Staff-level pattern should you apply?
A) A Circuit Breaker (e.g., replacing while True with a bounded for loop).
B) A try/except block wrapped around the network call.
C) Storing all API responses in a Set to check for duplicates.
D) A 5-second time.sleep() between requests.
Answer A) 
"""
def main():
    mock_data = [
            {
                "next_page_token": "token_page_2",
                "agents": [
                    {"agent_id": "agent_1", "context_window": "Prompt without emails."},
                    {"agent_id": "agent_2", "context_window": "Send info to user123@gmail.com immediately."}
                ]
            },
            {
                "next_page_token": "token_page_3",
                "agents": [
                    {"agent_id": "agent_3", "context_window": "Clean prompt"},
                    {"agent_id": "agent_4", "context_window": "Please cc support@sierra.ai and help@sierra.ai"}
                ]
            },
            {
                "next_page_token": None,
                "agents": [
                    {"agent_id": "agent_5", "context_window": "Another clean prompt."}
                ]
            }
        ]
    
    client = DummyApiClient(mock_data)
    vulnerable_agents = find_leaked_emails(client)
    print("vulnerable_agents: ", vulnerable_agents)
    
    assert vulnerable_agents == ["agent_2", "agent_4"]


if __name__ == "__main__":
    main()
