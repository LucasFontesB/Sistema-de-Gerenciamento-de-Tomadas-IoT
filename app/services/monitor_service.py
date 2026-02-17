import threading
import time
from app.services.tuya_service import obter_status
from app.models.dispositivo_repository import listar_dispositivos
from app.core.status_manager import atualizar_status
from flask import current_app
import socket

def dispositivo_online(ip, porta=6668, timeout=0.3):
    try:
        with socket.create_connection((ip, porta), timeout=timeout):
            return True
    except (socket.timeout, OSError):
        return False


def monitorar(d, socket_timeout):
    print(f"🟢 Thread criada para dispositivo {d['id']}")

    while True:
        try:
            print(f"🔁 Loop ativo para {d['id']}")

            # 🚨 Primeiro teste rápido de IP
            if not dispositivo_online(d["ip"]):
                print(f"🚫 IP offline detectado para {d['id']}")
                atualizar_status(d["id"], "inativo")
                time.sleep(2)  # resposta rápida
                continue

            # 🔎 Só chama Tuya se IP estiver vivo
            status = obter_status(d, socket_timeout)

            print(f"📡 Status obtido: {status}")

            atualizar_status(d["id"], status)

            time.sleep(5)

        except Exception as e:
            print(f"💥 ERRO na thread {d['id']}: {e}")
            atualizar_status(d["id"], "inativo")
            time.sleep(2)

def iniciar_monitoramento_automatico(app):
    print("🔥 Monitoramento iniciado")

    with app.app_context():
        dispositivos = listar_dispositivos()
        socket_timeout = app.config["SOCKET_TIMEOUT"]

    for d in dispositivos:
        threading.Thread(
            target=monitorar,
            args=(d, socket_timeout),
            daemon=True
        ).start()