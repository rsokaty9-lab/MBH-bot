from flask import Flask, render_template, jsonify
import threading
import time

# Track startup time
start_time = time.time()

app = Flask(__name__)

# Simple bot status for the dashboard
bot_status = {
    "is_ready": True,
    "user": "Deployment Bot",
    "guild_count": 1,
    "last_deployment": None,
    "total_deployments": 0
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify(bot_status)

@app.route('/api/health')
def api_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": time.time() - start_time if 'start_time' in globals() else 0
    })

@app.route('/ping')
def ping():
    """Simple ping endpoint to keep service alive"""
    return "pong"



def start_web_server():
    """Start the Flask web server"""
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
