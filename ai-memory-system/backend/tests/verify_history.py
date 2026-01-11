import requests
import uuid
import time

BASE_URL = "http://127.0.0.1:8000"

def test_history():
    task_id = f"test_task_{uuid.uuid4().hex[:6]}"
    print(f"Dataset Task ID: {task_id}")

    # 1. Send a message
    print("Sending message...")
    res = requests.post(f"{BASE_URL}/chat", json={
        "task_id": task_id,
        "message": "Hello, remember this string: BANANA"
    })
    print(f"Chat Response: {res.json()}")

    # 2. Fetch history
    print("Fetching history...")
    time.sleep(1) # wait for async write potentially (though it's sync in code)
    res = requests.get(f"{BASE_URL}/memory/session/{task_id}")
    data = res.json()
    
    print("\n--- History Data ---")
    print(data)
    
    if "messages" in data and len(data["messages"]) > 0:
        print("\n[PASS] History retrieved successfully.")
        msg = data["messages"][0]["content"]
        print(f"Content: {repr(msg)}")
    else:
        print("\n[FAIL] No history found!")

if __name__ == "__main__":
    test_history()
