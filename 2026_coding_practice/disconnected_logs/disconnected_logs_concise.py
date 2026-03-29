import re
from collections import defaultdict
from datetime import datetime

LOG_PATTERN = re.compile(
    r"\[(?P<timestamp>.*?)\]\s"
    r"(?P<trace_id>trace_\w+)\s"
    r"(?P<log_source>Auth|Database)"
    r"\sstatus=(?P<status_code>\d+)"
)

def analyze_disconnected_logs(input_stream):
    tenant = defaultdict(dict)
    total_latency = defaultdict(float)
    total_count = defaultdict(int)

    for log in input_stream:
        if not (match := LOG_PATTERN.search(log)): continue
        try:
            timestamp = datetime.fromisoformat(match["timestamp"])
        except ValueError: continue
            
        tid, source, status = match["trace_id"], match["log_source"], int(match["status_code"])

        if source == "Database" and status == 200:
            tenant.pop(tid, None)
        elif (source == "Auth" and status == 200) or (source == "Database" and status == 500):
            tenant[tid][source] = timestamp

        t_data = tenant.get(tid, {})
        if len(t_data) == 2:
            total_latency[tid] += abs((t_data["Auth"] - t_data["Database"]).total_seconds())
            total_count[tid] += 1
            tenant.pop(tid)

        # Evict old traces (> 1 hour)
        tenant = defaultdict(dict, {k: v for k, v in tenant.items() 
                                    if v and (timestamp - min(v.values())).total_seconds() <= 3600})

        if total_latency:
            avg_latency = {k: total_latency[k] / total_count[k] for k in total_latency}
            yield sorted(avg_latency.items(), key=lambda x: x[1], reverse=True)

def main():
    pass

if __name__ == "__main__":
    main()
