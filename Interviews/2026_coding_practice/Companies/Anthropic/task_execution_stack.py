"""
Solution: https://leetcode.com/problems/exclusive-time-of-functions/solutions/7593940/simplest-solution-beats-100-python-by-sa-3ip5
"""
class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        stack = []
        res = [0]*n
        prev_ts = 0         # This is the MAGIC TRICK! Keep prev_ts up to date to calc right result for the prev_task (if START new) or this_task (if END) 

        for log in logs:
            id, status, ts = log.split(":")
            id, ts = int(id), int(ts)

            match status:
                case "start":
                    # print("processing start")
                    # print("id:", id, "ts: ", ts, "stack: ", stack)
                    if stack:
                        # Add res for previous running task, but don't remove from stack as it's still running!
                        prev_task = stack[-1]
                        res[prev_task] += ts - prev_ts
                    # Add this task to running stack
                    stack.append(id)
                    prev_ts = ts
 
                    # print("id:", id, "ts: ", ts, "stack: ", stack, "res: ", res)


                case "end":
                    # print("processing end")
                    # print("id:", id, "ts: ", ts, "stack: ", stack)
                    # This task is done, calc res
                    stack.pop()
                    res[id] += ts - prev_ts + 1     # exclusive ts calc
                    prev_ts = ts + 1                # exclusive ts

                    # Done with this task
                    # print("id:", id, "ts: ", ts, "stack: ", stack, "res: ", res)

                case _:
                    raise Exception("Invalid Status Code Detected")

        return res