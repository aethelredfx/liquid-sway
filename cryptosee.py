import os
import time
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console(force_terminal=True, color_system="truecolor")

LOGO_LINES = [
    "██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗███████╗███████╗",
    "██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔════╝██╔════╝██╔════╝",
    "██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║╚█████╗ █████╗  █████╗  ",
    "██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║ ╚═══██╗██╔══╝  ██╔══╝  ",
    "╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██████╔╝███████╗███████╗",
    " ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝╚══════╝"
]

SUBHEADER = "Terminal Crypto Monitor"

def get_center_padding(text_len):
    try:
        terminal_width = os.get_terminal_size().columns
    except OSError:
        terminal_width = 80
    return max(0, (terminal_width - text_len) // 2)

def print_centered_header():
    for line in LOGO_LINES:
        padding = " " * get_center_padding(len(line))
        console.print(f"{padding}[bold orange3]{line}[/bold orange3]")
    
    padding = " " * get_center_padding(len(SUBHEADER))
    console.print(f"{padding}[bold dark_orange]{SUBHEADER}[/bold dark_orange]")

def fetch_crypto_data():
    url = "https://coinmarketcap.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        console.print(f"\n[bold red]Network error: {e}[/bold red]")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    table_body = soup.find("tbody")
    if not table_body:
        table = soup.find("table")
        if table:
            table_body = table.find("tbody")
            
    if not table_body:
        return []

    rows = table_body.find_all("tr")[:15]
    crypto_list = []

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        
        try:
            rank_text = cells[1].text.strip() if len(cells) > 1 else ""
            if not rank_text.isdigit():
                rank_text = "".join(filter(str.isdigit, cells[1].text)) if len(cells) > 1 else ""
            if not rank_text:
                continue

            name_cell = cells[2]
            text_strings = [t.strip() for t in name_cell.stripped_strings if t.strip()]
            
            if len(text_strings) >= 2:
                name = text_strings[0]
                ticker = text_strings[1]
            else:
                name = text_strings[0] if text_strings else "Unknown"
                ticker = ""

            price_cell = cells[3]
            price = price_cell.text.strip()

            change_cell = cells[4] if len(cells) > 4 else None
            if change_cell:
                change_text = change_cell.text.strip()
                is_down = "icon-Caret-down" in str(change_cell) or "color-red" in str(change_cell) or "-" in change_text
                sign = "-" if is_down else "+"
                change_text = change_text.replace("+", "").replace("-", "").strip()
                final_change = f"{sign}{change_text}"
            else:
                final_change = "N/A"
            
            crypto_list.append({
                "rank": rank_text,
                "name": f"{name} ({ticker})" if ticker else name,
                "price": price,
                "change": final_change
            })
        except Exception:
            continue

    return crypto_list

def main():
    first_run = True
    
    try:
        while True:
            console.clear()
            print_centered_header()

            if first_run:
                with Progress(
                    SpinnerColumn(style="bold orange3"),
                    TextColumn("[bold dark_orange]{task.description}"),
                    BarColumn(bar_width=50, complete_style="orange3", finished_style="bold dark_orange"),
                    TaskProgressColumn(style="bold orange3"),
                    console=console
                ) as progress:
                    task = progress.add_task(" Fetching blockchain data...", total=100)
                    
                    for _ in range(40):
                        time.sleep(0.01)
                        progress.update(task, advance=1)
                        
                    data = fetch_crypto_data()
                    
                    while not progress.finished:
                        time.sleep(0.01)
                        progress.update(task, advance=3)
                first_run = False
            else:
                with console.status("[bold orange3]Updating marketplace data...[/bold orange3]"):
                    data = fetch_crypto_data()

            if not data:
                console.print("[bold red]Failed to retrieve top 15 assets. Retrying in 5s...[/bold red]")
                time.sleep(5)
                continue

            table = Table(
                title="\n[bold orange3]❖ CURRENT CRYPTOCURRENCY RANKINGS ❖[/bold orange3]", 
                header_style="bold orange3", 
                border_style="dark_orange",
                box=None
            )
            
            table.add_column("#", justify="center", style="dim orange3", width=4)
            table.add_column("Asset", justify="left", style="bold white")
            table.add_column("Price (USD)", justify="right", style="bold green")
            table.add_column("Change (24h)", justify="right")

            for coin in data:
                if coin["change"].startswith("-"):
                    change_style = "bold red"
                else:
                    change_style = "bold green"
                    
                table.add_row(
                    coin["rank"],
                    coin["name"],
                    coin["price"],
                    f"[{change_style}]{coin['change']}[/{change_style}]"
                )

            console.print(table)
            console.print(f"\n[bold dark_orange]Synced: {time.strftime('%X')} | cryptosee | Auto-refresh: 5s (Ctrl+C to exit)[/bold dark_orange]\n")
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Monitoring stopped by user.[/bold yellow]\n")
        input("Press Enter to close the application...")

if __name__ == "__main__":
    main()
