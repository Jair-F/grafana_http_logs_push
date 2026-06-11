from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so your browser allows Grafana to send the request
CORS(app)

@app.route('/shutdown', methods=['POST'])
def trigger_action():
    print("🚀 Button clicked in Grafana!")
    
    # PUT YOUR SCRIPT LOGIC HERE
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("📡 Server starting on port 3030...")
    # Bind to 0.0.0.0 so external networks can connect
    app.run(host='0.0.0.0', port=3030, debug=True)
