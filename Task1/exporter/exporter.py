import time
import requests
from prometheus_client import start_http_server, Gauge

# 1. Define the 'Gauges' (The metrics Prometheus will track)
CPU_METRIC = Gauge('hydra_cpu_usage', 'CPU usage of the Hydra service')
MEM_METRIC = Gauge('hydra_mem_usage', 'Memory usage of the Hydra service')
LATENCY_METRIC = Gauge('hydra_latency', 'Latency of the Hydra service')

def fetch_and_translate():
    while True:
        try:
            # 2. Reach out to the Hydra Service (Task 1)
            # 'hydra-service' is the name of the other container
            r = requests.get("http://hydra-service:80/metrics")
            data = r.json()

            # 3. Update our Prometheus metrics with the JSON values
            CPU_METRIC.set(data['cpu_usage'])
            MEM_METRIC.set(data['memory_usage'])
            LATENCY_METRIC.set(data['latency_ms'])
            
        except Exception as e:
            print(f"Waiting for Hydra service... {e}")
        
        time.sleep(5) # Scrape every 5 seconds

if __name__ == "__main__":
    # 4. Start a server on port 8000 to expose the NEW format
    start_http_server(8000)
    fetch_and_translate()
