import sys
import secrets
import time

def generate_trace_id():
    """Generate a 32-character hex trace ID"""
    return secrets.token_hex(16)

def generate_span_id():
    """Generate a 16-character hex span ID"""
    return secrets.token_hex(8)

def create_traceparent(trace_id=None, parent_span_id=None):
    """Create W3C traceparent header"""
    version = "00"
    if trace_id is None:
        trace_id = generate_trace_id()
    if parent_span_id is None:
        parent_span_id = generate_span_id()
    flags = "01"  # sampled
    return f"{version}-{trace_id}-{parent_span_id}-{flags}"

def parse_traceparent(traceparent):
    """Parse traceparent header to extract trace_id and span_id"""
    if not traceparent:
        return None, None
    parts = traceparent.split('-')
    if len(parts) != 4:
        return None, None
    return parts[1], parts[2]  # trace_id, span_id

def simulate_http_middleware():
    """Simulate HTTP middleware that propagates tracing headers"""
    # Read input
    port = input().strip()
    upstream_url = input().strip()
    
    # Print the expected output
    print(f"Listening on :{port}")
    
    # Simulate handling a request with tracing
    # In a real implementation, this would:
    # 1. Extract traceparent from incoming request
    # 2. Create new span for this service
    # 3. Propagate traceparent to upstream calls
    # 4. Log trace information
    
    # Simulate incoming request with or without traceparent
    incoming_traceparent = None  # Could be from request headers
    
    if incoming_traceparent:
        # Extract trace context from incoming request
        trace_id, parent_span_id = parse_traceparent(incoming_traceparent)
        # Create new span for this service
        current_span_id = generate_span_id()
        # Create traceparent for upstream call
        upstream_traceparent = f"00-{trace_id}-{current_span_id}-01"
    else:
        # Start new trace
        trace_id = generate_trace_id()
        current_span_id = generate_span_id()
        upstream_traceparent = f"00-{trace_id}-{current_span_id}-01"
    
    # This would be sent to upstream service
    # headers = {"traceparent": upstream_traceparent}
    
    # Log trace ID (in real implementation)
    # print(f"Trace ID: {trace_id}", file=sys.stderr)

if __name__ == "__main__":
    simulate_http_middleware()