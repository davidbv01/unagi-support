import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from rich.console import Console

# Initialize console for rich output
console = Console()

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Ensure the URL uses psycopg2 (never asyncpg)
# Acceptable: postgresql:// or postgresql+psycopg2://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
# If user accidentally put asyncpg, fix it:
if DATABASE_URL.startswith('postgresql+asyncpg://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql+psycopg2://', 1)

try:
    # Create database engine with connection pooling
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )
    # Test the connection using SQLAlchemy's text() for raw SQL
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        console.print("[green]Database connection successful![/green]")
except SQLAlchemyError as e:
    console.print(f"[red]Error connecting to database: {str(e)}[/red]")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session with automatic cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database by creating all tables."""
    try:
        from models.product import Base
        Base.metadata.create_all(bind=engine)
        console.print("[green]Database tables created successfully![/green]")
    except SQLAlchemyError as e:
        console.print(f"[red]Error creating database tables: {str(e)}[/red]")
        raise 