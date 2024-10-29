#!/bin/bash

# Actualiza el índice de paquetes
sudo apt update

# Instala paquetes necesarios para Docker
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Agrega la clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Agrega el repositorio de Docker
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Actualiza el índice de paquetes nuevamente
sudo apt update

# Instala Docker
sudo apt install -y docker-ce

# Instala Python y pip
sudo apt install -y python3 python3-pip

# Verifica las instalaciones
docker --version
python3 --version
