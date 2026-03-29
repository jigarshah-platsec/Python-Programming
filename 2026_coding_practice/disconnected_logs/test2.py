def foo(average_latency):
    tenant_id = 1
    return [tenant_id, average for tenant_id, average in average_latency.items()]
