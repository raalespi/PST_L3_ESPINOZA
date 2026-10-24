from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led

def calcular_promedio_lecturas(n: int):
    if not store.lecturas:
        return None

    ultimas = store.lecturas[-n:]
    cantidad = len(ultimas)
    temps = [
        l.temperatura if hasattr(l, "temperatura") else l["temperatura"]
        for l in ultimas
    ]
    hums = [
        l.humedad if hasattr(l, "humedad") else l["humedad"]
        for l in ultimas
    ]
    return {
        "cantidad": cantidad,
        "temperatura_promedio": round(sum(temps) / cantidad, 2),
        "humedad_promedio": round(sum(hums) / cantidad, 2)
    }