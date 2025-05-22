import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from database.config import init_db
from rich.console import Console

console = Console()

def main():
    """Initialize the database with required tables."""
    try:
        console.print("[yellow]Initializing database...[/yellow]")
        init_db()
        console.print("[green]Database initialized successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error initializing database: {str(e)}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 