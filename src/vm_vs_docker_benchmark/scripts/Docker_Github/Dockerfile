FROM python:3.11-slim

# Instalar utilidades del sistema necesarias
RUN apt-get update && \
    apt-get install -y stress-ng curl && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear carpeta de trabajo
WORKDIR /app

# Copiar el código fuente al contenedor
COPY . .

# Crear la carpeta de resultados por si no existe
RUN mkdir -p results

# Comando por defecto al iniciar el contenedor
CMD ["python", "benchmark.py"]
