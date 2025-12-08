import requests
import datetime
import pytz
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Lista de países que deseas monitorear
PAISES = {
    "CO": "🇨🇴 Colombia",
    "US": "🇺🇸 Estados Unidos",
    "AE": "🇦🇪 Emiratos Árabes Unidos"
}

def obtener_festivos(pais):
    año = datetime.date.today().year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{año}/{pais}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": texto}
    requests.post(url, params=params)

def verificar_festivos():
    # Hora Colombia como referencia
    tz = pytz.timezone("America/Bogota")
    hoy = datetime.datetime.now(tz).date()

    for codigo, nombre_pais in PAISES.items():
        festivos = obtener_festivos(codigo)

        for festivo in festivos:
            fecha_festivo = datetime.datetime.strptime(festivo["date"], "%Y-%m-%d").date()
            nombre = festivo["localName"]

            # Notificación 3 días antes
            if (fecha_festivo - hoy).days == 3:
                enviar_mensaje(
                    f"⏰ In three days will be holiday in {nombre_pais}: *{nombre}* — {fecha_festivo}"
                )

            # Notificación el mismo día
            if fecha_festivo == hoy:
                enviar_mensaje(
                    f"🎉 Today is Holiday in {nombre_pais}: *{nombre}* — {fecha_festivo}"
                )

if __name__ == "__main__":
    verificar_festivos()


