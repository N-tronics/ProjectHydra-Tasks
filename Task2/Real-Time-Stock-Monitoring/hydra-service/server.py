from flask import Flask, jsonify, request, render_template
import time
import yfinance as yf
import container_metrics as contMetrics
    

app = Flask(__name__)
success_api_requests = 0
error_api_requests = 0
api_response_times = []
avg_api_response_time = 0
dashboard_page = 'index.html'

artificial_delay = 0
    
@app.route('/health')
def health():
    return 'OK'
        
@app.route('/metrics')
def metrics():
    data = contMetrics.get_container_stats()
    data["success_api_requests"] = success_api_requests
    data["error_api_requests"] = error_api_requests
    data["avg_api_response_time"] = avg_api_response_time
    return jsonify(data)
        
@app.route('/simulate_failure')
def failure():
    global artificial_delay
    artificial_delay = float(request.args.get('artificial_delay', 0))
    return f'Set arg \'artificial_delay\' in url params to set an artificial delay in seconds\nCurrent artificial_delay: {artificial_delay}'
        
@app.route('/data')
def data():
    global success_api_requests, error_api_requests, avg_api_response_time, api_response_times
    start_time = time.perf_counter()
    resp_data = {
        "ticker": None,
        "current_price": None,
        "price_change": None,
        "percentage_change": None,
        "market_cap": None,
        "volume": None
    }
    ticker = request.args.get('ticker', 'GOOGL')
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period='1d')
    if len(stock_info) == 0:
        error_api_requests += 1
        return resp_data
                
    resp_data["ticker"] = ticker
    resp_data["current_price"] = stock_info['Close'].iloc[0]
    prev_close = stock.info.get('previousClose', resp_data["current_price"])
    resp_data["price_change"] = resp_data["current_price"] - prev_close
    resp_data["percentage_change"] = resp_data["price_change"] / prev_close * 100 if prev_close != 0 else 0
    resp_data["market_cap"] = stock.info.get('marketCap', 'N/A')
    resp_data["volume"] = int(stock_info['Volume'].iloc[0])
    
    time.sleep(artificial_delay)
    elapsed_time = time.perf_counter() - start_time
               
    api_response_times.append(elapsed_time)
    if (len(api_response_times) > 10):
        api_response_times = api_response_times[1:]
    avg_api_response_time = sum(api_response_times) / 10
    success_api_requests += 1
    return resp_data
        
@app.route('/')
def index():
    return render_template(dashboard_page)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
