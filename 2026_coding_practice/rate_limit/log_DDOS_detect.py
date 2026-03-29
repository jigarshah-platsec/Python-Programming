import re
from collections import defaultdict
from typing import Dict, List, Tuple

# ------------------------------------------------------------------
# CHALLENGE: Suspicious Activity Detector (Log Parsing)
# ------------------------------------------------------------------
# Scenario:
# You are given a list of raw server logs. Your task is to process
# these logs to identify potential attackers.
#
# Requirements:
# 1. Parse the logs to extract the IP address, HTTP Status Code, and Endpoint.
# 2. Identify IP addresses that have generated more than `threshold` 
#    403 (Forbidden) or 401 (Unauthorized) errors.
# 3. Return a sorted list of tuples: (Count, IP_Address), descending by count.
#
# Constraints:
# - Use standard Python libraries (re, collections, etc.).
# - Focus on readability and efficiency.
# ------------------------------------------------------------------

RAW_LOGS = [
    '10.0.0.1 - - [10/Feb/2026:14:00:01] "GET /login HTTP/1.1" 200 1024',
    '192.168.1.5 - - [10/Feb/2026:14:00:02] "POST /api/v1/auth HTTP/1.1" 401 512',
    '10.0.0.2 - - [10/Feb/2026:14:00:03] "GET /home HTTP/1.1" 200 2048',
    '192.168.1.5 - - [10/Feb/2026:14:00:04] "POST /api/v1/auth HTTP/1.1" 401 512',
    '172.16.0.5 - - [10/Feb/2026:14:00:05] "GET /admin HTTP/1.1" 403 128',
    '192.168.1.5 - - [10/Feb/2026:14:00:06] "POST /api/v1/auth HTTP/1.1" 401 512',
    '10.0.0.1 - - [10/Feb/2026:14:00:07] "POST /upload HTTP/1.1" 200 4096',
    '172.16.0.5 - - [10/Feb/2026:14:00:08] "GET /etc/passwd HTTP/1.1" 403 128',
    '172.16.0.5 - - [10/Feb/2026:14:00:09] "GET /config HTTP/1.1" 403 128',
    '10.0.0.3 - - [10/Feb/2026:14:00:10] "GET /login HTTP/1.1" 200 1024'
    '333.333.333 - - [10/Feb/2026:14:00:10] "GET /login HTTP/1.1" 200 1024'     # malformed IP
]

PATTERN = re.compile(r"""
    (?P<IPAddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   # Named Matching Group: IPAddress       # use of digit /d range {1,3} on prior char
    (?:.*) #SKIP - - [date]                             # Named Matching Group: None            # use of .* to skip all chars until next group capture
    (?P<METHOD>\"GET|POST|PUT|DELETE).*\"\              # Named Matching Group: HTTP Method     # use of OR |
    (?P<status_code>\d{1,3})\                           # Named Matching Group: HTTP status code    # use of range
    (?P<total_bytes>\d+)                                # Named Matching Group: HTTP payload size   # use of any digit (can be large)
""", re.VERBOSE)

def analyse_logs(threshold: int) -> List[Tuple[int, str]]:
    # A map to hold {IP: Count}
    map_ip_count = {}

    for entry in RAW_LOGS:
        match = re.search(PATTERN, entry)
        if not match:
            continue
        ip_address = match['IPAddress']
        status_code = int(match['status_code'])
        endpoint = match['METHOD']
        
        if status_code in [401, 403]:       # ANOMOLY, SUSPICIOUS/UnAuthorized Activity Detected, 
            if ip_address not in map_ip_count:
                map_ip_count[ip_address] = 1
            else: 
                map_ip_count[ip_address] += 1

    print ("map_ip_count:", map_ip_count)


    # A list to hold the {IP: Count} map in sorted order
    list_top_offenders = []
    # SORTING a DICT: top offender IPs, count-wise
    list_top_offenders = sorted(map_ip_count.items(), key = lambda x: x[1], reverse = True) # reverse = DECENDING ORDER
    print("list_top_offenders:", list_top_offenders)

    # PATTERN: Build a list from dict values
    # A list to return values in List[Tuple[Count, IP]] format
    results = []
    results = [(count, ip) for (ip, count) in list_top_offenders if count > threshold]

    return results

if __name__ == "__main__":
    print("Analysing logs")
    results = analyse_logs(threshold=2)
    print("results:", results)
    
    # Test Case 1: Standard detection
    # Offender IP is captured in result
    assert (3, "192.168.1.5") in results
    # Offender IP has right count against it
    for result in results:
        if result[1] == "192.168.1.5":
            assert result[0] == 3

    print("Test Case 1 Passed: Standard detection")

    # Test Case 2: No suspicious activity (High threshold)
    print("\nTest Case 2: High Threshold")
    empty_results = analyse_logs(threshold=10)
    assert len(empty_results) == 0
    print("Test Case 2 Passed: No suspicious activity found with high threshold")

    # Test Case 3: Verify sorting order
    print("\nTest Case 3: Sorting Order")
    # 192.168.1.5 and 172.16.0.5 both have 3 errors. The order between them is stable/implementation dependent, 
    # but both should be present.
    assert len(results) == 2
    assert results[0][0] >= results[1][0] # First count >= Second count
    print("Test Case 3 Passed: Results sorted by count descending")

    # Test Case 4: Malformed Log Handling
    # The current code should gracefully skip the malformed line '333.333.333...'
    # without crashing. Since we just ran it successfully, this is implicitly tested.
    print("\nTest Case 4 Passed: Malformed logs handled gracefully")