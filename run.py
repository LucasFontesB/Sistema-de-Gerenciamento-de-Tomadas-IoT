from app import init
from app.services.monitor_service import iniciar_monitoramento_automatico

app = init.create_app()

if __name__ == "__main__":

    with app.app_context():
        iniciar_monitoramento_automatico(app)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )