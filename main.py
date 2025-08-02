#! usr/bin/env python3 | coding = utf-8
# Coded by WahyuDin Ambia
# Created - Selasa, 29 Juli 2025

# <!-- Import Library--->
import time, os, random, datetime
from datetime import datetime
from time import strftime
from rich import print as cetak
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils import (
    is_valid_ssid, generate_passkey, save_to_history,
    load_history, hapus_riwayat, export_ke_csv, check_connection
)
console = Console()

M2, H2, K2, P2, B2, U2, O2, C2, J2 = ["[#FF0000]", "[#00FF00]", "[#FFFF00]", "[#FFFFFF]", "[#1e00ff]", "[#b900ff]", "[#EB6000]", "[#00fbff]", "[#ff14cf]"]
acak = [M2, H2, K2, B2, U2, O2, P2, C2, J2]
warna2 = random.choice(acak)
til =f"{M2}● {K2}● {H2}●"
ken = f'{M2}›{K2}›{H2}› '
tod = f' {H2}‹{K2}‹{M2}‹'

# <-------[ Time ]------->
bulan = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'September','10': 'October', '11': 'November', '12': 'December'}
tgl = datetime.now().day
bln = bulan[(str(datetime.now().month))]
thn = datetime.now().year
tang = (str(tgl)+' '+str(bln)+' '+str(thn))
waktu = strftime('%H:%M:%S')
hari = datetime.now().strftime("%A")

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")
# <!-- Banner --->
def banner():
  bersihkan_layar()
  console.rule("[bold]> FiberHome WiFi Passkey Generator <")
  logo = f''' {til}{P2}[bold]
 _  _  ___  ____  _    _  __  ___   _ _    
( \( )(  _)(_  _)( \/\/ )/  \(  ,) ( ) )  © 2025 by @why.404_
 )  (  ) _)  )(   \    /( () ))  \  )  \      version 1.0
(_)\_)(___) (__)   \/\/  \__/(_)\_)(_)\_)

🤖 Network Engineering
🕐 {waktu} - {hari}, {tang}
'''
  cetak(logo)

# <!-- History --->
def tampilkan_riwayat(filter_date=None):
    history = load_history()
    if not history:
        print("---------------------------------------------")
        print("⚠️ Belum ada riwayat.")
        return
    if filter_date:
        history = [item for item in history if item["timestamp"].startswith(filter_date)]
        if not history:
            print(f"⚠️ Tidak ada data untuk tanggal {filter_date}[/]")
            return
    table = Table(title="Riwayat Generate", header_style="bold white")
    table.add_column("SSID", style="cyan")
    table.add_column("Passkey", style="yellow")
    table.add_column("Waktu", style="green")
    for item in history:
        table.add_row(item["ssid"], item["passkey"], item["timestamp"])
    console.print(table)

# <!-- Input SSID --->
def generate_mode():
    banner()
    ssid = input("🤖 input SSID (fh_xxxxxx atau fh_xxxxxx_5G) > ")
    if not is_valid_ssid(ssid):
        print("---------------------------------------------")
        print("⚠️ SSID tidak valid!")
        return;banner()
    if not check_connection():
        print("---------------------------------------------")
        print("📵 Tidak ada koneksi internet. Periksa jaringan Anda.")
        return;banner()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="⏳ Mengambil passkey...", total=None)
        time.sleep(1.5)
        try:
            passkey = generate_passkey(ssid)
            if passkey:
                print("---------------------------------------------")
                print(f"✅ Passkey untuk {ssid} : {passkey}")
                save_to_history(ssid, passkey)
            else:
                print("---------------------------------------------")
                print("⚠️ Passkey tidak ditemukan!")
        except Exception as e:
            print(f"⚠️ Error: {e}")

# <!-- Menu --->
def menu():
    banner()
    while True:
        print("---------------------------------------------")
        print("1. Generate Passkey")
        print("2. Lihat Riwayat")
        print("3. Hapus Riwayat")
        print("4. Export Riwayat ke CSV")
        print("5. Keluar")
        print("---------------------------------------------")
        pilihan = input("🤖 input@wahyudev. > ")
        if pilihan == "1":
            generate_mode()
        elif pilihan == "2":
            print("---------------------------------------------")
            print("🤖 Lihat Riwayat Generator Passkey:")
            print("1. Semua Riwayat")
            print("2. Filter Berdasarkan Tanggal")
            print("---------------------------------------------")
            sub = input("✍️ Pilih opsi > ")
            if sub == "1":
                banner()
                tampilkan_riwayat()
            elif sub == "2":
                banner()
                tanggal = input("✍️ Masukkan tanggal (format: YYYY-MM-DD): ")
                tampilkan_riwayat(filter_date=tanggal)
        elif pilihan == "3":
            if Confirm.ask("\n🫵 Yakin ingin menghapus semua riwayat?", default=False):
                banner()
                hapus_riwayat()
                console.print("✅ Riwayat telah dihapus.");time.sleep(1);banner
            else:
                print("\n⚠️ Batal menghapus riwayat.");time.sleep(1);banner()
        elif pilihan == "4":
            if export_ke_csv():
                print("\n✅ Riwayat berhasil diekspor ke 'history_export.csv'");time.sleep(1)
            else:
                print("\n⚠️ Tidak ada data untuk diekspor.");time.sleep(1);banner()
        elif pilihan == "5":
            print("\n👋 Sampai jumpa!")
            exit()
        else:
            print("\n[!] Input Yang Bener!");time.sleep(2)
            menu()

if __name__ == "__main__":
    menu()
