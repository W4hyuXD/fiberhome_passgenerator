import re
import requests
import json
import socket
import csv
from datetime import datetime

HISTORY_FILE = "history.json"

def is_valid_ssid(ssid: str) -> bool:
    return re.fullmatch(r"fh_\\d{6}(_5G)?", ssid) is not None

def generate_passkey(ssid: str) -> str | None:
    url = f"https://fh-wlan.vercel.app/api/generate?ssid={ssid}"
    response = requests.get(url)
    if response.ok:
        return response.json().get("passkey")
    return None

def save_to_history(ssid: str, passkey: str):
    try:
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    entry = {
        "ssid": ssid,
        "passkey": passkey,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def hapus_riwayat():
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def export_ke_csv(filename="history_export.csv"):
    data = load_history()
    if not data:
        return False

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ssid", "passkey", "timestamp"])
        writer.writeheader()
        writer.writerows(data)
    return True

def check_connection(host="1.1.1.1", port=53, timeout=3) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
