from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils import (
    is_valid_ssid, generate_passkey, save_to_history,
    load_history, hapus_riwayat, export_ke_csv, check_connection
)
import time

console = Console()

def tampilkan_riwayat(filter_date=None):
    history = load_history()
    if not history:
        console.print("[yellow]Belum ada riwayat.[/]")
        return

    if filter_date:
        history = [item for item in history if item["timestamp"].startswith(filter_date)]
        if not history:
            console.print(f"[red]Tidak ada data untuk tanggal {filter_date}[/]")
            return

    table = Table(title="Riwayat Generate", header_style="bold blue")
    table.add_column("SSID", style="cyan")
    table.add_column("Passkey", style="yellow")
    table.add_column("Waktu", style="green")

    for item in history:
        table.add_row(item["ssid"], item["passkey"], item["timestamp"])

    console.print(table)

def generate_mode():
    ssid = Prompt.ask("Masukkan SSID (fh_xxxxxx atau fh_xxxxxx_5G)")
    if not is_valid_ssid(ssid):
        console.print("[red]SSID tidak valid![/]")
        return

    if not check_connection():
        console.print("[bold red]Tidak ada koneksi internet. Periksa jaringan Anda.[/]")
        return

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Mengambil passkey...", total=None)
        time.sleep(1.5)
        try:
            passkey = generate_passkey(ssid)
            if passkey:
                console.print(f"\\n[bold green]Passkey untuk {ssid}:[/] [yellow]{passkey}[/]")
                save_to_history(ssid, passkey)
            else:
                console.print("[red]Passkey tidak ditemukan![/]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

def menu():
    console.rule("[bold blue]FiberHome WiFi Passkey Generator")

    while True:
        console.print("\\n[bold cyan]Menu:[/]")
        console.print("1. Generate Passkey")
        console.print("2. Lihat Riwayat")
        console.print("3. Hapus Riwayat")
        console.print("4. Export Riwayat ke CSV")
        console.print("5. Keluar")

        pilihan = Prompt.ask("\\nPilih opsi", choices=["1", "2", "3", "4", "5"], default="1")

        if pilihan == "1":
            generate_mode()

        elif pilihan == "2":
            console.print("\\n[bold cyan]Lihat Riwayat:[/]")
            console.print("1. Semua Riwayat")
            console.print("2. Filter Berdasarkan Tanggal (YYYY-MM-DD)")
            sub = Prompt.ask("Pilih opsi", choices=["1", "2"], default="1")

            if sub == "1":
                tampilkan_riwayat()
            elif sub == "2":
                tanggal = Prompt.ask("Masukkan tanggal (format: YYYY-MM-DD)")
                tampilkan_riwayat(filter_date=tanggal)

        elif pilihan == "3":
            if Confirm.ask("Yakin ingin menghapus semua riwayat?", default=False):
                hapus_riwayat()
                console.print("[green]Riwayat telah dihapus.[/green]")
            else:
                console.print("[yellow]Batal menghapus riwayat.[/yellow]")

        elif pilihan == "4":
            if export_ke_csv():
                console.print("[green]Riwayat berhasil diekspor ke 'history_export.csv'[/green]")
            else:
                console.print("[yellow]Tidak ada data untuk diekspor.[/yellow]")

        elif pilihan == "5":
            console.print("[bold green]Sampai jumpa![/]")
            break

if __name__ == "__main__":
    menu()
