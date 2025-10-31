import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

load_dotenv()
api_key = os.getenv("apiKey")

PHANTOM_NAME = "Extract-Perfil-Linkedin"
BASE_URL = "https://api.phantombuster.com/api/v2/agents"
OUTPUT_PATH = Path("dataset/candidatos_linkedin_raw.json")
LOG_PATH = Path("dataset/phantom_log.txt")
os.makedirs(OUTPUT_PATH.parent, exist_ok=True)

headers = {"X-Phantombuster-Key-1": api_key}


def log(msg: str):

    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get_phantom_id():
    log(f"🔍 Buscando ID do Phantom '{PHANTOM_NAME}'...")
    r = requests.get(f"{BASE_URL}/fetch-all", headers=headers)
    r.raise_for_status()
    agents = r.json()
    if isinstance(agents, dict) and "data" in agents:
        agents = agents["data"]
    for agent in agents:
        if agent.get("name") == PHANTOM_NAME:
            log(f"✅ Encontrado Phantom ID: {agent['id']}")
            return agent["id"]
    raise ValueError(f"Phantom '{PHANTOM_NAME}' não encontrado na conta.")


def get_last_output(agent_id):

    url = f"{BASE_URL}/fetch-output"
    params = {"id": agent_id}

    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        log(f"Erro ao buscar último output: {r.text}")
        r.raise_for_status()

    data = r.json()
    output_data = data.get("output", {}) or data.get("data", {})
    if not output_data:
        log("Nenhum output disponível ainda.")
    else:
        size = len(json.dumps(output_data))
        log(f"Output mais recente recuperado ({size} bytes).")
    return output_data


def main():
    try:
        agent_id = get_phantom_id()
        result_data = get_last_output(agent_id)

        if not result_data:
            log("Nenhum dado retornado pelo Phantom.")
            return

        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        log(f"Dados salvos em: {OUTPUT_PATH}")
        log("Processo finalizado com sucesso.")

    except Exception as e:
        log(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
