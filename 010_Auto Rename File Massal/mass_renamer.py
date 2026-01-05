import os
import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.text import Text
import sys
import io

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Initialize Console
console = Console()

def mass_rename():
    console.clear()
    
    # Header
    console.print(Panel(
        "[bold cyan]📁 AUTO MASS FILE RENAMER[/bold cyan]\n[dim]Organize your files instantly with date & numbering[/dim]",
        border_style="cyan"
    ))
    console.print()

    # Input: Target Directory
    target_dir_input = Prompt.ask("[bold white]📂 Masukkan Path Folder Target[/bold white]")
    target_path = Path(target_dir_input)

    # Validation
    if not target_path.exists():
        console.print(f"[bold red]❌ Error: Path '{target_path}' tidak ditemukan![/bold red]")
        return
    if not target_path.is_dir():
        console.print(f"[bold red]❌ Error: '{target_path}' bukan sebuah folder![/bold red]")
        return

    # Input: New Base Name
    base_name = Prompt.ask("[bold white]🏷️  Masukkan Nama Baru (Base Name)[/bold white]", default="File")
    
    # Get List of Files (exclude hidden files and directories)
    files = [f for f in target_path.iterdir() if f.is_file() and not f.name.startswith('.')]
    files.sort(key=lambda f: f.name) # Sort alphabetically/numerically by original name

    if not files:
        console.print("[yellow]⚠️  Tidak ada file ditemukan di folder ini.[/yellow]")
        return

    # Preview
    console.print(f"\n[bold blue]ℹ️  Ditemukan {len(files)} file untuk di-rename.[/bold blue]")
    console.print(f"[dim]Format Baru: {datetime.date.today()}_{base_name}_XXX.ext[/dim]\n")

    # Safety Confirmation
    if not Confirm.ask(f"[bold red]⚠️  Yakin ingin me-rename {len(files)} file ini?[/bold red]"):
        console.print("[red]Operasi dibatalkan.[/red]")
        return

    console.print("\n[bold]🚀 Memulai Proses...[/bold]\n")

    # Execution Loop
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    count = 0

    for index, file_path in enumerate(files, 1):
        extension = file_path.suffix
        new_filename = f"{today_date}_{base_name}_{index:03d}{extension}"
        new_path = target_path / new_filename

        # Skip if name is already correct to prevent errors or double renaming
        if file_path.name == new_filename:
            console.print(f"[dim]⏩ Skip: '{file_path.name}' (Sudah sesuai)[/dim]")
            continue

        try:
            os.rename(file_path, new_path)
            console.print(f"[green]✅ Renamed:[/green] '[dim]{file_path.name}[/dim]' ➡️  '[bold cyan]{new_filename}[/bold cyan]'")
            count += 1
        except Exception as e:
            console.print(f"[red]❌ Gagal Rename '{file_path.name}': {e}[/red]")

    # Final Summary
    console.print()
    console.print(Panel(
        f"[bold green]✨ SELESAI![/bold green]\nTotal file berhasil di-rename: [bold white]{count}[/bold white]",
        border_style="green"
    ))

if __name__ == "__main__":
    try:
        mass_rename()
    except KeyboardInterrupt:
        console.print("\n[red]Operasi dihentikan oleh pengguna.[/red]")
