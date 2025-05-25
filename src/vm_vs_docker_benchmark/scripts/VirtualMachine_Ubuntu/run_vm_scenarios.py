import subprocess
import psutil
import time
import json
import os
import csv
from datetime import datetime

results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../results"))
os.makedirs(results_dir, exist_ok=True)

def medir_recursos_durante(funcion_prueba, duracion_estimada=10):
    cpu_antes = psutil.cpu_percent(interval=1)
    mem_antes = psutil.virtual_memory().percent
    inicio = time.time()
    
    funcion_prueba()
    
    fin = time.time()
    cpu_despues = psutil.cpu_percent(interval=1)
    mem_despues = psutil.virtual_memory().percent
    
    cpu_prom = (cpu_antes + cpu_despues) / 2
    mem_prom = (mem_antes + mem_despues) / 2
    duracion = fin - inicio

    return cpu_prom, mem_prom, duracion

# ---------- Escenarios de prueba ----------

def idle_test():
    time.sleep(10)  # 10 segundos sin hacer nada

def cpu_stress():
    subprocess.run(["sysbench", "cpu", "--cpu-max-prime=20000", "--threads=1", "run"], stdout=subprocess.DEVNULL)

def memory_stress():
    subprocess.run(["sysbench", "memory", "--memory-total-size=5G", "run"], stdout=subprocess.DEVNULL)

def disk_write():
    subprocess.run("dd if=/dev/zero of=tempfile bs=1M count=512 oflag=dsync", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("tempfile")

# ---------- Lista de pruebas ----------

pruebas = {
    "idle": idle_test,
    "cpu_stress": cpu_stress,
    "memory_stress": memory_stress,
    "disk_write": disk_write
}

source = "VM"
timestamp_global = datetime.now().strftime("%Y%m%d_%H%M%S")
json_output = {}
csv_path = os.path.join(results_dir, "vm_scenarios_results.csv")
csv_existe = os.path.exists(csv_path)

for nombre_prueba, funcion in pruebas.items():
    print(f"🚀 Ejecutando prueba: {nombre_prueba}")
    cpu, mem, tiempo = medir_recursos_durante(funcion)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    resultado = {
        "test_type": nombre_prueba,
        "cpu_percent": round(cpu, 2),
        "memory_percent": round(mem, 2),
        "execution_time_sec": round(tiempo, 2),
        "source": source,
        "timestamp": timestamp
    }

    # Guardar en JSON individual
    json_path = os.path.join(results_dir, f"vm_{nombre_prueba}_{timestamp}.json")
    with open(json_path, "w") as jf:
        json.dump(resultado, jf, indent=2)

    # Añadir al CSV
    with open(csv_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not csv_existe:
            writer.writerow(["timestamp", "test_type", "cpu_percent", "memory_percent", "execution_time_sec", "source"])
            csv_existe = True
        writer.writerow([timestamp, nombre_prueba, cpu, mem, tiempo, source])

    print(f"✅ Prueba '{nombre_prueba}' completada. Resultado guardado.")

print("🏁 Todas las pruebas finalizadas.")
