import pandas as pd
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv
from utils.llm_utils import classify_intent, prepare_sql_data, get_required_fields

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

# Constants
MOCK_DB_DIR = Path("mock_db")
USERS_CSV = MOCK_DB_DIR / "users.csv"
PRODUCTS_CSV = MOCK_DB_DIR / "products.csv"

# Ensure mock database directory exists
MOCK_DB_DIR.mkdir(exist_ok=True)

def initialize_csv_files():
    """Initialize CSV files if they don't exist."""
    if not USERS_CSV.exists():
        users_df = pd.DataFrame(columns=[
            'id', 'email', 'full_name', 'hashed_password',
            'is_active', 'created_at', 'updated_at'
        ])
        users_df.to_csv(USERS_CSV, index=False)

    if not PRODUCTS_CSV.exists():
        products_df = pd.DataFrame(columns=[
            'id', 'name', 'description', 'price',
            'stock', 'category', 'created_at', 'updated_at'
        ])
        products_df.to_csv(PRODUCTS_CSV, index=False)

def collect_field_data(field: str) -> str:
    """Collect data for a specific field from the user."""
    return Prompt.ask(f"Please enter the {field}")

def execute_query(action: str, cleaned_data: dict) -> bool:
    """Execute the operation on the CSV files using cleaned data."""
    try:
        if action == "ADD_PRODUCT":
            df = pd.read_csv(PRODUCTS_CSV)
            new_id = len(df) + 1
            now = datetime.now().isoformat()
            
            new_row = {
                'id': new_id,
                'name': cleaned_data['name'],
                'description': cleaned_data['description'],
                'price': cleaned_data['price'],
                'stock': cleaned_data['stock'],
                'category': cleaned_data['category'],
                'created_at': now,
                'updated_at': now
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
        elif action == "DELETE_PRODUCT":
            df = pd.read_csv(PRODUCTS_CSV)
            product_id = cleaned_data['id']
            df = df[df['id'] != product_id]
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
        elif action == "UPDATE_PRODUCT":
            df = pd.read_csv(PRODUCTS_CSV)
            product_id = cleaned_data['id']
            mask = df['id'] == product_id
            
            for key, value in cleaned_data.items():
                if key != 'id':  # Skip the id field
                    df.loc[mask, key] = value
            
            df.loc[mask, 'updated_at'] = datetime.now().isoformat()
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
    except Exception as e:
        console.print(f"[red]Error executing operation: {str(e)}[/red]")
        return False
    
    return False

def main():
    """Main function to run the product management assistant."""
    console.print("[bold blue]Welcome to the Product Management Assistant![/bold blue]")
    console.print("Type 'exit' to quit the program.")
    
    initialize_csv_files()
    
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