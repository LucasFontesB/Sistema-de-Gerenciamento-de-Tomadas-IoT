import re
import ipaddress
from flask import flash

def validar_dispositivo(dados):
    erros = []

    # Campos obrigatórios
    campos = ["apartamento", "device_id", "local_key", "ip", "version"]
    for campo in campos:
        if not dados.get(campo) or not dados.get(campo).strip():
            erros.append(f"O campo {campo} não pode estar vazio.")

    # Validação de IP
    try:
        ipaddress.ip_address(dados["ip"])
    except ValueError:
        erros.append("IP inválido. Use formato como 192.168.0.10")

    # Validação de versão (formato X.X)
    if not re.fullmatch(r"\d\.\d", dados["version"]):
        erros.append("Versão inválida. Use formato como 3.3")

    return erros