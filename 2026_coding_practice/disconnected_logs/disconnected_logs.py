import re
from collections import defaultdict
from datetime import datetime

LOG_PATTERN = re.compile(
    r"\[(?P<timestamp>.*?)\]\s"
    r"(?P<trace_id>trace_\w+)\s"
    r"(?P<log_source>Auth|Database)"
    r"\sstatus=(?P<status_code>\d+)"
)

"""
► 4. You are calculating latency between asynchronous Auth and Database logs. To prevent an Out-Of-Memory (OOM) crash from successful traces that never throw an error, what is the mandatory action?
A) Periodically call dictionary.clear().
B) Use a queue.Queue with a maxsize.
C) Use .pop() to completely remove the trace_id from the pending map once a match is found.
D) Track the trace_id in a separate Hash Set.
Answer C)
"""

def analyze_disconnected_logs(input_stream):
    """tenant_id ->
                    "Auth" - timestamp
                    "DataBase" - timestamp
    """
    tenant: defaultdict[str, dict[str, datetime]] = defaultdict(dict)
    total_latency: defaultdict[str, int] = defaultdict(int)
    total_count: defaultdict[str, int] = defaultdict(int)
    average_latency: defaultdict[str, float] = defaultdict(float)

    for log in input_stream:
        tokens = re.search(LOG_PATTERN, log)
        if not tokens:  # Skip Malformed log lines
            continue
            
        try:
            timestamp = datetime.fromisoformat(tokens["timestamp"])
        except ValueError:
            continue
            
        tenant_id = tokens["trace_id"]
        log_source = tokens["log_source"]
        status_code = int(tokens["status_code"])

        match log_source:
            case "Auth":
                if status_code == 200:
                    tenant[tenant_id]["Auth"] = timestamp

            case "Database":
                if status_code == 500:
                    tenant[tenant_id]["Database"] = timestamp
                elif status_code == 200:
                    if tenant_id in tenant:
                        del tenant[tenant_id]
            case _:
                pass

        # Evict old traces (> 1 hour) to prevent memory leak for incomplete traces
        keys_to_delete = []
        for tid, data in tenant.items():
            if data:
                oldest = min(data.values())
                if (timestamp - oldest).total_seconds() > 3600:
                    keys_to_delete.append(tid)
            else:
                keys_to_delete.append(tid)
                
        for tid in keys_to_delete:
            del tenant[tid]

        # Process the tenant if both "Auth" and "Database" are gathered
        if "Auth" in tenant.get(tenant_id, {}) and "Database" in tenant.get(tenant_id, {}):
            diff = abs(tenant[tenant_id]["Auth"] - tenant[tenant_id]["Database"])
            total_latency[tenant_id] += diff.total_seconds()
            total_count[tenant_id] += 1
            average_latency[tenant_id] = total_latency[tenant_id] / total_count[tenant_id]

            # Prevent Memory Leak by removing the processed log entries!
            del tenant[tenant_id]

        if average_latency:
            # Yield the current live stats, sorted by average latency descending
            yield sorted(average_latency.items(), key=lambda x: x[1], reverse=True)


"""
► 5. In a Producer-Consumer multi-threading architecture, what is the standard, thread-safe way to tell the Consumer's while True loop to shut down cleanly?
A) Call thread.join(timeout=1).
B) Change a global is_running boolean flag.
C) Raise a SystemExit exception from the Producer.
D) Inject a "Poison Pill" (like None) into the shared queue.Queue
Answer: D)
A shared queue.Queue() is thread-safe shared-memory between producers/consumer 
Passing None into the queue is the standard way to tell the Consumer, "There is no more data coming, break your loop and shut down cleanly."
"""
def main():
    input_stream = [
        "[2026-03-14T09:00:00] trace_abc123 Auth status=200",
        "[2026-03-14T09:00:02] trace_xyz789 Auth status=200",
        "[2026-03-14T09:00:05] trace_abc123 Database status=500",
        "[malformed_log_line]",
    ]
    # Stream processing
    input_stream = (stream for stream in input_stream)

    for result in analyze_disconnected_logs(input_stream):
        print(f"Live Stats: {result}")


if __name__ == "__main__":
    main()
