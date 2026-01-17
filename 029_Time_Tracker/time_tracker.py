import sys
from datetime import datetime
from rich.console import Console

from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
import database

# Initialize Console
console = Console()

def show_menu():
    """Display the main menu."""
    console.print("\n[bold cyan]Time Tracker Menu[/bold cyan]")
    console.print("1. [green]Start Timer[/green]")
    console.print("2. [yellow]Stop Timer[/yellow]")
    console.print("3. [blue]View Daily Report[/blue]")
    console.print("4. [red]Exit[/red]")

def start_flow():
    """Handle starting a task."""
    task_name = Prompt.ask("[bold green]Enter task name[/bold green]")
    if not task_name:
        console.print("[red]Task name cannot be empty.[/red]")
        return
        
    msg = database.start_task(task_name)
    console.print(Panel(f"[bold green]{msg}[/bold green]", title="Timer Started"))

def stop_flow():
    """Handle stopping a task."""
    try:
        msg = database.stop_task()
        style = "bold green" if "Stopped" in msg else "bold yellow"
        console.print(Panel(f"[{style}]{msg}[/{style}]", title="Timer Stopped"))
    except Exception as e:
        console.print(f"[bold red]Error stopping task:[/bold red] {e}")

def report_flow():
    """Handle reporting."""
    summary = database.get_today_report()
    
    if not summary:
        console.print(Panel("No completed tasks found for today.", title="Daily Report", style="yellow"))
        return

    table = Table(title=f"Time Report - {datetime.now().strftime('%Y-%m-%d')}")
    table.add_column("Task Name", style="cyan")
    table.add_column("Duration", justify="right", style="magenta")
    table.add_column("Percent", justify="right", style="green")

    total_duration = sum((d.total_seconds() for d in summary.values()), 0)
    
    for task, duration in summary.items():
        seconds = duration.total_seconds()
        percentage = (seconds / total_duration) * 100 if total_duration > 0 else 0
        
        # Format duration nice
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        time_str = f"{int(hours)}h {int(mins)}m" if hours > 0 else f"{int(mins)}m"
        
        table.add_row(task, time_str, f"{percentage:.1f}%")

    total_hours, total_remainder = divmod(total_duration, 3600)
    total_mins, _ = divmod(total_remainder, 60)
    total_str = f"{int(total_hours)}h {int(total_mins)}m"
    
    console.print(table)
    console.print(f" [bold]Total Time Today:[/bold] {total_str}")

def main():
    database.init_db()
    console.print(Panel("[bold white]Welcome to Day 29 Time Tracker[/bold white]", style="blue"))

    while True:
        show_menu()
        choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4"], default=3)
        
        if choice == 1:
            start_flow()
        elif choice == 2:
            stop_flow()
        elif choice == 3:
            report_flow()
        elif choice == 4:
            console.print("[bold]Goodbye![/bold]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold]Exiting...[/bold]")
