# Task 1 C

## Overview
The cluster is built to mimic production environments where service dependencies and health monitoring are critical.

- Hydra Base Service: A FastAPI/Flask app simulating real-world workloads and failures.

- Hydra Exporter: A custom "sidecar" container that translates application state into Prometheus metrics.

- Prometheus: The time-series database acting as the "brain" for metrics storage.

- Grafana: The visualization layer for real-time monitoring and anomaly detection.

- Docker Network (```hydra-net```): An isolated bridge network facilitating DNS-based service discovery.

## Features
1. Hydra Base Service:

    The core microservice. It includes a specific endpoint to simulate system stress.

    - Port: 8000
    - Endpoints:
        - ```/health```: Returns standard health status.
        - ```/metrics```: Internal performance data.
        - ```/simulate_failure```: Triggers a simulated crash/latency spike for testing.

2. Metrics Exporter:

    A lightweight Python-based container that acts as the observation channel for the RL agent. It scrapes the Base Service and exposes data in the Prometheus text format on ```http://localhost:8000/```.

3. Monitoring stack:
    - Prometheus
        - Used to collect data
        - ```http://localhost:9090```
    - Grafana 
        - For visualizing the various metrics
        - ```http://localhost:3000 ```

## Steps / Implementation

 Docker compose is used to streamline the working of all the different containers required. The microservices will be running on 4 different containers all connected to a single docker network ```hydra-net```. 
 -  hydra-service:
    
    This is the hydra basae service that exposes the system metrics. It is running a simple python Flask server. The ```hydra-service/``` directory has all the necessary files to create the docker image.
 - exporter:

    The exporter service queries the ```/metrics``` endpoint on the base service and convertes the raw metrics into a format compatible with Prometheus. All necessary files to create the exporter image is in the ```exporter/``` directory.
 - prometheus: 
    
    Provides the data collecting tool and storage. The configurations required are present in the ```prometheus/``` directory.
 - grafana:
    
    Provides a dashboard to view all system metrics in an organized manner. The configurations are present in the ```grafana-provisioning/``` directory

After cloning the repo, the entire service can be started with ```docker compose up -d```
