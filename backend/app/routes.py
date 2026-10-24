from fastapi import APIRouter, HTTPException, Query, status
from .schemas import LecturaEntrada, ComandoLED
from . import services

router = APIRouter()

@router.get("/salud")
def salud():
    return {
        "estado": "ok",
        "laboratorio": 3
    }

@router.get("/lecturas/promedio", status_code=status.HTTP_200_OK)
def obtener_promedio_lecturas(
    n: int = Query(default=3, ge=1, le=100, description="Número de últimas lecturas a promediar")
):
    resultado = services.calcular_promedio_lecturas(n)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay lecturas registradas para calcular el promedio."
        )

    return resultado

@router.get("/lecturas")
def get_lecturas():
    return services.listar_lecturas()

@router.post("/lecturas", status_code=201)
def post_lectura(datos: LecturaEntrada):
    return services.guardar_lectura(datos)

@router.get("/led")
def get_led():
    return services.consultar_led()

@router.put("/led")
def put_led(comando: ComandoLED):
    return services.cambiar_led(comando)