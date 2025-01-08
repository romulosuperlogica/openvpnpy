import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
import subprocess
from datetime import datetime

# Caminho para o arquivo JSON que armazenará o caminho do .ovpn
CONFIG_FILE = 'openvpn_config.json'
# Diretório onde os arquivos .ovpn importados serão armazenados
OVPN_DIR = 'ovpn_configs'

# Certifique-se de que o diretório de configuração existe
if not os.path.exists(OVPN_DIR):
    os.makedirs(OVPN_DIR)

# Função para carregar o arquivo JSON
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

# Função para salvar o caminho do arquivo .ovpn no JSON
def save_config(config_data):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config_data, file)

# Função para importar o arquivo .ovpn
def import_ovpn():
    file_path = filedialog.askopenfilename(filetypes=[("OVPN files", "*.ovpn")])
    if file_path:
        # Copia o arquivo para o diretório do projeto
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(OVPN_DIR, file_name)
        shutil.copy(file_path, dest_path)

        # Salva o caminho no arquivo de configuração
        config_data['ovpn_file'] = dest_path
        save_config(config_data)
        update_status()

# Função para atualizar o status do arquivo importado
def update_status():
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Lista as sessões OpenVPN ativas
    result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True)
    output = result.stdout.decode('utf-8')

    # Procura pelo caminho da sessão ativa
    session_path = None
    for line in output.splitlines():
        if 'Path: ' in line:
            session_path = line.split('Path: ')[1].strip()
            break

    if session_path:
        vpn_status_label.config(text=f"Conectado")
        vpn_status_canvas.itemconfig(vpn_status, fill="green")
    else:
        vpn_status_label.config(text=f"Desconectado")
        vpn_status_canvas.itemconfig(vpn_status, fill="red")
    
    ovpn_file = config_data.get('ovpn_file')
    if ovpn_file:
        # status_label.config(text=f"Arquivo importado: {os.path.basename(ovpn_file)}")
        vpn_status_check.config(text=f"Ultima verificação em {data_atual}")
        arquivo_importado_status.config(text=f"Arquivo .OVPN importado")
    else:
        vpn_status_check.config(text=f"Necessario importar o arquivo .OVPN")
        arquivo_importado_status.config(text="Nenhum arquivo .OVPN importado")

    root.after(300000, update_status)  # Faz a checagem a 5 minutos

# Função para conectar usando o arquivo OVPN importado
def connect_vpn():
    ovpn_file = config_data.get('ovpn_file')
    if ovpn_file:
        try:
            # Lista as sessões OpenVPN ativas
            result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True)
            output = result.stdout.decode('utf-8')

            # Procura pelo caminho da sessão ativa
            session_path = None
            for line in output.splitlines():
                if 'Path: ' in line:
                    session_path = line.split('Path: ')[1].strip()
                    break

            if session_path:
                # Desconecta a sessão ativa
                subprocess.run(['openvpn3', 'session-manage', '--session-path', session_path, '--disconnect'], check=True)

            # Conecta à VPN usando o arquivo .ovpn
            subprocess.run(['openvpn3', 'session-start', '--config', ovpn_file], check=True)
            update_status()
            vpn_status_label.config(text=f"Conectado")
        except subprocess.CalledProcessError:
            vpn_status_check.config(text=f"Falha ao conectar à VPN")
            # messagebox.showerror("Erro", "Falha ao conectar à VPN.")
    # else:
    #     vpn_status_check.config(text=f"Nenhum arquivo OVPN importado")
        # messagebox.showwarning("Aviso", "Nenhum arquivo OVPN importado.")

# Função para desconectar a VPN
def disconnect_vpn():
    try:
        # Lista as sessões OpenVPN ativas
        result = subprocess.run(['openvpn3', 'sessions-list'], stdout=subprocess.PIPE, check=True)
        output = result.stdout.decode('utf-8')

        # Procura pelo caminho da sessão ativa
        session_path = None
        for line in output.splitlines():
            if 'Path: ' in line:
                session_path = line.split('Path: ')[1].strip()
                break

        if session_path:
            # Desconecta a sessão ativa
            subprocess.run(['openvpn3', 'session-manage', '--session-path', session_path, '--disconnect'], check=True)
            # messagebox.showinfo("Desconectado", "Desconectado da VPN com sucesso.")
            # vpn_status_check.config(text=f"Desconectado da VPN com sucesso.")
            update_status()
            vpn_status_label.config(text=f"Desconectado")
        else:
            # messagebox.showinfo("Desconectado", "Nenhuma sessão VPN ativa encontrada.")
            vpn_status_check.config(text=f"Nenhuma sessão VPN ativa encontrada")
    except subprocess.CalledProcessError:
        # messagebox.showerror("Erro", "Falha ao desconectar da VPN.")
        vpn_status_check.config(text=f"Falha ao desconectar da VPN")

# Carregar a configuração ao iniciar
config_data = load_config()

# Criar a interface gráfica
root = tk.Tk()
root.title("OPENVPNPY")
root.geometry('400x600')

# Label para mostrar o status do arquivo importado
vpn_status_title = tk.Label(
    root,
    text="Status VPN",
    font=(
        "Helvetica",
        14,
        "bold"
    )
)
vpn_status_title.pack(pady=10)

# Canvas para mostrar o status da VPN
vpn_status_canvas = tk.Canvas(root, width=50, height=50)
vpn_status = vpn_status_canvas.create_oval(10, 10, 30, 30, fill="red")  # Vermelho indica desconectado
vpn_status_canvas.pack(pady=10)

# Label de status VPN
vpn_status_label = tk.Label(root, text="")
vpn_status_label.pack(pady=10)

# Dica de checagem automatica VPN
vpn_status_check = tk.Label(root, text="")
vpn_status_check.pack(pady=10)

# Dica de checagem automatica VPN
vpn_status_dica = tk.Label(root, text="Checagem automatica a cada 5 minutos")
vpn_status_dica.pack(pady=10)

# Label Ações de conexão VPN
connections_label = tk.Label(
    root,
    text="Ações sobre a VPN",
    font=(
        "Helvetica",
        14,
        "bold"
    )
)
connections_label.pack(pady=5)

# Verificar status da VPN
vpn_status_button = tk.Button(root, text="Verificar Status", command=update_status)
vpn_status_button.pack(pady=10)

# Botão para conectar à VPN
connect_button = tk.Button(root, text="Conectar VPN", command=connect_vpn)
connect_button.pack(pady=10)

# Botão para desconectar da VPN
disconnect_button = tk.Button(root, text="Desconectar VPN", command=disconnect_vpn)
disconnect_button.pack(pady=10)

# Label de importação 
arquivo_importado_Label = tk.Label(
    root,
    text="Importação de arquivo",
    font=(
        "Helvetica",
        14,
        "bold"
    )
)
arquivo_importado_Label.pack(pady=10)

# Botão para importar o arquivo OVPN
import_button = tk.Button(root, text="Importar OVPN", command=import_ovpn)
import_button.pack(pady=10)

# Label para mostrar o status do arquivo importado
arquivo_importado_status = tk.Label(root, text="")
arquivo_importado_status.pack(pady=10)

# Atualiza o status ao iniciar o programa
update_status()

# Iniciar o loop da interface gráfica
root.mainloop()