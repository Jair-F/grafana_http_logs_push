from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
import time

class GrafanaButtonHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/shutdown":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(f"Grafana button clicked! Payload: {post_data}")
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*") 
            self.end_headers()
            
            response = "shutting down".encode("utf-8")
            self.wfile.write(response)
            
            print("Initiating server shutdown sequence...")
            threading.Thread(target=self.shutdown_server).start()
        else:
            self.send_response(404)
            self.end_headers()

    def shutdown_server(self):
        time.sleep(1)
        print("Server stopped.")
        os._exit(0)

    # needed for grafana CORS blocking error - allowing a wildcard header entry or a completely unrestricted response to custom headers.
    # FIX: Dynamically allows ANY header Grafana requests
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        
        # Read whatever headers the browser asks for and allow them explicitly
        requested_headers = self.headers.get("Access-Control-Request-Headers", "*")
        self.send_header("Access-Control-Allow-Headers", requested_headers)
        
        self.end_headers()

def run():
    port = 3030
    server_address = ("", port)
    httpd = HTTPServer(server_address, GrafanaButtonHandler)
    print(F"Grafana Listener Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
