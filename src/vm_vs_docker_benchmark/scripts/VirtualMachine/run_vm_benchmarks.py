import subprocess
import psutil
import time
import json
import os
import csv
from datetime import datetime

# Crear carpeta results si no existe
results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../results"))
os.makedirs(results_dir, exist_ok=True)

# Timestamp para los nombres de archivo
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Comando de benchmark (CPU)
benchmark_cmd = ["sysbench", "cpu", "--cpu-max-prime=20000", "--threads=1", "run"]

# Medir CPU y RAM justo antes de ejecutar
cpu_before = psutil.cpu_percent(interval=1)
mem_before = psutil.virtual_memory().percent

# Ejecutar benchmark
start = time.time()
process = subprocess.run(benchmark_cmd, capture_output=True, text=True)
end = time.time()

# Medir CPU y RAM justo después
cpu_after = psutil.cpu_percent(interval=1)
mem_after = psutil.virtual_memory().percent

# Calcular promedios durante la ejecución (simplificado)
cpu_avg = (cpu_before + cpu_after) / 2
mem_avg = (mem_before + mem_after) / 2

# Resultado de sysbench
output = process.stdout

# Guardar resultados en JSON
result_json = {
    "benchmark_output": output,
    "metrics": {
        "cpu_percent": round(cpu_avg, 2),
        "memory_percent": round(mem_avg, 2),
        "execution_time_sec": round(end - start, 2)
    },
    "timestamp": timestamp
}

json_path = os.path.join(results_dir, f"vm_cpu_benchmark_{timestamp}.json")
with open(json_path, "w") as f:
    json.dump(result_json, f, indent=2)

print(f"✅ Resultado guardado en {json_path}")

# Guardar también en CSV para visualización fácil
csv_path = os.path.join(results_dir, "vm_benchmark_results.csv")
csv_exists = os.path.exists(csv_path)

with open(csv_path, "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    if not csv_exists:
        writer.writerow(["timestamp", "cpu_percent", "memory_percent", "execution_time_sec"])
    writer.writerow([timestamp, cpu_avg, mem_avg, round(end - start, 2)])

print(f"📄 También se guardó en formato CSV: {csv_path}")
