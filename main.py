import time
import requests

"""
important to change in defaults.ini:

[auth.anonymous]
# enable anonymous access
enabled = true

# specify organization name that should be used for unauthenticated users
org_name = Main Org.

# specify role for unauthenticated users
org_role = Editor

# mask the Grafana version number for unauthenticated users
hide_version = false

# number of devices in total
device_limit =
"""

STREAM_NAME = "application_name"

GRAFANA_URL = "http://localhost:3000"
PUSH_URL = f"{GRAFANA_URL}/api/live/push/{STREAM_NAME}"

def trigger_live_log(message: str, level: str = "info"):
    headers = {
        "Content-Type": "text/plain" 
    }
    
    current_time_ns = time.time_ns()
    
    # Influx Line Protocol: metric_name field1="val",field2="val" timestamp
    payload = f"log message=\"{message}\",level=\"{level}\" {current_time_ns}"
    
    try:
        response = requests.post(PUSH_URL, data=payload, headers=headers)
        if response.status_code == 200:
            print(f"[TRIGGERED PUSH] Sent {level.upper()}: {message}")
        else:
            print(f"[FAILED] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[NETWORK ERROR]: {e}")

if __name__ == "__main__":
    print("Ready. Triggering updates on demand...")
    
    while True:
        # Example: Simulating sporadic event triggers instead of a steady timer loop
        trigger_live_log("User logged in successfully", "info")
        time.sleep(0.5)
        trigger_live_log("Database connection pool capacity reached 90%", "warn")
        time.sleep(4)
        trigger_live_log("Payment gateway timeout detected!", "error")
