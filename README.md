# 🧪 Comparativa de Rendimiento entre Máquinas Virtuales y Docker

Este repositorio contiene el código, scripts y análisis asociados a un trabajo de investigación cuyo objetivo es comparar el rendimiento de máquinas virtuales (VMs) y contenedores Docker en distintos escenarios prácticos. El estudio analiza el consumo de CPU, memoria y tiempos de ejecución en cada tecnología, con el fin de evaluar cuál ofrece mejor eficiencia en entornos controlados y reales.

---

## 📌 Objetivo del proyecto

Evaluar, de manera cuantitativa y reproducible, las diferencias de rendimiento entre máquinas virtuales y contenedores Docker ejecutando diversas cargas de trabajo. Para ello se diseñaron y ejecutaron pruebas de benchmarking automatizadas, recolectando datos clave sobre uso de recursos y tiempos de ejecución.

**Objetivos específicos:**

- Comparar el uso de CPU en tareas intensivas y ligeras.
- Medir el consumo máximo de memoria en distintos escenarios.
- Evaluar los tiempos de ejecución en pruebas controladas.
- Identificar fortalezas y debilidades de cada tecnología.

---

## ⚙️ Metodología

1. **Entornos controlados**: Todas las pruebas se realizaron en la misma máquina física (Intel Core i9-10900K, 16 GB RAM).
2. **Pruebas replicables**: Cada escenario se ejecutó 20 veces por entorno para asegurar estabilidad estadística.
3. **Automatización**: Se desarrollaron scripts en Python para lanzar las pruebas, recolectar métricas y exportar resultados en JSON.
4. **Análisis de datos**: Los resultados se visualizaron y analizaron usando Jupyter Notebooks con `pandas`, `matplotlib` y `seaborn`.

---

## 🧰 Herramientas utilizadas

### Hardware
- CPU: Intel Core i9-10900K
- RAM: 16 GB DDR4
- Sistema host: Windows 11

### Software
- Virtualización: VirtualBox (Ubuntu 25.04)
- Contenedores: Docker Engine
- Scripts: Python 3.11, Bash
- Métricas: `psutil`, `htop`, `perf`, `time`, `docker stats`
- Visualización: Jupyter Notebook, `matplotlib`, `seaborn`
- Editor de código: Visual Studio Code

---

## 📦 Estructura del repositorio

```
📁 vm_vs_docker_benchmark
├── 📁 notebooks
│   ├── 📄 docker_github_results_notebook.ipynb
│   ├── 📄 docker_vsc_results_notebook.ipy
│   ├── 📄 vm_ubuntu_results_notebook.ipynb
│   └── 📄 vm_windows10_results_notebook.ipynb
├── 📁 scripts
│   ├── 📁 VirtualMachine_Ubuntu
│   │   ├── 📄 run_vm_scenarios3.py
│   │   └── 📄 vm_setup.sh
│   ├── 📁 VirtualMachine_Windows10
│   │   ├── 📄 run_vm_scenarios.py
│   │   └── 📄 vm_setup.sh
│   ├── 📁 Docker_Github
│   │   ├── 📄 Dockerfile
│   │   ├── 📄 benchmark.py
│   │   └── 📄 requirements.txt
│   └── 📁 Docker_VisualStudioCode
│       ├── 📄 Dockerfile
│       ├── 📄 benchmark.py
│       └── 📄 requirements.txt
```

---

## 🧪 Pruebas realizadas

Cada script lanza múltiples escenarios de prueba, como:

- `idle`: sistema en reposo
- `cpu_stress`, `cpu_multi`: estrés de CPU (stress-ng)
- `memory_stress`, `memory_large`: uso intensivo de RAM
- `disk_read`, `disk_write`: operaciones con archivos grandes
- `network_download`: descarga vía `speedtest-cli`
- `process_spawn`: creación masiva de procesos

Las métricas se almacenan en JSON con información como:

- % de CPU usado
- Memoria máxima utilizada (MB)
- Tiempo total de ejecución (s)

Los resultados de cada entorno fueron los siguientes:

[GitHub codespaces Docker](src/vm_vs_docker_benchmark/notebooks/docker_github_results_notebook.ipynb)
[VisualStudio Code Docker](src/vm_vs_docker_benchmark/notebooks/docker_vsc_results_notebook.ipynb)
[Ubuntu en máquina virtual](src/vm_vs_docker_benchmark/notebooks/vm_ubuntu_results_notebook.ipynb)
[Windows 10 en máquina virtual](src/vm_vs_docker_benchmark/notebooks/vm_windows10_results_notebook.ipynb)

---

## 📊 Resultados destacados

### 🔧 Uso de CPU

- Docker demostró un uso más eficiente, especialmente en tareas ligeras como `idle` y `process_spawn`.
- VMs presentaron mayor consumo incluso en inactividad debido a su arquitectura más pesada.
- Docker sin restricciones (en VS Code) mostró menor uso medio de CPU, reflejando una ejecución más eficiente.

### 💾 Consumo de memoria

- Las VMs usaron más memoria incluso en reposo (30+ MB en algunos casos).
- Docker, en entornos como GitHub Codespaces, mantuvo un uso muy bajo excepto en pruebas forzadas (`memory_stress`).

### ⏱ Tiempo de ejecución

- Docker ejecutó pruebas significativamente más rápido en casi todos los escenarios.
- En `cpu_multi`, Docker tardó ~5 s, frente a >11 s en algunas VMs.
- En pruebas como `process_spawn`, Docker fue 4-5 veces más rápido.

---

## 🧩 Problemas encontrados

### En máquinas virtuales:

- **Gestión de dependencias**: fue necesario usar entornos virtuales (`venv`) por conflictos de paquetes.
- **Lectura de métricas incorrecta**: se descartó la primera muestra de `psutil.cpu_percent()` y se capturó la memoria máxima manualmente.

### En Docker:

- **Medición de memoria**: inicialmente incorrecta por limitaciones de visibilidad dentro del contenedor. Se ajustó para medir solo el uso pico real.

---

## 📈 Conclusiones

- Docker ofrece mejor rendimiento general, menor consumo de recursos y ejecución más rápida en la mayoría de los casos.
- Las máquinas virtuales presentan mayor sobrecarga, especialmente en Windows, pero ofrecen un mejor aislamiento del sistema.
- Para tareas de desarrollo, pruebas o despliegues donde el rendimiento es clave, Docker es preferible, siempre que el aislamiento completo no sea una necesidad.
- La elección entre Docker y VMs debe considerar el tipo de carga, la necesidad de aislamiento y la portabilidad deseada.

---

## 📚 Recursos empleados

- [Docker](https://www.docker.com/products/docker-desktop/)
- [VirtualBox](https://www.virtualbox.org)
- [Ubuntu](https://ubuntu.com/download/desktop)
- [Windows ISO](https://www.microsoft.com/es-es/software-download/windows10ISO)
- [Visual Studio Code](https://code.visualstudio.com)


