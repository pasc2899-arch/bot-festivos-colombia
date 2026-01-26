import requests
import datetime
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PAISES = {
    "CO": "🇨🇴 Colombia",
    "US": "🇺🇸 Estados Unidos",
    "AE": "🇦🇪 Emiratos Árabes Unidos"
}

def obtener_festivos(codigo_pais):
    año = datetime.date.today().year
    url = f"https://date.nager.at/api/v3/PublicHolidays/{año}/{codigo_pais}"

    resp = requests.get(url, timeout=10)

    if resp.status_code != 200:
        raise Exception(f"Error API {codigo_pais}: {resp.status_code}")

    try:
        return resp.json()
    except Exception:
        raise Exception(f"Respuesta no válida para {codigo_pais}: {resp.text}")

def enviar_mensaje(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto
    }
    requests.post(url, data=payload)

def verificar_festivos():
    hoy = datetime.date.today()

    for codigo, nombre_pais in PAISES.items():
        festivos = obtener_festivos(codigo)

        for festivo in festivos:
            fecha_festivo = datetime.datetime.strptime(
                festivo["date"], "%Y-%m-%d"
            ).date()

            if (fecha_festivo - hoy).days == 3:
                nombre = festivo["localName"]
                enviar_mensaje(
                    f"⏰ In 3 days is holiday in {nombre_pais}\n"
                    f"📅 {fecha_festivo}\n"
                    f"🎉 {nombre}"
                )

if __name__ == "__main__":
    enviar_mensaje("✅ Bot ejecutado correctamente desde GitHub Actions")
    verificar_festivos()

          
if __name__ == "__main__":
    verificar_festivos()


