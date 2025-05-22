"""
Functions for interacting with the Large Language Model (LLM).

This module will be responsible for:
- Formatting requests to the LLM.
- Sending database schema and user queries to the LLM.
- Receiving and parsing LLM responses, which might include:
    - Clarifying questions for the user.
    - SQL queries to be executed.
    - Confirmation of actions.
"""

# Future functions:
# def ask_llm_for_clarification(user_query, db_schema, api_key):
#     pass
#
# def ask_llm_to_generate_query(context, api_key):
#     pass 