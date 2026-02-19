import threading
import time

import tinytuya

from app.services import consumo_service
from app.services.tuya_service import obter_status
from app.models.dispositivo_repository import listar_dispositivos, buscar_por_id
from app.core.status_manager import atualizar_status
import socket

def dispositivo_online(ip, porta=6668, timeout=0.3):
    try:
        with socket.create_connection((ip, porta), timeout=timeout):
            return True
    except (socket.timeout, OSError):
        return False


def monitorar(app, dispositivo_id, socket_timeout):

    print(f"🟢 Thread criada para dispositivo {dispositivo_id}")

    ultimo_registro_consumo = time.time()

    while True:
        try:
            # 🔥 Sempre buscar dados atualizados do banco
            with app.app_context():
                d = buscar_por_id(dispositivo_id)

            if not d:
                print(f"❌ Dispositivo {dispositivo_id} removido do banco")
                break

            print(f"🔁 Loop ativo para {dispositivo_id}")

            # 🔍 Verifica se IP responde
            if not dispositivo_online(d["ip"]):
                print(f"🚫 IP offline detectado para {dispositivo_id}")
                atualizar_status(dispositivo_id, "inativo")
                time.sleep(2)
                continue

            # 🔥 Criar device com dados atualizados
            device = tinytuya.Device(
                d["device_id"],
                d["ip"],
                d["local_key"]
            )
            device.set_version(d["version"])
            device.set_socketTimeout(socket_timeout)

            try:
                status_data = device.status()
            except Exception as e:
                print(f"❌ Falha ao comunicar com dispositivo: {e}")
                atualizar_status(dispositivo_id, "inativo")
                time.sleep(2)
                continue

            # 🔒 Valida retorno
            if not status_data:
                print("⚠️ Sem resposta do dispositivo")
                atualizar_status(dispositivo_id, "inativo")
                time.sleep(2)
                continue

            if "Error" in status_data:
                print("❌ Erro de autenticação ou dispositivo inválido")
                atualizar_status(dispositivo_id, "inativo")
                time.sleep(2)
                continue

            if "dps" not in status_data:
                print("⚠️ Resposta sem DPS")
                atualizar_status(dispositivo_id, "inativo")
                time.sleep(2)
                continue

            # 🔄 Atualiza status
            status = "ligado" if status_data["dps"].get("1", False) else "desligado"
            print(f"📡 Status obtido: {status}")
            atualizar_status(dispositivo_id, status)

            # ⚡ Controle de consumo
            agora = time.time()

            if agora - ultimo_registro_consumo >= 30:
                with app.app_context():
                    consumo_service.processar_consumo(dispositivo_id, status_data)

                ultimo_registro_consumo = agora

            time.sleep(5)

        except Exception as e:
            print(f"💥 ERRO na thread {dispositivo_id}: {e}")
            atualizar_status(dispositivo_id, "inativo")
            time.sleep(2)

def iniciar_monitoramento_automatico(app):
    print("🔥 Monitoramento iniciado")

    with app.app_context():
        dispositivos = listar_dispositivos()
        socket_timeout = app.config["SOCKET_TIMEOUT"]

    for d in dispositivos:
        threading.Thread(
            target=monitorar,
            args=(app, d["id"], socket_timeout),
            daemon=True
        ).start()