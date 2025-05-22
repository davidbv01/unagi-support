import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv
from openai import OpenAI

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def classify_intent(user_input: str) -> str:
    """Use OpenAI to classify the user's intent."""
    prompt = f"""Classify the following user input into one of these categories:
    - ADD_PRODUCT
    - DELETE_PRODUCT
    - UPDATE_PRODUCT
    
    User input: {user_input}
    
    Respond with ONLY the category name, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip()

def get_required_fields(action: str) -> List[str]:
    """Return the required fields for a given action."""
    if action == "ADD_PRODUCT":
        return ["name", "description", "price", "stock", "category"]
    elif action == "UPDATE_PRODUCT":
        return ["id", "name", "description", "price", "stock", "category"]
    elif action == "DELETE_PRODUCT":
        return ["id"]
    return []

def collect_field_data(field: str) -> str:
    """Collect data for a specific field from the user."""
    return Prompt.ask(f"Please enter the {field}")

def generate_sql_query(action: str, data: Dict[str, str]) -> str:
    """Generate SQL query based on action and collected data."""
    prompt = f"""Generate a SQL query for the following action and data:
    Action: {action}
    Data: {json.dumps(data, indent=2)}
    
    Respond with ONLY the SQL query, nothing else."""

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    return response.choices[0].message.content.strip()

def execute_query(query: str) -> bool:
    """Execute the generated query on the CSV files."""
    try:
        if "INSERT INTO products" in query:
            df = pd.read_csv(PRODUCTS_CSV)
            new_id = len(df) + 1
            now = datetime.now().isoformat()
            
            # Extract values from query
            values = query.split("VALUES")[1].strip("();").split(",")
            values = [v.strip().strip("'") for v in values]
            
            new_row = {
                'id': new_id,
                'name': values[0],
                'description': values[1],
                'price': float(values[2]),
                'stock': int(values[3]),
                'category': values[4],
                'created_at': now,
                'updated_at': now
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
        elif "DELETE FROM products" in query:
            df = pd.read_csv(PRODUCTS_CSV)
            product_id = int(query.split("id = ")[1].strip(";"))
            df = df[df['id'] != product_id]
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
        elif "UPDATE products" in query:
            df = pd.read_csv(PRODUCTS_CSV)
            # Extract values from query
            set_clause = query.split("SET")[1].split("WHERE")[0]
            where_clause = query.split("WHERE")[1].strip(";")
            
            product_id = int(where_clause.split("=")[1].strip())
            updates = dict(item.split("=") for item in set_clause.split(","))
            
            mask = df['id'] == product_id
            for key, value in updates.items():
                key = key.strip()
                value = value.strip().strip("'")
                if key in ['price']:
                    value = float(value)
                elif key in ['stock']:
                    value = int(value)
                df.loc[mask, key] = value
            
            df.loc[mask, 'updated_at'] = datetime.now().isoformat()
            df.to_csv(PRODUCTS_CSV, index=False)
            return True
            
    except Exception as e:
        console.print(f"[red]Error executing query: {str(e)}[/red]")
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
        
        # Generate and execute SQL query
        query = generate_sql_query(action, collected_data)
        console.print(f"[yellow]Generated query: {query}[/yellow]")
        
        success = execute_query(query)
        if success:
            console.print("[green]Operation completed successfully![/green]")
        else:
            console.print("[red]Operation failed![/red]")

if __name__ == "__main__":
    main() 