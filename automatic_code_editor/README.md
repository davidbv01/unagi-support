# Automatic Code Editor for Web Designers/Hosters

This project aims to create an automatic code editor that interacts with a PostgreSQL database based on chat messages. The system will allow users to add or delete information from their databases through a conversational interface.

## Project Overview

The pipeline for processing user requests is as follows:

1.  **Input Message**: The system receives a message from the user via the terminal.
2.  **Client Database Identification**: The system identifies the client's database using an identifier from the message (e.g., phone number).
3.  **Database Structure Retrieval**: The system obtains the schema (tables, columns, types) of the identified client's database.
4.  **Contextualization with LLM**: The database structure and the user's request are sent to a simulated Large Language Model (LLM). The LLM determines if more information is needed to formulate a database query.
    *   If more data is needed, the LLM (simulated) will prompt the user for the specific details (e.g., "For adding a product, I need the name, price, description, and image URL.").
5.  **Query Generation and Execution**: Once all necessary information is gathered, the (simulated) LLM generates the appropriate SQL query (e.g., `INSERT`, `DELETE`). This query is then executed against the client's database.
6.  **Output/End**: The system provides feedback to the user (e.g., "Product added successfully," or error messages) via the terminal.

## Current Stage

This is the initial setup phase, focusing on:
*   Defining the project structure.
*   Creating placeholder functions and modules.
*   Documenting the intended functionality and workflow.

## Future Development (Not in scope for initial setup)

*   Integration with a real LLM.
*   Development of a chat interface (beyond simple terminal I/O).
*   Robust error handling and security measures.
*   User authentication and management.
*   Handling complex queries and database alterations. 