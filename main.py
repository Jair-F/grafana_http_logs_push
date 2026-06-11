import time
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread

"""
Important to change in defaults.ini:
[auth.anonymous]
enabled = true
org_name = Main Org.
org_role = Editor
"""

STREAM_NAME = "application_name"
GRAFANA_URL = "http://localhost:3000"
PUSH_URL = f"{GRAFANA_URL}/api/live/push/{STREAM_NAME}"

app = Flask(__name__)
CORS(app)  # Critical for browser execution security

shutdown = False
trigger_alert = False

# Matches the endpoint configured in your panel canvas button config
# @app.route('/', methods=['POST'])
@app.route('/shutdown', methods=['POST'])
def trigger_action():
    print("🚀 Button clicked in Grafana! Initiating script pipeline...")
    global trigger_alert
    trigger_alert = True
    return jsonify({"status": "success"})

def trigger_live_log(message: str, level: str = "info"):
    headers = {"Content-Type": "text/plain"}
    current_time_ns = time.time_ns()
    
    payload = f"log message=\"{message}\",level=\"{level}\" {current_time_ns}"
    
    try:
        response = requests.post(PUSH_URL, data=payload, headers=headers)
        if response.status_code == 200:
            print(f"[LIVE PUSH] Sent {level.upper()}: {message}")
        else:
            print(f"[FAILED] Status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[NETWORK ERROR]: {e}")

def run_flask() -> None:
    print("📡 Server web listener booting up...")
    # CRITICAL FIX: debug=False prevents the background thread from throwing Signal errors
    # use_reloader=False stops background threading conflicts
    app.run(host='0.0.0.0', port=3030, debug=False, use_reloader=False)

if __name__ == "__main__":
    print("Ready. Standing by for interactive Grafana button inputs...")
    
    t = Thread(target=run_flask, daemon=True)
    t.start()    

    try:
        while not shutdown:
            if trigger_alert:
                print("⚡ Processing button-triggered automation script...")
                shutdown = True
            
            # Execute your automation or sequential logging scripts here
            trigger_live_log("User requested system update via panel UI", "info")
            time.sleep(0.5)
            trigger_live_log("Simulated database connection pool validation complete", "warn")
            time.sleep(1.5)
            trigger_live_log("Grafana triggered execution completed successfully!", "error")
            
            # Reset the button trigger latch state, waiting for the next press

            # Tiny sleep constraint prevents 100% CPU thread thrashing while waiting
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping automation engine smoothly.")
        shutdown = True
        
    trigger_live_log("Shutting down data stream engine connection", "info")
