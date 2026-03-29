from collections import defaultdict, deque

# SLIDING WINDOW is a DEQUE of requests being processed 
# containing timestamps (1..5..6) based on param: window_size (5ms) and 
# constrained to len of max_requests_allowed (3)
window = defaultdict(deque[int])


def rate_limit(req, window_size_seconds=5, threshold=3) -> bool:
    """
    Evaluates if an incoming request should be allowed or rate-limited based on a sliding window.
    
    This function tracks the number of requests per IP address within a specified time window. 
    It maintains a queue (deque) of valid request timestamps. Requests older than the window 
    size are evicted. If the number of requests in the current window reaches the threshold,
    the request is rate-limited and an Exception is raised.

    Args:
        req (dict): A dictionary representing the incoming request. 
                    Must contain an IP address (key "IP" or "ip") and a "timestamp".
        window_size_seconds (int, optional): The duration of the sliding window in seconds. Defaults to 5.
        threshold (int, optional): The maximum number of requests allowed within the window. Defaults to 3.

    Returns:
        bool: True if the request is allowed and successfully queues up for processing.
        
    Raises:
        KeyError: If the 'req' dictionary is missing required keys ('IP'/'ip' or 'timestamp').
        Exception: If the rate limit is exceeded for the IP address.
    """
    if ("IP" not in req and "ip" not in req) and "timestamp" not in req:
        raise KeyError

    # Support both "IP" and "ip" keys
    ip = req.get("IP") or req.get("ip")
    curTimeStamp = int(req.get("timestamp"))

    
    # Window Management: Clear old requests that fall out of (current window of reqs processing)
    while window[ip] and (window[ip][0] <= (curTimeStamp - window_size_seconds)):
        window[ip].popleft()
    
    # Now q only has all valid requests that came in last x seconds (window_size)
    if len(window[ip]) >= threshold:
        # Window already has 3 requests (processing) in last 5 secs
        raise Exception(f"RATE LIMIT OFFENDER IP: {ip}")        # RATE LIMIT HIT !!!!!

    # Queue up this request
    window[ip].append(curTimeStamp)
    return True         # Request successfully processing

