import requests
import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def obtener_festivos():
    año = datetime.date.today().year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{año}/CO"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": texto}
    requests.post(url, params=params)

def verificar_festivos():
    # Obtener hora de Colombia
    tz = pytz.timezone("America/Bogota")
    hoy = datetime.datetime.now(tz).date()

    festivos = obtener_festivos()

    for festivo in festivos:
        fecha_festivo = datetime.datetime.strptime(festivo["date"], "%Y-%m-%d").date()

        # Si falta 1 día
        if (fecha_festivo - hoy).days == 1:
            nombre = festivo["localName"]
            enviar_mensaje(f"⏰ Tomorrow is holiday {nombre} — {fecha_festivo}")

        # Si hoy es festivo
        if fecha_festivo == hoy:
            nombre = festivo["localName"]
            enviar_mensaje(f"🎉 ¡Hoy es festivo en Colombia!: {nombre}")

if __name__ == "__main__":
    verificar_festivos()

