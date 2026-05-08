"""
Algorithm: GREEDY       DS: MIN-HEAP (To maintain meeting end-times)
Make sure the intervals are in sorted order before processing, In this case, sort by "start time"

Case 1: START of this meeting is < end of shortest meeting --- Need new meeting room
Case 2: START of this meeting is >= end of shortest meeting --- Re-use same meeting room ---> update end 

"""
from typing import List
import heapq
from collections import defaultdict

class Solution:
    def minMeetingRooms(self, meetings: List[List[int]]) -> int:
        meetings = sorted(meetings, key=lambda x: x[0]) # Sort meetings by start time
        
        
        # Heap of [meeting[END_TIME]] 
        # Example: meetings = [[0,30],[5,10],[15,20]] --> Book room until end: 30, 10, 20 
        #             rooms = [10, 20, 30] --- 1st room is available on top and so on... 
        #           
        rooms = []      
        
        
        START_TIME, END_TIME = 0, 1
        for i, meeting in enumerate(meetings):
            if i == 0:  # 1st meeting --- Need new meeting room
                heapq.heappush(rooms, meeting[END_TIME])
                continue
            
            # print(f"rooms: {rooms}, meeting: {meeting}")
            
            # Case 2: START of this meeting is < end of shortest meeting --- Re-use same meeting room ---> update end            
            lastMeetingEnding = rooms[0]
            if meeting[START_TIME] >= lastMeetingEnding:
                heapq.heapreplace(rooms, meeting[END_TIME])
            
            # Case 1: START of this meeting is < end of shortest meeting --- Need new meeting room
            else:
                heapq.heappush(rooms, meeting[END_TIME])
        
        return len(rooms)
    def minMeetingRoomsReq(self, meetings):
        if not meetings: return 0
        meetings = sorted(meetings, key=lambda x:x[0])
        # First meeting, just add a room that's already available to begin first meeting
        rooms = [0]

        startIdx, endIdx = 0, 1
        for meeting in meetings:
            start, end = meeting[startIdx], meeting[endIdx]

            # If the room that finishes earliest is free, reuse it
            if rooms[0] <= start:
                heapq.heapreplace(rooms, end)
            else:
                heapq.heappush(rooms, end)
        
        return len(rooms)

            
    def mostBooked(self, meetings, total_rooms):
        meetings.sort(key=lambda x: x[0])
        room_end_times = [0] * total_rooms
        freq = [0] * total_rooms
        
        for start, end in meetings:
            found_unused_room = False
            
            # 1. Look for the first (lowest ID) room that is free
            for i in range(total_rooms):
                if room_end_times[i] <= start:
                    room_end_times[i] = end
                    freq[i] += 1
                    found_unused_room = True
                    break
            
            # 2. If no room is free, wait for the one that ends first
            if not found_unused_room:
                # Find the minimum end time and the lowest room ID associated with it
                min_end_time = min(room_end_times)
                room_id = room_end_times.index(min_end_time)
                
                room_end_times[room_id] += (end - start)
                freq[room_id] += 1
                
        return freq.index(max(freq))

if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ([[0, 30], [5, 10], [15, 20]], 2),
        ([[7, 10], [2, 4]], 1),
        ([[1, 5], [8, 9], [8, 9]], 2),
        ([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]], 4),
        ([], 0)
    ]
    
    print("Testing minMeetingRooms:")
    for meetings, expected in test_cases:
        actual = sol.minMeetingRooms(meetings)
        print(f"Meetings: {meetings}, Expected: {expected}, Actual: {actual}, {'PASS' if actual == expected else 'FAIL'}")

    print("\nTesting minMeetingRoomsReq:")
    for meetings, expected in test_cases:
        actual = sol.minMeetingRoomsReq(meetings)
        print(f"Meetings: {meetings}, Expected: {expected}, Actual: {actual}, {'PASS' if actual == expected else 'FAIL'}")

    print("\nTesting mostBooked:")
    test_cases_most_booked = [
        (2, [[0, 10], [1, 5], [2, 7], [3, 4]], 0),
        (3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]], 1),
        (2, [[0, 5], [1, 2], [6, 10]], 0) # This should fail on single-heap logic
    ]
    for n, meetings, expected in test_cases_most_booked:
        actual = sol.mostBooked(meetings, n)
        print(f"n: {n}, Meetings: {meetings}, Expected (Room ID): {expected}, Actual: {actual}, {'PASS' if actual == expected else 'FAIL'}")
