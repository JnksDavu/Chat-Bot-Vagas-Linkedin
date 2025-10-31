import re
import requests
import json
from pathlib import Path

RAW_PATH = Path("dataset/candidatos_linkedin_raw.json")
OUTPUT_PATH = Path("dataset/candidatos_linkedin.json")

raw_text = RAW_PATH.read_text(encoding="utf-8")

match = re.search(r"https://phantombuster\.s3\.amazonaws\.com/[^\s]+result\.json", raw_text)
if not match:
    print("Nenhum link JSON encontrado no log do Phantom.")
else:
    json_url = match.group(0)

    r = requests.get(json_url)
    r.raise_for_status()

    data = r.json()

    OUTPUT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
