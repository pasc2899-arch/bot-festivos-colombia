import requests
import datetime

TOKEN = "TU_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"

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
    hoy = datetime.date.today()
    festivos = obtener_festivos()

    for festivo in festivos:
        fecha_festivo = datetime.datetime.strptime(festivo["date"], "%Y-%m-%d").date()
        if (fecha_festivo - hoy).days == 1:
            nombre = festivo["localName"]
            enviar_mensaje(f"⏰ En 1 día es festivo: {nombre} — {fecha_festivo}")

if __name__ == "__main__":
    verificar_festivos()
