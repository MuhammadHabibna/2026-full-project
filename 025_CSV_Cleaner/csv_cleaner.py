import pandas as pd
import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class DataCleaner:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.df = None
        self.original_rows = 0
        self.cleaned_rows = 0
        
    def load_data(self):
        """Loads data with automatic encoding detection."""
        try:
            # Try default utf-8 first
            self.df = pd.read_csv(self.filepath)
        except UnicodeDecodeError:
            try:
                # Try latin1 fallback
                self.df = pd.read_csv(self.filepath, encoding='latin1')
            except Exception as e:
                console.print(f"[bold red]Failed to load CSV:[/bold red] {e}")
                sys.exit(1)
        
        self.original_rows = len(self.df)
        console.print(f"[green]Loaded {self.filepath.name} with {self.original_rows} rows.[/green]")

    def clean_columns(self):
        """Normalizes column names."""
        console.print("[dim]Normalizing column names...[/dim]")
        
        # Strip whitespace, lowercase, replace spaces with underscores
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Remove any empty named columns
        self.df = self.df.loc[:, ~self.df.columns.str.contains('^unnamed')]

    def clean_rows(self):
        """Cleans headers, duplicate rows, empty rows."""
        console.print("[dim]Cleaning rows (dedup & empty checks)...[/dim]")
        
        # Drop duplicates
        dup_count = self.df.duplicated().sum()
        self.df.drop_duplicates(inplace=True)
        if dup_count > 0:
            console.print(f"  - Removed [bold yellow]{dup_count}[/bold yellow] duplicate rows.")
            
        # Drop fully empty rows
        self.df.dropna(how='all', inplace=True)
        
        # Convert string columns: strip whitespace
        for col in self.df.select_dtypes(['object']):
            self.df[col] = self.df[col].str.strip()
            
    def validate_types(self):
        """Attempts to deduce types and clean inconsistent values."""
        console.print("[dim]Validating data types...[/dim]")
        
        for col in self.df.columns:
            # Attempt numeric conversion
            # coerce errors will turn "1O0" (typo) into NaN, which is often desired for cleaning
            if 'score' in col or 'amount' in col or 'price' in col:
                 self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                 console.print(f"  - Converted column '{col}' to Numeric.")
                 
            # Attempt date conversion
            if 'date' in col or 'time' in col or 'joined' in col:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                console.print(f"  - Converted column '{col}' to Datetime.")

            # Email lowercasing
            if 'email' in col:
                self.df[col] = self.df[col].str.lower()
                console.print(f"  - Standardized column '{col}' (lowercase).")

    def generate_report(self):
        """Displays summary report."""
        self.cleaned_rows = len(self.df)
        
        table = Table(title="Cleaning Report")
        table.add_column("Metric", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        
        table.add_row("Original Rows", str(self.original_rows))
        table.add_row("Cleaned Rows", str(self.cleaned_rows))
        table.add_row("Dropped Rows", str(self.original_rows - self.cleaned_rows))
        table.add_row("Missing Values", str(self.df.isnull().sum().sum()))
        
        console.print(table)
        
        # Column specific report
        console.print("\n[bold]Column Summary:[/bold]")
        col_table = Table(show_header=True, header_style="bold blue")
        col_table.add_column("Column")
        col_table.add_column("Type")
        col_table.add_column("Missing")
        
        for col in self.df.columns:
            col_table.add_row(col, str(self.df[col].dtype), str(self.df[col].isnull().sum()))
            
        console.print(col_table)

    def save_data(self):
        """Saves the cleaned data."""
        output_name = f"{self.filepath.stem}_cleaned.csv"
        output_path = self.filepath.parent / output_name
        self.df.to_csv(output_path, index=False)
        console.print(f"\n[bold green]Success![/bold green] Cleaned data saved to: [underline]{output_name}[/underline]")

def main():
    parser = argparse.ArgumentParser(description="CSV Smart Cleaner")
    parser.add_argument("file", nargs='?', help="Path to CSV file")
    args = parser.parse_args()
    
    console.print(Panel.fit("[bold white]CSV Auto Cleaner & Validator[/bold white]", style="bold blue"))
    
    file_path = args.file
    if not file_path:
        file_path = console.input("[yellow]Enter CSV file path[/yellow]: ").strip().replace('"', '')
        
    if not Path(file_path).exists():
        console.print("[bold red]Error:[/bold red] File not found!")
        return

    cleaner = DataCleaner(file_path)
    cleaner.load_data()
    cleaner.clean_columns()
    cleaner.clean_rows()
    cleaner.validate_types()
    cleaner.generate_report()
    cleaner.save_data()

if __name__ == "__main__":
    main()
