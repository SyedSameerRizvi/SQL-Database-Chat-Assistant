# SQL Database Chat Assistant 💬
This project is a Streamlit web application designed to assist users with their SQL queries using a conversational chatbot interface. The chatbot is powered by OpenAI's GPT-4 model and can connect to both SQLite and MySQL databases to assist with a variety of database-related tasks and queries.

You can check the app here: [SQL Database Chat Assistant](https://sql-database-chat-assistant-6thdvjxf9dypct3rdxltcy.streamlit.app/)

## Features
- Database Chatbot: Ask questions about SQL, such as database design, query optimization, or even specific queries related to your database.
- Supports Multiple Databases: Works with local SQLite databases and remote MySQL databases.
- Easy to Use Interface: Simple, intuitive interface for both technical and non-technical users.
- Powered by OpenAI: Uses GPT-4 via OpenAI's API to provide intelligent responses to SQL-related queries.
## Installation
To get started, install the required dependencies:
```
pip install -r requirements.txt
```

## How to Use
1. Set OpenAI API Key: In the app, you'll need to provide your OpenAI API key.
2. Choose a Database:
  - Use the sidebar to select either an SQLite or MySQL database.
  - For SQLite, a student.db file will be used automatically.
  - For MySQL, provide connection details such as the host, username, password, and database name.
3. Ask SQL Queries: You can now ask the chatbot anything SQL-related:
- "What is database normalization?"
- "Can you help me write a JOIN query?"
- "Explain how indexes work in SQL."

