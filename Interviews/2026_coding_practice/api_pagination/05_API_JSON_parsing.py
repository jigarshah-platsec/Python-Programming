"""
Day 5: API & JSON Handling (The "Pagination Scanner")
"Who is an Admin but doesn't have MFA?"
Practice Problem: The Vulnerable Admin Scanner
Scenario:
You need to audit a user database. The API is paginated.
You must find all users who have role: "admin" BUT mfa_enabled: false.

The Mock API:
You are given a function mock_api_client(page_number) that simulates a REST call.
It returns a dictionary (JSON):

Your Task:
Write a function find_vulnerable_admins(api_function) that:

Calls the API starting at Page 1.

Loops through all pages until next_page is None.

Filters the results.

Returns a list of vulnerable id strings
"""
from typing import List, Dict, Any

def find_vulnerable_admins(api_client) -> List[str]:
    vulnerable_ids = []
    
    # Initialize the "pointer" to the first page
    current_page = 1

    # Loop as long as we have a page number to fetch
    while current_page:
        # 1. Fetch Data
        response = api_client(page_number=current_page)
        
        # 2. Process Current Page (Single Source of Truth)
        # Use .get() with empty list default to be safe
        for user in response.get("users", []):
            # strict check: role is admin AND mfa is explictly False
            if (user.get("role") == "admin") and (user.get("mfa_enabled") is False):
                vulnerable_ids.append(user.get("id"))
        
        # 3. Advance the Pointer
        # If "next_page" is None, the loop terminates naturally
        current_page = response.get("next_page")

    return vulnerable_ids

def mock_api_client(page_number) -> Dict:
    return {
    "users": [
        {"id": "user_1", "role": "admin", "mfa_enabled": True},
        {"id": "user_2", "role": "admin", "mfa_enabled": False}, # <--- VULNERABLE!
        {"id": "user_3", "role": "dev", "mfa_enabled": False}
    ],
    "next_page": None  # Returns None if there are no more pages.
    }

def main():
    vuln_ids_list = find_vulnerable_admins(mock_api_client)
    assert "user_2" in vuln_ids_list
    
if __name__ == "__main__":
    main()