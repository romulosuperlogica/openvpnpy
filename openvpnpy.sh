#!/bin/bash

VENV_DIR="./venv"

echo "Iniciando configuração..."

echo "Verificando dependências do sistema..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip python3-tk openvpn3

if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv "$VENV_DIR"
fi

echo "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

echo "Instalando dependências do Python..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "Executando o script OPENVPNPY..."
    "$VENV_DIR/bin/python" vpn_ui.py
