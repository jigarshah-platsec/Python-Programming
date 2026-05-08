"""
Given API check_object(day, hour, min) -> True/False
Task: Find closest minute the object is disappreared in April (30 days)
Constraint: Cost to Query Day->100ms  Hour->500ms Min->1000ms

Approach: Hierarichale Bindary Search
            object_missing_day = BinarySearch(Days)
            object_missing_hour = BinarySearch(Hours)
            object_missing_minute = BinarySearch(Minutes)
"""

def check_object(day, hour, min): # return True or False when object is missing on that day, hour, min
    # Let's say it disappeared on Day 15, Hour 12, Min 34
    if day > 15: return True
    if day == 15 and hour > 12: return True
    if day == 15 and hour == 12 and min >= 34: return True
    return False

def find_closest_hierarchical():
    """
    Approach 1: Hierarchical Binary Search
    Instead of finding the FIRST MISSING time (which is buggy at 00:00 boundaries),
    we find the LAST PRESENT time (is_missing == False), then add 1 minute.
    """
    # 1. Find Day (Last Present Day at 00:00)
    low, high = 1, 30
    last_present_day = -1
    while low <= high:
        mid = (low + high) // 2
        if not check_object(mid, 0, 0): # False means PRESENT
            last_present_day = mid
            low = mid + 1             # Search for a later present day
        else:
            high = mid - 1            # Search for an earlier present day
            
        
    # 2. Find Hour (Last Present Hour at 00 min on last_present_day)
    low, high = 0, 23
    last_present_hour = -1
    while low <= high:
        mid = (low + high) // 2
        if not check_object(last_present_day, mid, 0):
            last_present_hour = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # 3. Find Minute (Last Present Minute on last_present_day, last_present_hour)
    low, high = 0, 59
    last_present_min = -1
    while low <= high:
        mid = (low + high) // 2
        if not check_object(last_present_day, last_present_hour, mid):
            last_present_min = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # The disappearance is EXACTLY 1 minute AFTER the last present minute
    dis_min = last_present_min + 1
    dis_hour = last_present_hour
    dis_day = last_present_day
    
    # Handle rollover for the time
    if dis_min == 60:
        dis_min = 0
        dis_hour += 1
    if dis_hour == 24:
        dis_hour = 0
        dis_day += 1
        
    return (dis_day, dis_hour, dis_min)

def find_closest_single_search():
    """
    Approach 2: Single Binary Search over all minutes in April.
    Simpler code, but costs 16 * 1000ms = 16000ms.
    """
    low = 0
    high = 30 * 24 * 60 - 1
    
    first_missing_time = (-1, -1, -1)
    while low <= high:
        mid = (low + high) // 2
        
        # Convert total minutes back to day, hour, minute
        day = (mid // (24 * 60)) + 1
        hour = (mid % (24 * 60)) // 60
        minute = mid % 60
        
        if check_object(day, hour, minute):
            first_missing_time = (day, hour, minute)
            high = mid - 1  # Object missing, search earlier in time
        else:
            low = mid + 1   # Object still present, search later in time
            
    return first_missing_time

if __name__ == "__main__":
    print("Hierarchical result:", find_closest_hierarchical())
    print("Single Search result:", find_closest_single_search())