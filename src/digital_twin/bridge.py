import json

def stream_to_digital_twin(crowd_data, endpoint):
    # crowd_data: positions, density, etc.
    # endpoint: URL or socket for 3D engine
    # Placeholder: send JSON to endpoint
    print(f"[DIGITAL TWIN] Sending to {endpoint}: {json.dumps(crowd_data)}")

# Example usage:
# stream_to_digital_twin({"positions": [...]}, "ws://localhost:9000") 