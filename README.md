Raziel Espinoza Vargas 
Paralelo 104

### Objetivo
Comprender e implementar la arquitectura modular por capas (rutas, esquemas, servicios y almacenamiento en memoria) de una API REST utilizando FastAPI para la captura de telemetría de sensores y control de actuadores en dispositivos IoT (ESP8266).

# Lab 3 Estructura de un backend

Código base del curso para leer, ejecutar y modificar a mano, sin IA.
Hardware de referencia: NodeMCU ESP8266, DHT11 y LED RGB de cátodo común.
Este proyecto es una propuesta de material base para acompañar la guía.

## Backend en Windows
Desde backend, en una terminal Command Prompt de VS Code:
```
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Swagger: http://127.0.0.1:8000/docs
En macOS/Linux: python3 -m venv .venv y usar .venv/bin/python.
Los cinco endpoints base están en app/routes.py. La lista guarda como máximo
100 lecturas en memoria y se pierde al reiniciar. Ejecutar un solo proceso.
POST /lecturas retorna HTTP 201 con {"lectura": {...}, "led": "apagado"}.
PUT /led acepta rojo, verde, azul o apagado. No hay autenticación:
utilizar únicamente en la red de laboratorio autorizada.

## Firmware
Abrir firmware con PlatformIO IDE en VS Code. Copiar include/config.example.h
a include/config.h y completar WiFi, URL con IPv4 del PC e identificador.
Build, Upload y Monitor a 115200 baudios. El ESP envía cada 5 segundos y aplica
el color devuelto por POST /lecturas; PUT /led se refleja en el próximo envío.
Conexiones y pruebas: ver guía. Las dependencias se descargan la primera vez.
No publicar config.h, contraseñas ni tokens.

## Reto
Implementar GET /lecturas/promedio?n=3 a mano; no se incluye la solución.
Devolver cantidad, temperatura_promedio y humedad_promedio (dos decimales).
Validar n de 1 a 100; sin lecturas responder 404; si hay menos de n, usar todas.

## Respuesta a las preguntas dadas

# Pregunta 1: ¿Qué función recibe el JSON y cuál lo guarda?
La función que recibe es la función post que se encarga de leer las entradas en routes.py y la que lo guarda es guardar lecturas en services.py

# Pregunta 2: ¿Qué archivo cambiarías para añadir una URL?
Cambiaría el routes.py y si queremos darle lógica usamos services.py.

# Pregunta 3: ¿Qué ocurre con las lecturas y el color cuando se reinicia la API? ¿Por qué?
Al reiniciar la API los datos se reinician a sus valores iniciales, esto es debido a que están guardados en memoria en store.py por lo que se pierden al reiniciar.

# Pregunta 4: ¿Por qué una petición con JSON bien escrito puede devolver 422? Indica qué archivo define esa validación.
No cumplió con las validaciones realizadas en el archivo schemas.py y no se agrega pues al ser validado no se registra en los datos.

# Pregunta 5: Explica el recorrido completo de una lectura: ESP8266, ruta, modelo, servicio, almacenamiento y respuesta. ¿En qué momento cambia el LED?
El recorrido inicia cuando el ESP8266 captura las variables físicas mediante sus sensores, arma el payload JSON y realiza una petición HTTP POST /lecturas hacia el backend; al recibirla, la ruta intercepta la solicitud y transfiere los datos al modelo para validar los tipos de datos y rangos permitidos, retornando 422 si no son válidos; una vez validada, pasa al servicio, donde se aplica la lógica de negocio que evalúa los umbrales de temperatura y humedad para determinar el nuevo color del actuador, momento exacto en el que cambia el LED; finalmente, los datos se guardan en el almacenamiento y el servidor devuelve al ESP8266 una respuesta HTTP 201 Created con la confirmación de la lectura registrada y el estado resultante del actuador.



Evidencias
## Registro de Pruebas de la API
| N.° | Método | Ruta | Código Esperado | Código Obtenido | Descripción / Caso de Prueba |
|:---:|:---:|:---|:---:|:---:|:---|
| 1 | `GET` `/salud` | 200 | 200 | Verificación del estado del servicio (`{"estado": "ok"}`) |
| 2 | `GET` `/lecturas` | 200 | 200 | Consulta inicial de lecturas registradas (lista vacía `[]`) |
| 3 | `GET` `/led` | 200 | 200 | Consulta del estado actual del actuador LED (`apagado`) |
| 4 | `PUT` `/led` | 200 | 200 | Actualización exitosa del estado del LED (`"color": "verde"`) |
| 5 | `POST` `/lecturas` | 201 | 201 | Registro exitoso de telemetría de sensores (temperatura y humedad) |
| 6 | `GET` `/led` | 200 | 200 | Verificación del estado del actuador LED tras eventos previos |
| 7 | `POST` `/lecturas` | 422 | 422 | Error de validación: valor de humedad fuera del rango permitido (> 100) |
| 8 | `PUT` `/led` | 422 | 422 | Error de validación: valor de color no permitido (literal inválido) |

### Parte 5: Modificación del endpoint /salud
* **Archivo modificado:** `app/routes.py` (función manejadora de la ruta `GET /salud`).
* **Cambio en la respuesta:** Se añadió el campo `"laboratorio": 3` al objeto JSON de retorno, manteniendo intacto el campo `"estado": "ok"`. La respuesta pasó de ser `{"estado": "ok"}` a `{"estado": "ok", "laboratorio": 3}` con código de estado HTTP 200.

## Reto: Pruebas del endpoint GET /lecturas/promedio

### Datos de prueba registrados (equipo01)
* **Lectura 1:** Temperatura = 20 , Humedad = 40 
* **Lectura 2:** Temperatura = 24 , Humedad = 50 
* **Lectura 3:** Temperatura = 28 , Humedad = 60 

| Consulta | Código Esperado | Código Obtenido | Cuerpo de Respuesta Obtenido |
| Sin lecturas previas (`?n=3`) | 404 | 404 | `{"detail": "No hay lecturas registradas para calcular el promedio."}` |
| `?n=3` | 200 | 200 | `{"cantidad": 3, "temperatura_promedio": 24.0, "humedad_promedio": 50.0}` |
| `?n=2` | 200 | 200 | `{"cantidad": 2, "temperatura_promedio": 26.0, "humedad_promedio": 55.0}` |
| `?n=5` | 200 | 200 | `{"cantidad": 3, "temperatura_promedio": 24.0, "humedad_promedio": 50.0}` |
| `?n=0` | 422 | 422 | Error de validación (el valor debe ser mayor o igual a 1) |
| `?n=101` | 422 | 422 | Error de validación (el valor debe ser menor o igual a 100) |
| Sin indicar `n` | 200 | 200 | `{"cantidad": 3, "temperatura_promedio": 24.0, "humedad_promedio": 50.0}` |

### Cálculos de verificación:
* **Para n=3 (o sin indicar n):**
  * Cantidad usada: 3 lecturas
  * Temperatura promedio: $(20 + 24 + 28) / 3 = 72 / 3 = 24.0$
  * Humedad promedio: $(40 + 50 + 60) / 3 = 150 / 3 = 50.0$
* **Para n=2:**
  * Cantidad usada: 2 últimas lecturas 
  * Temperatura promedio: $(24 + 28) / 2 = 52 / 2 = 26.0$
  * Humedad promedio: $(50 + 60) / 2 = 110 / 2 = 55.0$
* **Para n=5:**
  * Cantidad usada: 3 disponibles
  * Temperatura promedio: $(20 + 24 + 28) / 3 = 24.0$
  * Humedad promedio: $(40 + 50 + 60) / 3 = 50.0$


  