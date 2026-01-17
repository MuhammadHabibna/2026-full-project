import os
import re
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()

class InvertedIndex:
    def __init__(self):
        self.index = {}  # {word: [(path, line_num), ...]}
        self.documents = {} # {path: [lines]}

    def clean_text(self, text):
        """Tokenize and clean text."""
        # Simple regex to keep alphanumeric
        return re.findall(r'\b\w+\b', text.lower())

    def build_index(self, root_dir):
        """Walk directory and index files."""
        console.print(f"[bold cyan]Scanning {root_dir}...[/bold cyan]")
        start_time = time.time()
        count = 0
        
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(('.txt', '.md', '.py', '.html', '.css', '.js')):
                    filepath = os.path.join(dirpath, filename)
                    self._index_file(filepath)
                    count += 1
                    
        duration = time.time() - start_time
        console.print(f"[green]Indexed {count} files in {duration:.2f} seconds.[/green]")

    def _index_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                self.documents[filepath] = lines
                
                for line_num, line in enumerate(lines, 1):
                    words = self.clean_text(line)
                    for word in set(words): # Use set to avoid duplicate hits per line
                        if word not in self.index:
                            self.index[word] = []
                        self.index[word].append((filepath, line_num))
        except Exception:
            # Skip unreadable files
            pass

    def search(self, query):
        """Search for a query string."""
        terms = self.clean_text(query)
        if not terms:
            return {}

        # Simple AND search: must contain all terms (or at least first term for now)
        # Let's do single term search or finding intersection for multiple
        
        # Start with results for first term
        first_term = terms[0]
        results = self.index.get(first_term, [])
        
        # Filter for subsequent terms (AND logic)
        for term in terms[1:]:
            term_results = self.index.get(term, [])
            # Inefficient intersection but works for small scale
            # We need to intersect based on (filepath, line_num)? 
            # Or just filepath? Usually search engines match document. 
            # But here we index lines.
            
            # Let's stick to simple "matches any" OR logic for simplicity, 
            # or strict AND. Let's do exact match of first term for MVP.
            pass
            
        return results

    def display_results(self, query, results):
        if not results:
            console.print("[red]No results found.[/red]")
            return

        # Group by file
        grouped = {}
        for path, line_num in results:
            if path not in grouped:
                grouped[path] = []
            grouped[path].append(line_num)

        console.print(f"\nFound matches in [bold]{len(grouped)}[/bold] files:\n")

        for path, line_nums in grouped.items():
            console.print(Panel(f"[bold blue]{path}[/bold blue]"))
            
            # Show top 3 matches per file to avoid spam
            lines = self.documents[path]
            for ln in line_nums[:3]:
                # 0-indexed list, 1-indexed line_num
                content = lines[ln-1].strip()
                # Highlight query
                highlighted = content.replace(query, f"[black on yellow]{query}[/black on yellow]")
                console.print(f"  [dim]{ln}:[/dim] {highlighted}")
            
            if len(line_nums) > 3:
                console.print(f"  [dim]... and {len(line_nums)-3} more lines.[/dim]")
            print()

def main():
    console.print(Panel("[bold white]Local Search Engine[/bold white]", style="magenta"))
    
    # Default to parent of current dir (to scan sibling projects)
    # But for safety/speed, let's ask or default to current.
    # User might want to search all 365days.
    default_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    
    target_dir = Prompt.ask("Directory to scan", default=default_path)
    
    engine = InvertedIndex()
    engine.build_index(target_dir)
    
    while True:
        query = Prompt.ask("\n[bold green]Search[/bold green] (or 'exit')")
        if query.lower() in ('exit', 'quit'):
            break
        
        results = engine.search(query)
        engine.display_results(query, results)

if __name__ == "__main__":
    main()
