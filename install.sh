#!/bin/bash

SOURCE_PYTHON_SCRIPT="./openvpnpy.py"
DESKTOP_FILE="/usr/share/applications/openvpnpy.desktop"
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

# Tornar o arquivo Python executável
echo "Tornando o script Python executável..."
sudo chmod +x "$SOURCE_PYTHON_SCRIPT"

# Criar o arquivo .desktop
echo "Criando atalho .desktop em $DESKTOP_FILE..."
sudo bash -c "cat > $DESKTOP_FILE <<EOF
[Desktop Entry]
Name=OpenVPNPY
Exec=python3 $PWD/openvpnpy.py > /dev/null 2>&1
Icon=$PWD/openvpn.ico
Terminal=false
Type=Application
Categories=Utility;
EOF"

# Garantir que o arquivo .desktop tenha permissões de execução
echo "Tornando o arquivo .desktop executável..."
sudo chmod +x "$DESKTOP_FILE"

# Finalização
echo "Instalação concluída!"
echo "O arquivo Python foi copiado para /usr/local/bin/ e o atalho foi criado em /usr/share/applications/."
echo "Você pode agora encontrar o atalho para o script no menu de aplicações ou em outras interfaces gráficas."
