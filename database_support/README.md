# Product Management Assistant

A CLI-based assistant that helps manage products using natural language processing and a mock database system.

## Features

- Natural language processing for product management
- Support for adding, updating, and deleting products
- Mock database using CSV files
- Rich terminal interface
- OpenAI GPT integration for intent classification and SQL query generation

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the program:
```bash
python product_assistant.py
```

2. Interact with the assistant using natural language. For example:
- "I want to add a new product"
- "Delete product with ID 1"
- "Update the price of product 2"

3. Follow the prompts to provide the required information for each action.

4. Type 'exit' to quit the program.

## Data Structure

The program uses two CSV files in the `mock_db` directory:

### products.csv
- id (Integer, Primary Key)
- name (String, Not Null)
- description (String, Not Null)
- price (Float, Not Null)
- stock (Integer, Not Null, Default: 0)
- category (String, Not Null)
- created_at (DateTime, Not Null)
- updated_at (DateTime, Not Null)

### users.csv
- id (Integer, Primary Key)
- email (String, Unique, Not Null)
- full_name (String, Not Null)
- hashed_password (String, Not Null)
- is_active (Boolean, Default: True)
- created_at (DateTime, Not Null)
- updated_at (DateTime, Not Null)

## Requirements

- Python 3.8+
- OpenAI API key
- Required Python packages (see requirements.txt) 