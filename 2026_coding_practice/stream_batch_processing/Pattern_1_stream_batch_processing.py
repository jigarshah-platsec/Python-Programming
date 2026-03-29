
"""
Here are two highly probable coding exercises based on their stack (Multi-tenant, Agent Logs, Data Security, Metrics).

► Exercise 1: The "Context Bleed" Metrics Aggregator
The Scenario:
Sierra agents operate in a multi-tenant environment. You are handed a massive 50GB log file of agent API requests. You need to calculate the average token usage per tenant, but only for requests that hit the /v1/chat endpoint and resulted in a successful 200 status.

The Catch (Staff Level): You cannot load the file into memory. You must parse it line-by-line, extract the exact metrics, and ignore malformed SRE logs without crashing.

The Log Format:

Plaintext
[2026-03-14T09:00:00] INFO tenant_A endpoint=/v1/chat status=200 tokens=450
[2026-03-14T09:00:01] ERROR tenant_B endpoint=/v1/chat status=500 tokens=10
[2026-03-14T09:00:02] INFO tenant_A endpoint=/v1/chat status=200 tokens=550
[2026-03-14T09:00:03] INFO tenant_C endpoint=/v1/embeddings status=200 tokens=1000
malformed_garbage_line_here
Your Task:
Write a function calculate_average_tokens(log_stream) that returns a dictionary like {"tenant_A": 500.0}.
"""
import re
PATTERN = re.compile(r'\[.*]\s(?P<LOG_LEVEL>INFO|ERROR|WARN)\s(?P<TENANT>tenant_\w)\sendpoint=(?P<ENDPOINT>.*)status=(?P<STATUS>\d{3})\stokens=(?P<TOKENS>\d+)')

""" PATTERN: BATCH PROCESSING for Large (50GB) file in chunks(batches)
def read_file_in_batches(file_path, batch_size_bytes=100 * 1024 * 1024):
    with open(file_path, 'r') as f:
        while True:
            # Reads whole lines until the memory hint (~100MB) is reached
            lines_batch = f.readlines(batch_size_bytes)
            if not lines_batch:
                break
            yield lines_batch

"""
def find_top_offenders(chunks):
    # tenant -> [total_tokens, num_requests, average_tokens]
    tenant_info = {}

    for chunk in chunks:
        buffer = "" + chunk         # Temp: IN MEMORY Buffer - DO NOT LOG Entire 50GB Log file

        match = re.search(PATTERN, buffer)
        if not match:
            continue

        tenant = match["TENANT"]
        endpoint = match["ENDPOINT"].rstrip()
        status = int(match["STATUS"])
        tokens = int(match["TOKENS"])
        
        # Analyse only Successful requests
        if endpoint in ["/v1/chat"] and status == 200:  
            if tenant not in tenant_info:
                tenant_info[tenant] = [0, 0, 0]     # Initialize # tenant -> [total_tokens, num_requests, average_tokens]
            tenant_info[tenant][0] += tokens        # total_tokens
            tenant_info[tenant][1] += 1             # num_requests
            tenant_info[tenant][2] = tenant_info[tenant][0] // tenant_info[tenant][1] # average_tokens

        # Sort top tenants by average tokens
        # tenant_info.items() gives us (tenant, [total, count, average])
        sorted_items = sorted(tenant_info.items(), key=lambda item: item[1][2], reverse=True)
        # A dictionary {'tenant_A': 500, 'tenant_B': 300}
        resDict = {tenant: info[2] for tenant, info in sorted_items}

        yield resDict


def main():
    log_stream = [
        '[2026-03-14T09:00:00] INFO tenant_A endpoint=/v1/chat status=200 tokens=450',
        '[2026-03-14T09:00:01] ERROR tenant_B endpoint=/v1/chat status=500 tokens=10',
        '[2026-03-14T09:00:02] INFO tenant_A endpoint=/v1/chat status=200 tokens=550',
        '[2026-03-14T09:00:03] INFO tenant_C endpoint=/v1/embeddings status=200 tokens=1000',
        'malformed_garbage_line_here'
    ]
    
    """ PATTERN: Batch processing of input log stream 
    - using - The Generator Expression ()(Lazy Evaluation)
    
    # Simulate a lazy generator stream (just like reading from a massive file line-by-line)
    """
    stream = (line for line in log_stream)
    
    # The find_top_offenders function acts as a pipeline step
    # We iterate over its yielded results continuously
    for running_stats in find_top_offenders(stream):
        print("Live Stats:", running_stats)
if __name__ == "__main__":
    main()

"""

"""