import os
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv
from database.config import get_db, init_db
from repositories.product_repository import ProductRepository
from utils.llm_utils import classify_intent, prepare_sql_data, get_required_fields

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

def collect_field_data(field: str) -> str:
    """Collect data for a specific field from the user."""
    return Prompt.ask(f"Please enter the {field}")

def execute_query(action: str, cleaned_data: dict) -> bool:
    """Execute the operation on the database using cleaned data."""
    try:
        db = next(get_db())
        repository = ProductRepository(db)
        
        if action == "ADD_PRODUCT":
            repository.create_product(cleaned_data)
            return True
            
        elif action == "DELETE_PRODUCT":
            return repository.delete_product(cleaned_data['id'])
            
        elif action == "UPDATE_PRODUCT":
            product = repository.update_product(cleaned_data['id'], cleaned_data)
            return product is not None
            
    except Exception as e:
        console.print(f"[red]Error executing operation: {str(e)}[/red]")
        return False
    
    return False

def main():
    """Main function to run the product management assistant."""
    console.print("[bold blue]Welcome to the SQL Product Management Assistant![/bold blue]")
    console.print("Type 'exit' to quit the program.")
    
    # Initialize database
    init_db()
    
    while True:
        user_input = Prompt.ask("\nWhat would you like to do?")
        
        if user_input.lower() == 'exit':
            break
            
        # Classify the intent
        action = classify_intent(user_input)
        console.print(f"[green]Detected action: {action}[/green]")
        
        # Collect required fields
        required_fields = get_required_fields(action)
        collected_data = {}
        
        for field in required_fields:
            value = collect_field_data(field)
            collected_data[field] = value
        
        # Clean and format the data
        cleaned_data = prepare_sql_data(action, collected_data)
        console.print(f"[yellow]Cleaned data: {cleaned_data}[/yellow]")
        
        # Execute the operation
        success = execute_query(action, cleaned_data)
        if success:
            console.print("[green]Operation completed successfully![/green]")
        else:
            console.print("[red]Operation failed![/red]")

if __name__ == "__main__":
    main() 