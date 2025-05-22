import os
from typing import Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def classify_intent(user_input: str) -> str:
    """Use OpenAI to classify the user's intent."""
    prompt = (
        "Classify the following user input into one of these categories:\n"
        "- ADD_PRODUCT\n"
        "- DELETE_PRODUCT\n"
        "- UPDATE_PRODUCT\n\n"
        f"User input: {user_input}\n\n"
        "Respond with ONLY the category name, nothing else."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()

def prepare_sql_data(action: str, data: Dict[str, str]) -> Dict:
    """Clean and format data based on the action type."""
    if action == "ADD_PRODUCT":
        prompt = (
            "Clean and format the following product data for insertion into a database.\n"
            "Rules:\n"
            "- name: string, no special formatting needed\n"
            "- description: string, no special formatting needed\n"
            "- price: convert to float, remove currency symbols and commas (e.g., '123,44€' -> 123.44)\n"
            "- stock: convert to integer, remove any non-numeric characters\n"
            "- category: string, no special formatting needed\n\n"
            f"Input data: {data}\n\n"
            "Respond with a JSON object containing the cleaned values.\n"
            "Example format:\n"
            "{\n"
            "  'name': 'Product Name',\n"
            "  'description': 'Product Description',\n"
            "  'price': 123.44,\n"
            "  'stock': 100,\n"
            "  'category': 'Category Name'\n"
            "}"
        )
    elif action == "UPDATE_PRODUCT":
        prompt = (
            "Clean and format the following product data for updating a database record.\n"
            "Rules:\n"
            "- id: convert to integer\n"
            "- name: string, no special formatting needed\n"
            "- description: string, no special formatting needed\n"
            "- price: convert to float, remove currency symbols and commas (e.g., '123,44€' -> 123.44)\n"
            "- stock: convert to integer, remove any non-numeric characters\n"
            "- category: string, no special formatting needed\n\n"
            f"Input data: {data}\n\n"
            "Respond with a JSON object containing the cleaned values.\n"
            "Example format:\n"
            "{\n"
            "  'id': 1,\n"
            "  'name': 'Product Name',\n"
            "  'description': 'Product Description',\n"
            "  'price': 123.44,\n"
            "  'stock': 100,\n"
            "  'category': 'Category Name'\n"
            "}"
        )
    elif action == "DELETE_PRODUCT":
        prompt = (
            "Clean and format the following product ID for deletion.\n"
            "Rules:\n"
            "- id: convert to integer, remove any non-numeric characters\n\n"
            f"Input data: {data}\n\n"
            "Respond with a JSON object containing the cleaned ID.\n"
            "Example format:\n"
            "{\n"
            "  'id': 1\n"
            "}"
        )
    else:
        raise ValueError(f"Unknown action type: {action}")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    try:
        result = eval(response.choices[0].message.content.strip())
        return result
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {str(e)}")

def get_required_fields(action: str) -> List[str]:
    """Return the required fields for a given action."""
    if action == "ADD_PRODUCT":
        return ["name", "description", "price", "stock", "category"]
    elif action == "UPDATE_PRODUCT":
        return ["id", "name", "description", "price", "stock", "category"]
    elif action == "DELETE_PRODUCT":
        return ["id"]
    return []
