import json
import os
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich import box

# Configuration
DATA_FILE = "snippets.json"
console = Console()

def load_snippets():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_snippets(snippets):
    with open(DATA_FILE, "w") as f:
        json.dump(snippets, f, indent=4)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_snippet(snippets):
    console.print(Panel("[bold green]Add New Snippet[/bold green]", expand=False))
    
    title = Prompt.ask("[bold cyan]Title[/bold cyan]")
    lang = Prompt.ask("[bold cyan]Language[/bold cyan] (e.g., python, js)", default="python")
    tags_str = Prompt.ask("[bold cyan]Tags[/bold cyan] (comma separated)")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    console.print("[dim]Enter your code below. Type 'END' on a new line to finish:[/dim]")
    code_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        code_lines.append(line)
    
    code = "\n".join(code_lines)
    
    new_id = 1
    if snippets:
        new_id = max(s['id'] for s in snippets) + 1
        
    snippet = {
        "id": new_id,
        "title": title,
        "language": lang,
        "tags": tags,
        "code": code
    }
    
    snippets.append(snippet)
    save_snippets(snippets)
    console.print(f"\n[bold green]Success![/bold green] Snippet saved with ID {new_id}!")
    input("\nPress Enter to continue...")

def display_snippets(snippets_to_show):
    if not snippets_to_show:
        console.print("[yellow]No snippets found.[/yellow]")
        return False

    table = Table(box=box.ROUNDED)
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Title", style="bold white")
    table.add_column("Language", style="magenta")
    table.add_column("Tags", style="green")

    for s in snippets_to_show:
        tags_display = ", ".join(s['tags'])
        table.add_row(str(s['id']), s['title'], s['language'], tags_display)

    console.print(table)
    return True

def view_and_copy(snippets):
    console.print(Panel("[bold blue]Search & Copy[/bold blue]", expand=False))
    query = Prompt.ask("[bold cyan]Search (Title/Tags)[/bold cyan] (Leave empty for all)").lower()
    
    filtered = [
        s for s in snippets 
        if query in s['title'].lower() or any(query in t.lower() for t in s['tags'])
    ]
    
    if display_snippets(filtered):
        choice = Prompt.ask("\n[bold yellow]Enter ID to Copy/View[/bold yellow] (or 'b' to back)")
        if choice.lower() == 'b':
            return

        selected = next((s for s in filtered if str(s['id']) == choice), None)
        if selected:
            clear_screen()
            console.print(Panel(f"[bold]{selected['title']}[/bold] ({selected['language']})", style="blue"))
            
            syntax = Syntax(selected['code'], selected['language'], theme="monokai", line_numbers=True)
            console.print(syntax)
            
            console.print("\nOptions:")
            console.print("1. [bold green]Copy to Clipboard[/bold green]")
            console.print("2. [bold red]Delete Snippet[/bold red]")
            console.print("3. Back")
            
            action = Prompt.ask("Choose", choices=["1", "2", "3"], default="1")
            
            if action == "1":
                pyperclip.copy(selected['code'])
                console.print("\n[bold green]✔ Code copied to clipboard![/bold green]")
                input("\nPress Enter to continue...")
            elif action == "2":
                if Confirm.ask(f"Delete snippet '{selected['title']}'?"):
                    snippets.remove(selected)
                    save_snippets(snippets)
                    console.print("[red]Snippet deleted.[/red]")
                    input("\nPress Enter to continue...")
        else:
            console.print("[red]Invalid ID.[/red]")
            input("\nPress Enter to continue...")

def main():
    while True:
        clear_screen()
        snippets = load_snippets()
        
        console.print(Panel.fit("[bold yellow]⚡ Snippet Manager ⚡[/bold yellow]\n[dim]Your personal code library[/dim]"))
        
        console.print("1. [bold green]Add Snippet[/bold green]")
        console.print("2. [bold blue]Search & Copy[/bold blue]")
        console.print("3. [bold red]Exit[/bold red]")
        
        choice = Prompt.ask("\nSelect Option", choices=["1", "2", "3"])
        
        if choice == "1":
            clear_screen()
            add_snippet(snippets)
        elif choice == "2":
            clear_screen()
            view_and_copy(snippets)
        elif choice == "3":
            console.print("Bye! Keep coding! 🚀")
            break

if __name__ == "__main__":
    main()
