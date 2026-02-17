import threading

status_cache = {}
status_lock = threading.Lock()

def atualizar_status(id, status):
    with status_lock:
        status_cache[id] = status

def obter_status(id):
    with status_lock:
        return status_cache.get(id, "inativo")

def obter_todos():
    with status_lock:
        return dict(status_cache)