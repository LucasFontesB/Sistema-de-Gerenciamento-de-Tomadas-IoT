import sqlite3
from flask import current_app
import datetime


def consumo_diario(dispositivo_id):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(energia_kwh)
            FROM consumo
            WHERE dispositivo_id = ?
            AND DATE(timestamp) = DATE('now')
        """, (dispositivo_id,))

        resultado = cursor.fetchone()[0]

    return float(resultado or 0)


def consumo_diario(dispositivo_id):
    with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(energia_kwh)
            FROM consumo
            WHERE dispositivo_id = ?
            AND DATE(timestamp) = DATE('now')
        """, (dispositivo_id,))

        resultado = cursor.fetchone()[0]

    return float(resultado or 0)


def extrair_consumo(status_data):
    print("\n⚡ [CONSUMO] Iniciando extração de dados...")

    dps = status_data.get("dps", {})
    print(f"🔍 DPS recebido: {dps}")

    try:
        potencia_raw = dps.get("18", 0)
        corrente_raw = dps.get("19", 0)
        tensao_raw = dps.get("20", 0)

        print(f"📥 Valores brutos -> Potência: {potencia_raw}, Corrente: {corrente_raw}, Tensão: {tensao_raw}")

        potencia = potencia_raw / 10
        corrente = corrente_raw
        tensao = tensao_raw / 10

        print(f"📊 Valores convertidos -> Potência: {potencia}W | Corrente: {corrente}mA | Tensão: {tensao}V")

        return potencia, corrente, tensao

    except Exception as e:
        print(f"💥 [ERRO EXTRAÇÃO] {e}")
        return 0, 0, 0


def salvar_consumo(dispositivo_id, potencia, corrente, tensao):
    INTERVALO_SEGUNDOS = 30
    print(f"💾 [BANCO] Salvando consumo do dispositivo {dispositivo_id}...")
    energia_kwh = (potencia * (INTERVALO_SEGUNDOS / 3600)) / 1000

    try:
        with sqlite3.connect(current_app.config["DB_PATH"]) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consumo (dispositivo_id, potencia, corrente, tensao, energia_kwh)
                VALUES (?, ?, ?, ?, ?)
            """, (dispositivo_id, potencia, corrente, tensao, energia_kwh))
            conn.commit()

        print(f"✅ [BANCO] Registro salvo com sucesso! "
              f"({datetime.datetime.now()})")

    except Exception as e:
        print(f"💥 [ERRO BANCO] Falha ao salvar consumo: {e}")


def processar_consumo(dispositivo_id, status_data):
    print(f"\n🚀 [PROCESSAMENTO] Dispositivo {dispositivo_id}")

    potencia, corrente, tensao = extrair_consumo(status_data)

    if potencia > 0:
        print("⚡ Potência maior que zero, registrando consumo...")
        salvar_consumo(dispositivo_id, potencia, corrente, tensao)
    else:
        print("🟡 Potência zero, registro ignorado.")