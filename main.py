import requests
import time
from datetime import datetime

# Importa las estrategias como funciones
from strategy_1 import strategy_decision as strategy_1
from strategy_2 import strategy_decision as strategy_2
from strategy_3 import strategy_decision as strategy_3
from strategy_4 import strategy_decision as strategy_4
from strategy_5 import strategy_decision as strategy_5

BASE_URL = "https://demo-api-capital.backend-capital.com/"
API_KEY = "Nzng8d2eRXiX1Ho5"
IDENTIFIER = "jaimefarill@gmail.com"
PASSWORD = "Tulipan#8"
EPIC = "BTCUSD"
MONTOS_USD = [1000] * 5
last_request_time = 0

def send_debug(msg):
    print(f"{datetime.now().strftime('%H:%M:%S')} | {msg}")

def refresh_session():
    global last_request_time
    session_url = f"{BASE_URL}/api/v1/session"
    headers = {"X-CAP-API-KEY": API_KEY, "Content-Type": "application/json"}
    payload = {
        "identifier": IDENTIFIER,
        "password": PASSWORD,
        "encryptedPassword": False
    }
    time.sleep(max(0, 1 - (time.time() - last_request_time)))
    response = requests.post(session_url, headers=headers, json=payload)
    last_request_time = time.time()
    if response.status_code == 200:
        send_debug("[✅] Sesión iniciada correctamente")
        return {
            "CST": response.headers["CST"],
            "X-SECURITY-TOKEN": response.headers["X-SECURITY-TOKEN"]
        }
    else:
        send_debug(f"[❌] Error al iniciar sesión: {response.status_code} - {response.text}")
        return None

def list_available_accounts(headers):
    global last_request_time
    url = f"{BASE_URL}/api/v1/accounts"
    time.sleep(max(0, 1 - (time.time() - last_request_time)))
    response = requests.get(url, headers=headers)
    last_request_time = time.time()
    if response.status_code == 200:
        accounts = response.json().get("accounts", [])
        demo_accounts = []
        for acc in accounts:
            account_id = acc.get("accountId")
            account_name = acc.get("accountName", "")
            if account_name in ["1", "2", "3", "4", "5"]:
                demo_accounts.append(account_id)
        return demo_accounts
    else:
        send_debug(f"[❌] Error al listar cuentas: {response.status_code} - {response.text}")
        return []

def switch_to_demo_account(account_id, headers):
    global last_request_time
    url = f"{BASE_URL}/api/v1/session"
    payload = {"accountId": account_id}
    time.sleep(max(0, 1 - (time.time() - last_request_time)))
    response = requests.put(url, headers=headers, json=payload)
    last_request_time = time.time()
    if response.status_code == 200:
        send_debug(f"[✅] Cambiado a cuenta demo: {account_id}")
        return True
    elif response.status_code == 400 and "not-different" in response.text:
        send_debug(f"[ℹ️] La cuenta {account_id} ya está activa")
        return True
    else:
        send_debug(f"[❌] No se pudo cambiar a {account_id}: {response.status_code} - {response.text}")
        return False

def get_market_details(epic, headers):
    global last_request_time
    url = f"{BASE_URL}/api/v1/markets/{epic}"
    time.sleep(max(0, 1 - (time.time() - last_request_time)))
    response = requests.get(url, headers=headers)
    last_request_time = time.time()
    if response.status_code == 200:
        data = response.json()
        snapshot = data.get("snapshot", {})
        dealingRules = data.get("dealingRules", {})
        minDealSize = float(dealingRules["minDealSize"]["value"])
        minSizeIncrement = float(dealingRules["minSizeIncrement"]["value"])
        scaling_factor = float(data.get("scalingFactor", 1))
        ask = float(snapshot.get("offer"))
        return {
            "tradeable": snapshot.get("marketStatus") in ["TRADEABLE", "OPEN"],
            "ask": ask,
            "scalingFactor": scaling_factor,
            "minDealSize": minDealSize,
            "minSizeIncrement": minSizeIncrement
        }
    else:
        send_debug(f"[❌] No se pudo obtener datos del mercado ({epic}): {response.status_code} - {response.text}")
        return {"tradeable": False}

def round_to_increment(value, increment):
    return max(increment, round(value / increment) * increment)

def open_position(epic, size, direction, headers):
    global last_request_time
    payload = {
        "epic": epic,
        "direction": direction,
        "size": size,
        "orderType": "MARKET"
    }
    url = f"{BASE_URL}/api/v1/positions"
    time.sleep(max(0, 1 - (time.time() - last_request_time)))
    response = requests.post(url, headers=headers, json=payload)
    last_request_time = time.time()
    if response.status_code == 200:
        deal_ref = response.json().get("dealReference", "Desconocido")
        send_debug(f"[✅] Posición {direction} abierta en {epic} (size: {size}) | DealRef: {deal_ref}")
        return True
    else:
        send_debug(f"[❌] No se pudo abrir posición en {epic}: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    send_debug("[✅] Iniciando sesión...")
    session_tokens = refresh_session()
    if not session_tokens:
        send_debug("[❌] No se pudo iniciar sesión")
        exit()

    headers = {
        "X-CAP-API-KEY": API_KEY,
        "Content-Type": "application/json",
        "CST": session_tokens["CST"],
        "X-SECURITY-TOKEN": session_tokens["X-SECURITY-TOKEN"]
    }

    cuentas_demo = list_available_accounts(headers)
    if not cuentas_demo or len(cuentas_demo) < 5:
        send_debug("[⚠️] No se encontraron 5 cuentas demo.")
        exit()

    market = get_market_details(EPIC, headers)
    if not market["tradeable"]:
        send_debug(f"[⚠️] Mercado de {EPIC} no está abierto para trading.")
        exit()
    else:
        send_debug(f"[✅] Mercado {EPIC} abierto: Ask: {market['ask']}")

    ask = float(market['ask'])
    scaling = float(market['scalingFactor'])
    minDealSize = float(market['minDealSize'])
    minSizeIncrement = float(market['minSizeIncrement'])
    size = round_to_increment(1000 / (ask * scaling), minSizeIncrement)
    if size < minDealSize:
        send_debug(f"[❌] Size ({size}) menor que el mínimo permitido ({minDealSize}).")
        exit()

    # Asocia cada estrategia a cada cuenta
    strategies = [strategy_1, strategy_2, strategy_3, strategy_4, strategy_5]

    for i, account_id in enumerate(cuentas_demo):
        print(f"\n{'-'*35}\n[INFO] Trabajando en cuenta demo {i+1}: {account_id}\n{'-'*35}")
        if not switch_to_demo_account(account_id, headers):
            continue

        # Llama a la estrategia correspondiente para decidir la dirección
        direction, method_desc = strategies[i](ask)

        send_debug(f"[AI-{i+1}] Método: {method_desc} => Dirección: {direction}")

        exito = open_position(EPIC, size, direction, headers)
        if exito:
            send_debug(f"[✅] Trade {direction} abierto en demo {i+1} con 1000 USD (size: {size}) usando {method_desc}")
        else:
            send_debug(f"[❌] Trade falló en demo {i+1}")

        time.sleep(2)

    send_debug("¡Estrategias AI ejecutadas!")

