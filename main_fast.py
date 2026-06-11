import time
import requests
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from threading import Thread
import sys

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

shutdown = False
trigger_alert = False

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

def run_background_loop():
    global shutdown, trigger_alert
    print("Ready. Standing by for interactive Grafana button inputs...")
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
            
            time.sleep(1)
            
    except Exception as e:
        print(f"Loop error: {e}")
        
    trigger_live_log("Shutting down data stream engine connection", "info")
    print("Stopping automation engine smoothly.")
    sys.exit(0)


# MODERN FIX: Using asynccontextmanager lifespan handler instead of @app.on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Everything inside here executes BEFORE the server starts handling client requests
    t = Thread(target=run_background_loop, daemon=True)
    t.start()
    yield
    # Code right after 'yield' executes when the server shuts down (Ctrl+C)
    global shutdown
    shutdown = True

# Assign the lifespan event to the application lifecycle
app = FastAPI(lifespan=lifespan)

# Enable CORS for browser security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Matches the endpoint configured in your panel canvas button config
@app.post("/shutdown")
def trigger_action():
    print("🚀 Button clicked in Grafana! Initiating script pipeline...")
    global trigger_alert
    trigger_alert = True
    return JSONResponse(content={"status": "success"})


if __name__ == "__main__":
    print("📡 Server web listener booting up...")
    # Port 3030 matches your Grafana Canvas settings
    uvicorn.run("main_fast:app", host="0.0.0.0", port=3030, log_level="info")
