import time
import requests
from prometheus_client import start_http_server, Gauge

# 1. Define the 'Gauges' (The metrics Prometheus will track)
CPU_METRIC = Gauge('hydra_cpu_usage', 'CPU usage of the Hydra service')
MEM_METRIC = Gauge('hydra_mem_usage', 'Memory usage of the Hydra service')
SUCCESS_API_REQUESTS = Gauge('hydra_success_api_requests', 'Number of successful API requests')
ERROR_API_REQUESTS = Gauge('hydra_error_api_requests', 'Number of unsuccessful API requests')
AVG_API_RESPONSE_TIME = Gauge('hydra_avg_api_response_time', 'Average API Response Time')

def fetch_and_translate():
    while True:
        try:
            # 2. Reach out to the Hydra Service (Task 1)
            # 'hydra-service' is the name of the other container
            r = requests.get("http://rtsm-hydra-service:80/metrics")
            data = r.json()

            # 3. Update our Prometheus metrics with the JSON values
            CPU_METRIC.set(data['cpu_usage'])
            MEM_METRIC.set(data['mem_usage'])
            SUCCESS_API_REQUESTS.set(data['success_api_requests'])
            ERROR_API_REQUESTS.set(data['error_api_requests'])
            AVG_API_RESPONSE_TIME.set(data['avg_api_response_time'])
            
        except Exception as e:
            print(f"Waiting for Hydra service... {e}")
        
        time.sleep(5) # Scrape every 5 seconds

if __name__ == "__main__":
    # 4. Start a server on port 8000 to expose the NEW format
    start_http_server(8000)
    fetch_and_translate()
