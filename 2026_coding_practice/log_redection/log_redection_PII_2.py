"""
► 3. When redacting 11-character SSNs from an infinite text stream, what is the correct $O(1)$ memory strategy to handle SSNs split across chunk boundaries?
A) Buffer the entire stream and run Regex at the end.
B) yield the buffer but hold back the last 10 characters for the next loop.
C) yield the buffer but hold back the first 10 characters of the next chunk.
D) Run Regex on each chunk independently and discard.

B) --- SSN can only be 10 char long so only that data from prev chunk is required to see disjoint SSN in next chunk
"""
import re
LOG_PATTERN = re.compile(r'(\[.+]\s)(INFO|WARN|ERROR|CRITICAL)\s(?P<TENANT>\w+)\slatency=(?P<LATENCY>\d{1,4})ms\spayload=(?P<PAYLOAD>.*)')
SSN_PATTNER = re.compile(r'\d{3}-\d{2}-\d{4}')
def redact_ssn(chunks):
    average_latency = {}
    total_latency = {}
    total_count = {}

    for chunk in chunks:
        match = re.search(LOG_PATTERN, chunk)
        if not match:
            continue
        tenant = match['TENANT']
        latency = int(match['LATENCY'])
        payload = match['PAYLOAD']

        # Parse only valid log lines
        if tenant and latency and payload:
            ssn_match = re.search(SSN_PATTNER, payload)
            if not ssn_match:
                continue
            redected_payload = re.sub(SSN_PATTNER, "***-**-****", payload)

            # Update Metrics of Tenant and Latency
            if tenant not in total_count:
                total_count[tenant] = 1
            else:
                total_count[tenant] += 1
                
            if tenant not in total_latency:
                total_latency[tenant] = latency
            else:
            total_latency[tenant] += latency
            
            average_latency[tenant] = total_latency[tenant] / total_count[tenant]
        
        
        redected_chunk = re.sub(LOG_PATTERN, redected_payload, chunk)
    
    yield get_top_k_offenders(average_latency, 3)


import heapq

def get_top_k_offenders(tenant_counts: dict, k: int):
    # Our VIP club (the heap)
    top_k_heap = []
    
    for tenant, count in tenant_counts.items():
        # 1. Push a tuple of (count, tenant) into the heap. 
        # Python heaps sort by the first element of the tuple.
        heapq.heappush(top_k_heap, (count, tenant))
        
        # 2. If the club has more than K people, kick out the smallest!
        if len(top_k_heap) > k:
            heapq.heappop(top_k_heap)
            
    # The heap now contains our top K offenders. 
    # We can sort it in reverse so the absolute worst is at index 0.
    return sorted(top_k_heap, reverse=True)



def main():
    # HEAP: PRIORITY Q: To find top K offenders - VIP Club! 
    # Example usage:
    counts = {"tenant_A": 50, "tenant_B": 120, "tenant_C": 5, "tenant_D": 300}
    print("Heap Example:", get_top_k_offenders(counts, k=2)) 
    # Output: [(300, 'tenant_D'), (120, 'tenant_B')]

    input_stream = [
        '[2026-03-10T10:00:00] INFO tenant_A latency=45ms payload="User asked about weather."',
        '[2026-03-10T10:00:01] WARN tenant_B latency=120ms payload="My SSN is 123-45-6789, please update my account."',
        '[2026-03-10T10:00:02] ERROR tenant_A latency=500ms payload="Database timeout."',
        '[2026-03-10T10:00:03] INFO tenant_B latency=80ms payload="User SSN 987-65-4321 verified."',
        '[2026-03-10T10:00:04] INFO tenant_C latency=30ms payload="Hello world."',
        '[malformed_log_line_ignore_me]'
    ]

    # We consume the generator
    offenders = next(redact_ssn(input_stream))
    print(offenders)
    assert offenders == [(100.0, 'tenant_B')]

    # print(safe_output)
    # Output: Hello, my SSN is ***-**-****. Please don't steal it!

    
    


if __name__ == "__main__":
    main()