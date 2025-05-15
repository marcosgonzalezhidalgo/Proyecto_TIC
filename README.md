# Comparativa entre Máquinas Virtuales y Docker

## 📘 Descripción del proyecto

Este repositorio contiene una investigación detallada sobre las diferencias entre el uso de máquinas virtuales (VMs) y contenedores Docker en entornos de virtualización. El propósito principal es evaluar el rendimiento, consumo de recursos y tiempos de despliegue en distintos escenarios, con el fin de determinar cuál tecnología es más eficiente para ciertos tipos de tareas.

## 🎯 Objetivos

- Entender los principios de funcionamiento de las máquinas virtuales y Docker.
- Comparar el rendimiento de ambas tecnologías en distintos escenarios prácticos.
- Evaluar el uso de recursos como CPU, RAM, disco y tiempo de arranque.
- Documentar el proceso completo, incluyendo los scripts utilizados, para que otros puedan replicarlo.

## 🧱 Estructura del repositorio

```
comparativa-vm-vs-docker/
│
├── vm/
│ ├── setup_vm.sh
│ └── pruebas_vm.sh
│
├── docker/
│ ├── Dockerfile
│ ├── setup_docker.sh
│ └── pruebas_docker.sh
│
├── resultados/
│ ├── resultados_vm.txt
│ └── resultados_docker.txt
│
└── README.md
```


## 🧠 Metodología

### 1. Entorno de pruebas

Se realizaron pruebas en un mismo equipo anfitrión para asegurar igualdad de condiciones. Las especificaciones son las siguientes:

- **CPU:** Intel i9-10900K
- **RAM:** 16 GB
- **Sistema Operativo:** Windows 11 
- **Virtualización:** VirtualBox para VMs
- **Contenedores:** Docker 

### 2. Configuración

#### Máquina Virtual

- Se utilizó una imagen de Ubuntu 25.04.
- Recursos asignados: 4 CPU, 8 GB RAM.
- Instalación de dependencias y herramientas de prueba mediante `setup_vm.sh`.

#### Contenedor Docker

- Imagen base: `ubuntu:latest`
- Configuración de entorno y herramientas mediante `Dockerfile` y `setup_docker.sh`.

### 3. Pruebas inciales realizadas

Se realizaron pruebas idénticas en ambos entornos, ejecutadas mediante scripts automatizados:

- Tiempo de arranque.
- Consumo de CPU y RAM con `stress-ng`.
- Acceso a disco con operaciones de lectura/escritura.
- Instalación de paquetes y tiempos de respuesta.
- Simulación de tráfico de red con `iperf`.

### 4. Recolección de datos

Los datos fueron recolectados usando herramientas como:

- `time`
- `top`
- `htop`
- `vmstat`
- `iotop`
- `stress-ng`
- `iperf`

Los resultados se guardaron en la carpeta `/resultados`.

## 📊 Resultados y análisis

Los resultados detallados están en la carpeta `resultados/`. A continuación, un resumen de las observaciones:

| Métrica                  | VM                      | Docker                  |
|--------------------------|--------------------------|--------------------------|
| Tiempo de arranque       | Más lento (~25s)         | Muy rápido (~1s)         |
| Uso de RAM base          | Alto (~500 MB)           | Bajo (~50 MB)            |
| Rendimiento CPU          | Similar                  | Similar                  |
| Acceso a disco           | Más lento                | Más rápido               |
| Instalación de paquetes  | Más lenta                | Más rápida               |

**Conclusión preliminar:** Docker ofrece una solución más liviana y rápida para entornos aislados, mientras que las VMs proporcionan mayor aislamiento y compatibilidad de sistema completo.

## 🧪 Scripts

Los scripts de configuración y prueba están disponibles en las carpetas `vm/` y `docker/`. Cada script contiene comentarios para facilitar su comprensión y modificación.

## 📌 Consideraciones

- Las pruebas fueron realizadas en un entorno controlado. En producción, otros factores como seguridad, compatibilidad o persistencia pueden influir en la decisión entre usar VMs o contenedores.
- No se ha incluido orquestación (como Kubernetes) ni hipervisores de nivel empresarial (como VMware ESXi), pero podrían considerarse en futuras ampliaciones.

## 📚 Recursos empleados

- [Docker Documentation](https://docs.docker.com/)
- [VirtualBox Manual](https://www.virtualbox.org/manual/)
- [Linux Performance Tools](http://www.brendangregg.com/linuxperf.html)



