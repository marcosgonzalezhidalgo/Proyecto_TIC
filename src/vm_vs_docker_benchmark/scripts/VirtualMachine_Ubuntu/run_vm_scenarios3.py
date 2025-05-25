import os
import time
import json
import psutil
import subprocess
import threading
import numpy as np
from datetime import datetime

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def monitor_usage(stop_event, interval=0.1):
    cpu_usages = []
    memory_usages = []

    while not stop_event.is_set():
        cpu_usages.append(psutil.cpu_percent(interval=None))
        memory_usages.append(psutil.virtual_memory().used / (1024 * 1024))  # MB
        time.sleep(interval)

    return cpu_usages, memory_usages

def measure(func):
    def wrapper(*args, **kwargs):
        stop_event = threading.Event()
        results = {}

        # Start monitoring thread
        cpu_data = []
        mem_data = []

        def monitor():
            nonlocal cpu_data, mem_data
            cpu_data, mem_data = monitor_usage(stop_event)

        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.start()

        start_time = time.time()
        try:
            func(*args, **kwargs)
        except Exception as e:
            stop_event.set()
            monitor_thread.join()
            raise e
        end_time = time.time()

        stop_event.set()
        monitor_thread.join()

        if cpu_data and mem_data:
            results["cpu"] = max(cpu_data)
            results["memory"] = max(mem_data) - min(mem_data)
        else:
            results["cpu"] = 0.0
            results["memory"] = 0.0

        results["time"] = end_time - start_time
        return results
    return wrapper

@measure
def idle():
    time.sleep(5)

@measure
def cpu_stress():
    subprocess.run(["stress-ng", "--cpu", "1", "--timeout", "5"], check=True)

@measure
def cpu_multi():
    subprocess.run(["stress-ng", "--cpu", str(psutil.cpu_count()), "--timeout", "5"], check=True)

@measure
def memory_stress():
    subprocess.run(["stress-ng", "--vm", "4", "--vm-bytes", "1G", "--timeout", "5", "--vm-keep"], check=True)

@measure
def memory_large():
    # Reservar ~6 GB usando numpy (8 bytes por int64)
    num_elements = (6 * 1024 * 1024 * 1024) // 8
    a = np.zeros(num_elements, dtype=np.int64)
    time.sleep(3)
    del a
    time.sleep(1)

@measure
def disk_write():
    with open("tempfile", "wb") as f:
        f.write(os.urandom(500 * 1024 * 1024))  # 500 MB
    os.remove("tempfile")

@measure
def disk_read():
    with open("tempfile", "wb") as f:
        f.write(os.urandom(500 * 1024 * 1024))  # 500 MB
    with open("tempfile", "rb") as f:
        _ = f.read()
    os.remove("tempfile")

@measure
def network_download():
    subprocess.run(["speedtest-cli", "--no-upload", "--bytes"], stdout=subprocess.DEVNULL)

@measure
def process_spawn():
    processes = []
    for _ in range(200):
        p = subprocess.Popen(["sleep", "0.1"])
        processes.append(p)
    for p in processes:
        p.wait()

pruebas = {
    "idle": idle,
    "cpu_stress": cpu_stress,
    "cpu_multi": cpu_multi,
    "memory_stress": memory_stress,
    "memory_large": memory_large,
    "disk_write": disk_write,
    "disk_read": disk_read,
    "network_download": network_download,
    "process_spawn": process_spawn,
}

results = {}

for name, test in pruebas.items():
    print(f"Running test: {name}")
    try:
        results[name] = test()
    except Exception as e:
        results[name] = {"error": str(e)}

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = os.path.join(RESULTS_DIR, f"results_vm_{timestamp}.json")
with open(filename, "w") as f:
    json.dump(results, f, indent=4)

print(f"All tests completed. Results saved in {filename}.")
