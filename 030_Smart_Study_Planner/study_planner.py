import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.panel import Panel

console = Console()

class Subject:
    def __init__(self, name, deadline, hours_needed):
        self.name = name
        self.deadline = deadline
        self.hours_needed = hours_needed
        self.hours_allocated = 0

def get_date_input(prompt_text):
    """Helper to get date input."""
    while True:
        date_str = Prompt.ask(prompt_text)
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Invalid format. Use YYYY-MM-DD[/red]")

def collect_inputs():
    """Collect subjects from user."""
    subjects = []
    console.print(Panel("[bold]Smart Study Planner Input[/bold]", style="cyan"))
    console.print("Enter your subjects. Type 'done' as subject name to finish.\n")
    
    while True:
        name = Prompt.ask("[bold green]Subject Name[/bold green]")
        if name.lower() == 'done':
            break
        
        deadline = get_date_input(f"Deadline for [bold]{name}[/bold] (YYYY-MM-DD)")
        hours = IntPrompt.ask(f"Total hours needed for [bold]{name}[/bold]")
        
        # Validation: Deadline must be in future
        if deadline < datetime.date.today():
             console.print("[yellow]Warning: Deadline is in the past! Added anyway.[/yellow]")

        subjects.append(Subject(name, deadline, hours))
        console.print(f"[dim]Added {name}[/dim]\n")
        
    return subjects

def generate_schedule(subjects, daily_limit):
    """Generate a 7-day schedule."""
    today = datetime.date.today()
    schedule = {}  # {date: [(subject, hours), ...]}
    
    # Sort subjects by deadline (Urgency)
    subjects.sort(key=lambda s: s.deadline)
    
    for i in range(7):
        current_date = today + datetime.timedelta(days=i)
        schedule[current_date] = []
        available_hours = daily_limit
        
        # Round Robin allocation based on urgency would be complex.
        # Simple Greedy: Fill earliest deadline subject first.
        
        for subject in subjects:
            if available_hours <= 0:
                break
            
            # Skip if completed
            if subject.hours_allocated >= subject.hours_needed:
                continue
            
            # Skip if deadline passed (optional, strictly speaking we should cram, but let's stick to logic)
            if subject.deadline < current_date:
                continue

            # Allocate max possible for this subject today
            # We want to distribute load? Or finish ASAP?
            # Strategy: Allocate min(remaining_needed, available_hours)
            # To avoid burnout on one subject, maybe max 2 hours per subject per day if we have variety?
            # For simplicity: Greedy fill.
            
            remaining_needed = subject.hours_needed - subject.hours_allocated
            allocate = min(remaining_needed, available_hours)
            
            if allocate > 0:
                schedule[current_date].append((subject.name, allocate))
                subject.hours_allocated += allocate
                available_hours -= allocate
                
    return schedule

def display_schedule(schedule):
    """Print the schedule."""
    table = Table(title="Study Schedule (Next 7 Days)")
    table.add_column("Date", style="cyan", no_wrap=True)
    table.add_column("Day", style="blue")
    table.add_column("Plan", style="white")
    
    today = datetime.date.today()
    
    for date, tasks in schedule.items():
        day_name = date.strftime("%A")
        date_str = date.strftime("%Y-%m-%d")
        
        if not tasks:
            plan_str = "[dim]Free day / Relax[/dim]"
        else:
            plan_str = ", ".join([f"[bold]{name}[/bold] ({hrs}h)" for name, hrs in tasks])
            
        table.add_row(date_str, day_name, plan_str)
        
    console.print(table)

def main():
    console.print(Panel("[bold white]Welcome to Smart Study Planner Generator[/bold white]", style="blue"))
    
    daily_capacity = IntPrompt.ask("How many hours can you study per day?", default=3)
    
    subjects = collect_inputs()
    
    if not subjects:
        console.print("[yellow]No subjects entered. Exiting.[/yellow]")
        return
        
    console.print("\n[bold]Generating Schedule...[/bold]\n")
    schedule = generate_schedule(subjects, daily_capacity)
    display_schedule(schedule)
    
    # Check for unallocated
    unfinished = [s for s in subjects if s.hours_allocated < s.hours_needed]
    if unfinished:
        console.print(Panel("[bold red]Warning: Constraint Impossible[/bold red]", border_style="red"))
        for s in unfinished:
            remaining = s.hours_needed - s.hours_allocated
            console.print(f"could not schedule [bold]{remaining}h[/bold] for {s.name} (Deadline: {s.deadline})")
        console.print("[white]Tip: Increase daily study hours![/white]")

if __name__ == "__main__":
    main()
