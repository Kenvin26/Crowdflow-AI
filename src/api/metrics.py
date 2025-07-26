from fastapi import APIRouter, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()

active_gauge = Gauge('crowdflow_active', 'Active people count')
in_counter = Counter('crowdflow_in', 'Cumulative in count')
out_counter = Counter('crowdflow_out', 'Cumulative out count')

@router.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Example usage in your pipeline:
# active_gauge.set(active_count)
# in_counter.inc(in_count)
# out_counter.inc(out_count) 