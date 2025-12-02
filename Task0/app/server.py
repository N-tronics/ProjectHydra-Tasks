from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK'

@app.route('/')
def root():
    return 'Go to /health'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
