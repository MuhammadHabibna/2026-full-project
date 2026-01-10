import feedparser
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
import textwrap

# Configuration
SAVED_FILE = "saved_articles.json"
FEEDS = {
    "CNN Indonesia": "https://www.cnnindonesia.com/nasional/rss",
    "Detik.com": "http://rss.detik.com/index.php/detikcom",
    "Kompas News": "https://www.kompas.com/rss/news",
    "Antara News": "https://www.antaranews.com/rss/top-news.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Verge": "https://www.theverge.com/rss/index.xml" 
}

console = Console()

class RSSReader:
    def __init__(self):
        self.articles = []
        self.saved_articles = self.load_saved_articles()

    def load_saved_articles(self):
        if not os.path.exists(SAVED_FILE):
            return []
        try:
            with open(SAVED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def save_article_to_disk(self, article):
        # Check if already saved
        if any(a['link'] == article['link'] for a in self.saved_articles):
            console.print("[yellow]Artikel ini sudah tersimpan![/yellow]")
            return

        # Add date saved
        article['saved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.saved_articles.append(article)
        
        with open(SAVED_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.saved_articles, f, indent=4, ensure_ascii=False)
        
        console.print(f"[green]Artikel '{article['title']}' berhasil disimpan![/green]")

    def fetch_feeds(self):
        self.articles = []
        with console.status("[bold green]Mengambil berita terbaru...[/bold green]", spinner="dots"):
            for source, url in FEEDS.items():
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:10]: # Ambil 10 teratas per feed
                        self.articles.append({
                            'source': source,
                            'title': entry.title,
                            'link': entry.link,
                            'summary': entry.get('summary', 'Tidak ada ringkasan.'),
                            'published': entry.get('published', 'Tanggal tidak diketahui')
                        })
                except Exception as e:
                    console.print(f"[red]Gagal mengambil {source}: {e}[/red]")
        
        console.print(f"[bold cyan]Berhasil mengambil {len(self.articles)} artikel dari berbagai sumber.[/bold cyan]\n")

    def display_articles(self, articles_to_show):
        if not articles_to_show:
            console.print("[red]Tidak ada artikel yang ditemukan.[/red]")
            return

        table = Table(title="Berita Terbaru", box=box.ROUNDED, show_lines=True)
        table.add_column("No", style="cyan", width=4)
        table.add_column("Sumber", style="magenta", width=15)
        table.add_column("Judul", style="white")
        table.add_column("Waktu", style="dim", width=20)

        for idx, article in enumerate(articles_to_show, 1):
            table.add_row(
                str(idx),
                article['source'],
                article['title'],
                article['published']
            )

        console.print(table)

    def display_saved_articles(self):
        if not self.saved_articles:
            console.print("[yellow]Belum ada artikel yang disimpan (Read Later).[/yellow]")
            return

        table = Table(title="Daftar Baca Nanti (Read Later)", box=box.DOUBLE_EDGE, show_lines=True)
        table.add_column("No", style="cyan", width=4)
        table.add_column("Sumber", style="magenta", width=15)
        table.add_column("Judul", style="white")
        table.add_column("Disimpan Pada", style="green", width=20)

        for idx, article in enumerate(self.saved_articles, 1):
            table.add_row(
                str(idx),
                article['source'],
                article['title'],
                article['saved_at']
            )
        console.print(table)
        
        if Confirm.ask("Buka artikel di browser?"):
             choice = Prompt.ask("Masukkan nomor artikel", default="0")
             try:
                 idx = int(choice) - 1
                 if 0 <= idx < len(self.saved_articles):
                     import webbrowser
                     webbrowser.open(self.saved_articles[idx]['link'])
                 else:
                     console.print("[red]Nomor tidak valid.[/red]")
             except ValueError:
                 console.print("[red]Input bukan angka.[/red]")


def main():
    reader = RSSReader()
    
    while True:
        console.clear()
        console.print(Panel.fit("[bold yellow]RSS News Reader Offline-Style[/bold yellow]", subtitle="Day 22"))
        
        console.print("[1] Ambil Berita Terbaru (Refresh)")
        console.print("[2] Cari & Filter Berita (Keyword)")
        console.print("[3] Simpan Artikel ke 'Read Later'")
        console.print("[4] Buka 'Read Later'")
        console.print("[ecs] Keluar (Ketik 'x' atau Ctrl+C)")
        
        choice = Prompt.ask("Pilih Menu", choices=["1", "2", "3", "4", "x"], default="1")

        if choice == '1':
            reader.fetch_feeds()
            reader.display_articles(reader.articles)
            Prompt.ask("\nTekan Enter untuk kembali ke menu...")

        elif choice == '2':
            if not reader.articles:
                reader.fetch_feeds()
            
            keyword = Prompt.ask("Masukkan kata kunci filter (misal: AI, Crypto, Google)")
            filtered = [a for a in reader.articles if keyword.lower() in a['title'].lower()]
            
            console.print(f"\n[bold]Hasil Filter untuk '{keyword}':[/bold]")
            reader.display_articles(filtered)
            Prompt.ask("\nTekan Enter untuk kembali ke menu...")

        elif choice == '3':
            if not reader.articles:
                console.print("[yellow]Belum ada berita. Mengambil data dulu...[/yellow]")
                reader.fetch_feeds()
            
            reader.display_articles(reader.articles)
            article_idx = Prompt.ask("Masukkan nomor artikel yang ingin disimpan", default="0")
            
            try:
                idx = int(article_idx) - 1
                if 0 <= idx < len(reader.articles):
                    reader.save_article_to_disk(reader.articles[idx])
                elif article_idx != "0":
                    console.print("[red]Nomor artikel tidak valid.[/red]")
            except ValueError:
                console.print("[red]Input harus berupa angka.[/red]")
            
            Prompt.ask("\nTekan Enter untuk kembali ke menu...")

        elif choice == '4':
            reader.display_saved_articles()
            Prompt.ask("\nTekan Enter untuk kembali ke menu...")

        elif choice == 'x':
            console.print("[bold]Sampai Jumpa![/bold]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold]Program dihentikan.[/bold]")
