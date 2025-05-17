#!/bin/bash
echo "🚀 Setting up environment for benchmarking..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip sysbench docker.io git curl procps
if command -v pip3 >/dev/null 2>&1; then
    pip3 install --upgrade pip
    pip3 install jupyter matplotlib psutil
else
    echo "❌ Error: pip3 no está disponible incluso después de la instalación."
    exit 1
fi
if ! getent group docker > /dev/null 2>&1; then
    sudo groupadd docker
fi
sudo usermod -aG docker $USER
echo "✅ Setup complete! Please restart your VM for Docker permissions to take effect."
echo "➡️ To start Jupyter, run: jupyter notebook"
