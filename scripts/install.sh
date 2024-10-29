#!/bin/bash

# Actualiza el índice de paquetes
sudo yum update -y

# Instala paquetes necesarios para Docker
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# Agrega el repositorio oficial de Docker
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Instala Docker
sudo yum install -y docker

# Inicia y habilita Docker
sudo systemctl start docker
sudo systemctl enable docker

# Agrega tu usuario al grupo docker (opcional, para evitar usar sudo con Docker)
sudo usermod -aG docker $USER

# Instala Python y pip
sudo yum install -y python3 python3-pip

# Verifica las instalaciones
docker --version
python3 --version
