import subprocess
import time
import json
import os
import csv
from datetime import datetime

results_dir = "/app/results"
os.makedirs(results_dir, exist_ok=True)

def usar_cgroup_v2():
    return os.path.exists("/sys/fs/cgroup/cgroup.controllers")

CGROUP_V2 = usar_cgroup_v2()

def leer_memoria_docker():
    try:
        if CGROUP_V2:
            path = "/sys/fs/cgroup/memory.current"
        else:
            path = "/sys/fs/cgroup/memory/memory.usage_in_bytes"
        with open(path, "r") as f:
            memoria = int(f.read()) / (1024 * 1024)
            return memoria
    except Exception:
        return 0.0

def leer_cpu_docker(inicio_cpu, inicio_tiempo):
    try:
        if CGROUP_V2:
            path = "/sys/fs/cgroup/cpu.stat"
            with open(path, "r") as f:
                lines = f.readlines()
                usage_usec = int([line for line in lines if "usage_usec" in line][0].split()[1])
        else:
            path = "/sys/fs/cgroup/cpuacct/cpuacct.usage"
            with open(path, "r") as f:
                usage_nsec = int(f.read())
                usage_usec = usage_nsec // 1000
        return (usage_usec - inicio_cpu) / ((time.time() - inicio_tiempo) * 1_000_000) * 100
    except Exception:
        return 0.0

def leer_cpu_inicio():
    try:
        if CGROUP_V2:
            path = "/sys/fs/cgroup/cpu.stat"
            with open(path, "r") as f:
                lines = f.readlines()
                return int([line for line in lines if "usage_usec" in line][0].split()[1])
        else:
            path = "/sys/fs/cgroup/cpuacct/cpuacct.usage"
            with open(path, "r") as f:
                usage_nsec = int(f.read())
                return usage_nsec // 1000
    except Exception:
        return 0

def medir_recursos_durante(funcion_prueba):
    mem_antes = leer_memoria_docker()
    inicio_cpu = leer_cpu_inicio()
    inicio_tiempo = time.time()

    funcion_prueba()

    fin_cpu = leer_cpu_docker(inicio_cpu, inicio_tiempo)
    mem_despues = leer_memoria_docker()
    duracion = time.time() - inicio_tiempo

    mem_prom = (mem_antes + mem_despues) / 2
    return round(fin_cpu, 2), round(mem_prom, 2), round(duracion, 2)

# ---------- ESCENARIOS MEJORADOS ----------

def idle_test():
    time.sleep(10)

def cpu_stress():
    subprocess.run(["sysbench", "cpu", "--cpu-max-prime=20000", "--threads=1", "run"], stdout=subprocess.DEVNULL)

def cpu_multi():
    subprocess.run(["sysbench", "cpu", "--cpu-max-prime=20000", "--threads=4", "run"], stdout=subprocess.DEVNULL)

def memory_stress():
    subprocess.run(["sysbench", "memory", "--memory-total-size=5G", "--memory-block-size=1M", "--memory-oper=write", "--threads=1", "run"], stdout=subprocess.DEVNULL)

def memory_large():
    subprocess.run(["sysbench", "memory", "--memory-total-size=10G", "--memory-block-size=1M", "--memory-oper=write", "--threads=1", "run"], stdout=subprocess.DEVNULL)

def disk_write():
    subprocess.run("dd if=/dev/zero of=tempfile bs=1M count=512 oflag=dsync", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("tempfile")

def disk_read():
    if not os.path.exists("temp_readfile"):
        subprocess.run("dd if=/dev/urandom of=temp_readfile bs=1M count=512", shell=True, stdout=subprocess.DEVNULL)
    subprocess.run("dd if=temp_readfile of=/dev/null bs=1M iflag=direct", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("temp_readfile")

def network_download():
    subprocess.run("curl -L --no-cache -o /dev/null https://speed.hetzner.de/1GB.bin", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_spawn():
    try:
        for _ in range(100):
            subprocess.Popen(["true"])
    except Exception as e:
        print(f"⚠️ Error en process_spawn: {e}")

# ---------- CONFIGURACIÓN ----------

pruebas = {
    "idle": idle_test,
    "cpu_stress": cpu_stress,
    "cpu_multi": cpu_multi,
    "memory_stress": memory_stress,
    "memory_large": memory_large,
    "disk_write": disk_write,
    "disk_read": disk_read,
    "network_download": network_download,
    "process_spawn": process_spawn
}

source = "Docker"
json_output = {}
csv_path = os.path.join(results_dir, "docker_scenarios_results.csv")
csv_existe = os.path.exists(csv_path)

# ---------- EJECUCIÓN ----------

for nombre_prueba, funcion in pruebas.items():
    print(f"🐳 Ejecutando prueba: {nombre_prueba}")
    cpu, mem, tiempo = medir_recursos_durante(funcion)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    resultado = {
        "test_type": nombre_prueba,
        "cpu_percent": cpu,
        "memory_mb": mem,
        "execution_time_sec": tiempo,
        "source": source,
        "timestamp": timestamp
    }

    json_path = os.path.join(results_dir, f"docker_{nombre_prueba}_{timestamp}.json")
    with open(json_path, "w") as jf:
        json.dump(resultado, jf, indent=2)

    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not csv_existe:
            writer.writerow(["timestamp", "test_type", "cpu_percent", "memory_mb", "execution_time_sec", "source"])
            csv_existe = True
        writer.writerow([timestamp, nombre_prueba, cpu, mem, tiempo, source])

    print(f"✅ Prueba '{nombre_prueba}' completada.")

print("🏁 Todas las pruebas Docker han sido ejecutadas.")
