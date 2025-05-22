# Product Management Assistant

A CLI-based product management assistant that uses PostgreSQL for data storage and OpenAI for natural language processing.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- OpenAI API key

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL:
   - Create a new database
   - Note down the database credentials

4. Configure environment variables:
   Create a `.env` file in the root directory with:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. Run database migrations:
```bash
alembic upgrade head
```

## Usage

Run the assistant:
```bash
python sql_product_assistant.py
```

The assistant supports the following operations:
- Add new products
- Update existing products
- Delete products
- View product details

## Development

### Database Migrations

To create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
alembic upgrade head
```

To rollback migrations:
```bash
alembic downgrade -1  # Roll back one migration
```

## Project Structure

```
database_support/
├── models/              # Database models
├── database/           # Database configuration
├── repositories/       # Database operations
├── utils/             # Utility functions
├── migrations/        # Database migrations
├── scripts/           # Utility scripts
└── sql_product_assistant.py  # Main application
``` 