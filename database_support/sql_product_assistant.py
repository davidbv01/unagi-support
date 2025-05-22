import os
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.config import get_db, init_db
from repositories.product_repository import ProductRepository
from utils.llm_utils import classify_intent, prepare_sql_data, get_required_fields

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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