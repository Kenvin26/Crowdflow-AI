import json

def stream_to_ar_app(crowd_data, endpoint):
    # crowd_data: positions, density, etc.
    # endpoint: URL or socket for AR app
    print(f"[AR] Sending to {endpoint}: {json.dumps(crowd_data)}")

# Example usage:
# stream_to_ar_app({"positions": [...]}, "ws://localhost:9100") 