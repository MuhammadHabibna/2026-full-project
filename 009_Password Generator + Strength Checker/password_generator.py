import secrets
import string
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.prompt import IntPrompt, Confirm
from rich.text import Text
from rich import box

# Initialize Console
console = Console()

def generate_password(length=12, use_symbols=True, use_numbers=True, use_upper=True):
    """
    Generates a secure password using the secrets library.
    Ensures at least one character from each selected category is included.
    """
    alphabet = string.ascii_lowercase
    required_chars = []

    if use_upper:
        alphabet += string.ascii_uppercase
        required_chars.append(secrets.choice(string.ascii_uppercase))
    
    if use_numbers:
        alphabet += string.digits
        required_chars.append(secrets.choice(string.digits))
    
    if use_symbols:
        alphabet += string.punctuation
        required_chars.append(secrets.choice(string.punctuation))

    # Fill the rest of the password length
    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        remaining_length = 0 # Handle edge case where length is very small
        
    password_chars = required_chars + [secrets.choice(alphabet) for _ in range(remaining_length)]
    
    # Shuffle to avoid predictable patterns (required chars at start)
    secrets.SystemRandom().shuffle(password_chars)
    
    return ''.join(password_chars)

def calculate_strength(password):
    """
    Calculates a simple strength score (0-100) based on length and variety.
    """
    score = 0
    length = len(password)
    
    # Base score based on lengthh (up to 40 points for 10 chars, max 60 for 15+)
    score += min(length * 4, 60)
    
    # Variety bonuses
    if any(c.isupper() for c in password):
        score += 15
    if any(c.isdigit() for c in password):
        score += 15
    if any(c in string.punctuation for c in password):
        score += 20
        
    # Cap at 100
    return min(score, 100)

def get_strength_color(score):
    if score < 50:
        return "red"
    elif score < 75:
        return "yellow"
    else:
        return "green"

def main():
    console.clear()
    
    # Title Header
    console.print(Panel.fit(
        "[bold cyan]🔐 ULTRA SECURE PASSWORD GENERATOR[/bold cyan]",
        box=box.DOUBLE,
        border_style="cyan"
    ))
    console.print()

    # User Inputs
    try:
        length = IntPrompt.ask("[bold white]🔢 Masukkan panjang password[/bold white]", default=12)
        if length < 4:
            console.print("[red]⚠️  Panjang password minimal 4 karakter![/red]")
            return
            
        use_symbols = Confirm.ask("[bold white]🔣 Gunakan Simbol?[/bold white]", default=True)
        use_numbers = Confirm.ask("[bold white]1️⃣  Gunakan Angka?[/bold white]", default=True)
        use_upper = Confirm.ask("[bold white]🔠 Gunakan Huruf Besar?[/bold white]", default=True)
    except KeyboardInterrupt:
        console.print("\n[red]Operasi dibatalkan.[/red]")
        return

    console.print()

    # Generating Animationn
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task1 = progress.add_task("[cyan]Generating Entropy...", total=100)
        
        # Simulate complex calculation
        for _ in range(20):
            time.sleep(0.05)
            progress.update(task1, advance=5)
            
        password = generate_password(length, use_symbols, use_numbers, use_upper)
        
        task2 = progress.add_task("[magenta]Analyzing Security Strength...", total=100)
        for _ in range(20):
            time.sleep(0.04)
            progress.update(task2, advance=5)
            
        score = calculate_strength(password)
        color = get_strength_color(score)

    # Final Output
    console.print()
    
    result_text = Text()
    result_text.append("\n🔑 PASSWORD ANDA:\n", style="bold white")
    result_text.append(f"{password}\n", style="bold green on black")
    result_text.append("\n🛡️  SECURITY SCORE: ", style="bold white")
    result_text.append(f"{score}/100", style=f"bold {color}")
    
    if score >= 90:
        verdict = "UNHACKABLE"
    elif score >= 70:
        verdict = "STRONG"
    elif score >= 50:
        verdict = "MODERATE"
    else:
        verdict = "WEAK"
        
    result_text.append(f" ({verdict})", style=f"italic {color}")

    console.print(Panel(
        result_text,
        title="[bold green]GENERATION COMPLETE[/bold green]",
        border_style="green",
        expand=False
    ))
    
    console.print("\n[dim]Tips: Jangan pernah bagikan password ini kepada siapapun![/dim]")

if __name__ == "__main__":
    main()
