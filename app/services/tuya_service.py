import tinytuya

def criar_device(d, socket_timeout):
    device = tinytuya.OutletDevice(
        d["device_id"],
        d["ip"],
        d["local_key"]
    )
    device.set_version(d["version"])
    device.set_socketTimeout(socket_timeout)
    return device


def ligar(d, socket_timeout):
    device = criar_device(d, socket_timeout)
    device.turn_on()


def desligar(d, socket_timeout):
    device = criar_device(d, socket_timeout)
    device.turn_off()


def obter_status(d, socket_timeout):
    device = criar_device(d, socket_timeout)
    data = device.status()

    if "dps" in data:
        return "ligado" if data["dps"].get("1", False) else "desligado"

    return "inativo"