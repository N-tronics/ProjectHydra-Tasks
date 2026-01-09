import time
import os

def get_cpu_usage_nanoseconds():
    path = "/sys/fs/cgroup/cpu.stat"
    if not os.path.exists(path):
        raise FileNotFoundError("Cgroup v2 path not found. Ensure you are on Linux with cgroup v2 enabled.")

    with open(path, "r") as f:
        for line in f:
            if line.startswith("usage_usec"):
                # usage_usec is in microseconds; convert to nanoseconds
                return int(line.split()[1]) * 1000
    return 0

def calculate_cpu_percentage(interval=0.5):
    t1_cpu = get_cpu_usage_nanoseconds()
    t1_time = time.time_ns()

    time.sleep(interval)

    t2_cpu = get_cpu_usage_nanoseconds()
    t2_time = time.time_ns()

    usage_delta = t2_cpu - t1_cpu
    time_delta = t2_time - t1_time

    if time_delta == 0:
        return 0.0
        
    cpu_pct = (usage_delta / time_delta) * 100
    return cpu_pct

def get_metric(paths):
    for path in paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read().strip()
    return None

def get_container_stats():
    mem_usage = get_metric([
        '/sys/fs/cgroup/memory.current',           # v2
        '/sys/fs/cgroup/memory/memory.usage_in_bytes' # v1
    ])
    
    mem_limit = get_metric([
        '/sys/fs/cgroup/memory.max',               # v2
        '/sys/fs/cgroup/memory/memory.limit_in_bytes' # v1
    ])

    cpu_usage = calculate_cpu_percentage()

    return {
        "mem_usage": int(mem_usage) / (1024 * 1024),
        "cpu_usage": float(cpu_usage)
    }

if __name__ == "__main__":
    print(get_container_stats())
