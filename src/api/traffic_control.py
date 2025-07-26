from fastapi import APIRouter

router = APIRouter()

@router.post('/traffic/signal')
def control_signal(action: str):
    # action: 'green', 'red', 'open', 'close', etc.
    # Placeholder: send command to traffic system
    print(f"[TRAFFIC CONTROL] Action: {action}")
    return {"status": "ok", "action": action}

# Example usage:
# POST /traffic/signal {"action": "green"} 