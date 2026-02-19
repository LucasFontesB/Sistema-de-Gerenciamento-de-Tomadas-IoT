from flask import Blueprint, render_template
from app.services import consumo_service
from app.models.dispositivo_repository import listar_dispositivos

energia_bp = Blueprint("energia", __name__)

@energia_bp.route("/relatorioEnergia")
def relatorio_energia():

    dispositivos = listar_dispositivos()
    dados = []

    total_kwh = 0
    tarifa = 0.95

    for d in dispositivos:
        kwh = consumo_service.consumo_diario(d["id"])
        kwh = float(kwh or 0)

        custo = kwh * tarifa

        total_kwh += kwh

        dados.append({
            "apartamento": d["apartamento"],
            "kwh": kwh,
            "custo": custo
        })

    total_custo = total_kwh * tarifa

    return render_template(
        "relatorioEnergia.html",
        dados=dados,
        total_kwh=total_kwh,
        total_custo=total_custo
    )