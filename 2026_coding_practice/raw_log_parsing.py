"""
Task:
Write a function analyze_logins(logs) that returns a dictionary counting failed ConsoleLogin attempts per user.

Constraints/Goals:

Target only Event: ConsoleLogin.
Count only Status: Failure.

Resilience: If a line is missing the Event, User, or Status field, or is completely malformed, skip it (do not crash).
"""
logs = [
    "RequestId: 123 | Event: ConsoleLogin | User: jigar | Status: Success",
    "RequestId: 124 | Event: ListBuckets | User: malicious_actor | Status: AccessDenied",
    "CORRUPTED_LINE_IGNORE_ME",
    "RequestId: 125 | Event: ConsoleLogin | User: hacker | Status: Failure",
    "RequestId: 126 | User: forgot_event_name | Status: Failure", # Missing 'Event'
    "RequestId: 127 | Event: ConsoleLogin | User: hacker | Status: Failure"
]

from collections import defaultdict
from typing import List

TOTAL_PARTS = 4     # RequestID | Event | User | Status
def analyze_logins(logs):
    # A map having failure count for each user i.e {"hacker": 2, "unknown": 3}
    userMap = defaultdict(int)
        
    for entry in logs:
        parts = entry.split("|")
        if len(parts) < TOTAL_PARTS:
            continue

        # A map storing list of {key, value} for each field
        # i.e {"RequestID": 125}, {"Event": "ConsoleLogin"}, {"User": "hacker"}, {"Status": "Failure"}
        entryMap = {}
        # store parts of entry as {Key: Val}
        # Those parts can be in any order!
        for part in parts:
            keyValue = part.split(":")
            key, value = keyValue[0].strip(), keyValue[1].strip()
            entryMap[key] = value

        # Analyse this entry now
        if entryMap.get("Event", "unknown") == "ConsoleLogin" and entryMap.get("Status", "unknown") == "Failure":
            userMap[entryMap.get("User", "unknown")] += 1

        entryMap = {}
    
    return userMap

def main():
    userMap = analyze_logins(logs)
    for user, count in userMap.items():
        print(user, count)
    

if __name__ == "__main__":
    main()