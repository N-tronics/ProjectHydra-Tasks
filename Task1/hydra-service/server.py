from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK'

@app.route('/metrics')
def metrics():
    return jsonify({
        "cpu_usage": 45.5,
        "memory_usage": 128,
        "latency_ms": 12
    })

@app.route('/simulate_failure')
def failure():
    return 'Failure'

@app.route('/')
def root():
    return 'Go to /health'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
