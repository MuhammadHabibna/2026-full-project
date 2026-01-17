import difflib
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

def get_multiline_input(label):
    """Capture multiline input from user."""
    console.print(f"\n[bold cyan]{label}[/bold cyan] (Type 'END' on a new line to finish):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return lines

def display_diff(text_a, text_b):
    """Display side-by-side or unified diff."""
    console.print(Panel("[bold]Diff Result[/bold]", style="blue"))
    
    diff = difflib.ndiff(text_a, text_b)
    
    # Process the diff generator
    # ndiff produces lines starting with:
    # '- ' : line unique to sequence 1 (deleted)
    # '+ ' : line unique to sequence 2 (added)
    # '  ' : line common to both
    # '? ' : internal difference on previous line
    
    for line in diff:
        code = line[:2]
        content = line[2:].rstrip()
        
        if code == '- ':
            console.print(Text(f"- {content}", style="bold red"))
        elif code == '+ ':
            console.print(Text(f"+ {content}", style="bold green"))
        elif code == '  ':
            console.print(Text(f"  {content}", style="dim white"))
        elif code == '? ':
            # This line indicates intra-line changes, useful but can be noisy. 
            # We'll skip printing it directly to keep it simple, 
            # or we could use it to highlight specific characters.
            pass

def main():
    console.print(Panel("[bold white]Text Diff Highlighter[/bold white]", style="magenta"))
    
    console.print("Paste your [bold]Original Text[/bold]:")
    text_a = get_multiline_input("Original Text")
    
    console.print("\nPaste your [bold]New Text[/bold]:")
    text_b = get_multiline_input("New Text")
    
    if not text_a and not text_b:
        console.print("[yellow]Empty inputs. Exiting.[/yellow]")
        return

    display_diff(text_a, text_b)

if __name__ == "__main__":
    main()
