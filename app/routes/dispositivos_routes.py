from flask import Blueprint, jsonify, render_template, request, redirect, url_for, current_app, flash
from app.models.dispositivo_repository import (
    listar_dispositivos,
    buscar_por_id,
    inserir_dispositivo, deletar_dispositivo, atualizar_dispositivo
)
from app.services.tuya_service import ligar, desligar
from app.core.status_manager import obter_todos, atualizar_status
from app.services.monitor_service import monitorar
from app.utils.validacoes import validar_dispositivo
import threading

dispositivos_bp = Blueprint("dispositivos", __name__)

@dispositivos_bp.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    from flask import flash
    if request.method == "POST":

        erros = validar_dispositivo(request.form)

        if erros:
            for erro in erros:
                flash(erro, "error")
            return render_template("adicionar.html")

        novo_id = inserir_dispositivo(request.form)

        socket_timeout = current_app.config["SOCKET_TIMEOUT"]

        threading.Thread(
            target=monitorar,
            args=(current_app._get_current_object(), novo_id, socket_timeout),
            daemon=True
        ).start()

        flash("Dispositivo adicionado com sucesso!", "success")
        return redirect(url_for("dispositivos.home"))

    return render_template("adicionar.html", dados=request.form)

@dispositivos_bp.route("/")
def home():
    dispositivos = listar_dispositivos()
    return render_template("index.html", dispositivos=dispositivos)

@dispositivos_bp.route("/status_geral")
def status_geral():
    return jsonify(obter_todos())

@dispositivos_bp.route("/ligar/<int:id>")
def ligar_rota(id):
    d = buscar_por_id(id)
    socket_timeout = current_app.config["SOCKET_TIMEOUT"]

    ligar(d, socket_timeout)

    return jsonify({"ok": True, "status": "ligado"})

@dispositivos_bp.route("/desligar/<int:id>")
def desligar_rota(id):
    d = buscar_por_id(id)

    if not d:
        return jsonify({"ok": False}), 404

    socket_timeout = current_app.config["SOCKET_TIMEOUT"]

    desligar(d, socket_timeout)

    atualizar_status(id, "desligado")

    return jsonify({"ok": True, "status": "desligado"})

@dispositivos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    dispositivo = buscar_por_id(id)

    if request.method == "POST":
        atualizar_dispositivo(id, request.form)
        flash("Dispositivo atualizado!", "success")
        return redirect(url_for("dispositivos.home"))

    return render_template("editar.html", dispositivo=dispositivo)

@dispositivos_bp.route("/deletar/<int:id>")
def deletar(id):
    if deletar_dispositivo(id):
        flash("Dispositivo removido!", "success")
    else:
        flash("Dispositivo não encontrado.", "error")
    flash("Dispositivo removido!", "success")
    return redirect(url_for("dispositivos.home"))