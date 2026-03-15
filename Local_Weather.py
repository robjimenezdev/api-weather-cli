import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import locale
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        pass

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

print("=" * 60)
print("        CONSULTA DEL TIEMPO - PREVISION 5 DIAS")
print("=" * 60)
ciudad = input("\nIntroduce el nombre de la ciudad: ")

respuesta = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params={
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    }
)

if respuesta.status_code != 200:
    print(f"\n[ERROR] Ciudad no encontrada o problema con la API. Codigo: {respuesta.status_code}")
    exit()

datos = respuesta.json()

iconos = {
    "cielo claro":     "☀  Sol",
    "pocas nubes":     "⛅ Sol/Nub",
    "nubes dispersas": "🌤 Nublado",
    "muy nuboso":      "☁  Muy nub",
    "cielo cubierto":  "☁  Cubierto",
    "nubes":           "☁  Nubes",        # <-- añadida
    "nuboso":          "☁  Nuboso",       # <-- añadida
    "lluvia ligera":   "🌦 Lluvia",
    "lluvia moderada": "🌧 Lluvia++",
    "lluvia intensa":  "⛈  Tormenta",
    "nieve":           "❄  Nieve",
    "niebla":          "🌫 Niebla",
    "tormenta":        "⚡ Rayo",
    "llovizna":        "🌦 Llovizna",
}
def get_icono(descripcion):
    descripcion = descripcion.lower().strip()
    if descripcion in iconos:
        return iconos[descripcion]
    for clave, icono in iconos.items():
        if clave in descripcion:
            return icono
    return f"[{descripcion[:6].upper()}]"

def get_viento(velocidad):
    if velocidad < 2:
        return "Calma"
    elif velocidad < 6:
        return "Flojo"
    elif velocidad < 12:
        return "Moderado"
    elif velocidad < 20:
        return "Fuerte"
    else:
        return "Muy fuerte"

print(f"\n  CIUDAD   : {datos['city']['name']}, {datos['city']['country']}")
print(f"  POBLACION: {datos['city']['population']:,} habitantes")
print(f"  CONSULTA : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

dia_actual = ""

for item in datos["list"]:
    fecha_hora = datetime.fromtimestamp(item["dt"])
    dia = fecha_hora.strftime("%A %d/%m/%Y")
    hora = fecha_hora.strftime("%H:%M")
    temp = item["main"]["temp"]
    temp_min = item["main"]["temp_min"]
    temp_max = item["main"]["temp_max"]
    sensacion = item["main"]["feels_like"]
    descripcion = item["weather"][0]["description"]
    viento = item["wind"]["speed"]
    humedad = item["main"]["humidity"]
    icono = get_icono(descripcion)
    estado_viento = get_viento(viento)

    if dia != dia_actual:
        dia_actual = dia
        print(f"\n  +{'='*58}+")
        print(f"  |  {dia.upper():<56}|")
        print(f"  +{'='*58}+")
        print(f"  | {'HORA':<6} {'ICONO':<11} {'TEMP':>6} {'SENS':>6} {'MIN':>6} {'MAX':>6} {'HUM':>5} {'VIENTO':<10}|")
        print(f"  +{'-'*58}+")

    print(f"  | {hora:<6} {icono:<11} {temp:>5.1f}C {sensacion:>5.1f}C {temp_min:>5.1f}C {temp_max:>5.1f}C {humedad:>4}% {estado_viento:<10}|")

print(f"\n  +{'='*58}+")
print(f"  |{'FIN DE LA PREVISION':^60}|")
print(f"  +{'='*58}+\n")