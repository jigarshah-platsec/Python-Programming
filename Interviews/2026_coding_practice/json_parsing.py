""" The JSON Batch Processor
► The Scenario: 
You are tailing a live, infinite stream of JSON logs from Sierra's AI agents. Every single line coming in is a JSON object containing a tenant_id and an http_status.

❖ The Challenge:
You need to count exactly how many 403 Forbidden errors each tenant is hitting.
However, because the stream literally never ends, you cannot just return a final dictionary at the end of the file.

🚀 Your Task:
Design a generator function that processes exactly 1,000 logs at a time (one batch).
The moment it reads the 1,000th log, it must yield a JSON summary of the 403 counts for that specific batch, wipe its memory completely clean, and immediately start counting the next 1,000 logs.
"""
from collections import defaultdict
import json
from typing import Iterator
def json_log_processor(input_stream: Iterator[str], batch_size=1000) -> Iterator[str]:
    # tenant_id -> 403 error count
    total_errors = defaultdict(int)
    current_count = 0   # Used to yield results (Generator) when batch_size is reached and RESET

    for line in input_stream:     # Each log line is JSON
        try:
            log_data = json.loads(line)
        except json.JSONDecodeError:
            continue            # log line is NOT JSON! skip this

        tenant_id = log_data.get("tenant_id", "unknown")
        error = log_data.get("http_status", "200")  # If no error consider it's successful
        
        # Challenge strictly asks for 403 Forbidden errors
        if str(error) in ["401", "403"]:
            total_errors[tenant_id] += 1
        
        # Batch Processing --- 
        current_count += 1    
        if current_count >= batch_size: # A Batch is complete
            # yield results
            yield json.dumps(total_errors)
            # RESET for next batch - 
            total_errors = defaultdict(int)     # MEMORY LEAK FIX!
            current_count = 0
    
    # EDGE CASE: All Batches ended, Flush last remaining results
    if current_count > 0 and len(total_errors) > 0:
        yield json.dumps(total_errors)


def main():
    logs = [
    '{"tenant_id": "tenant_A", "http_status": 403}',
    '{"tenant_id": "tenant_B", "http_status": 200}', # Should not be counted
    '{"tenant_id": "tenant_A", "http_status": 403}',
    ]

    # Stream using Python Generator! it'll be passed as Iterator!
    input_stream = (log for log in logs)
    for total_errors in json_log_processor(input_stream, batch_size=1000):
        print(f"Live Stats: {total_errors}")

if __name__ == "__main__":
    main()