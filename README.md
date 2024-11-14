# SQL Database Chat Assistant 💬

View the YouTube video here: [SQL Database Chat Assistant Video](https://www.youtube.com/watch?v=HgvTYbv_xUk)

# Abstract
The SQL Database Chat Assistant is a conversational application that allows users to interact with their databases using natural language. Built with Streamlit for the user interface, LangChain for handling SQL interactions, and OpenAI's GPT-4 for language understanding, this assistant transforms SQL querying into a user-friendly chat experience.

## Why Use the SQL Database Chat Assistant?

### 1. Support for Multiple Databases
The assistant works with both **SQLite** and **MySQL** databases, giving you flexibility whether you’re working locally or with a remote setup. It’s easy to switch between databases, making it ideal for testing, development, and real-time SQL work without the hassle of complex configurations.

### 2. Intuitive, Chat-Based Interface
With a clean and simple chat interface, you can ask questions as if you’re talking to a human assistant. This conversational design lets you:
- Pose SQL queries in plain language.
- Ask general database questions.
- Even troubleshoot specific issues, making it a great learning tool and a helpful companion for complex tasks.

### 3. Powered by OpenAI's GPT-4
The assistant leverages **GPT-4’s advanced language model** to provide intelligent, detailed responses. It’s capable of understanding questions beyond typical SQL queries, offering insights into topics like database normalization, data manipulation, and optimization tips. This makes it an educational resource as much as it is a functional assistant.

## Practical Uses
Whether you're a data science student, a developer, or a business analyst, the SQL Database Chat Assistant can be a game-changer in your work:
- **Learning SQL**: Get explanations of SQL concepts and step-by-step guidance on query formation.
- **Data Analysis**: Quickly extract insights from your data, with the option to filter and manipulate as needed.
- **Database Troubleshooting**: Find solutions to SQL-related issues, such as syntax errors or inefficient queries.

This assistant not only saves time but also makes working with SQL more accessible to everyone. Connect your own database to get tailored responses or use the example databases provided to explore SQL concepts interactively.

You can check the app here: [SQL Database Chat Assistant](https://sql-database-chat-assistant-6thdvjxf9dypct3rdxltcy.streamlit.app/)

> **Note**: To connect to a MySQL database, it’s recommended to run the app locally for the best compatibility.

## Example Queries
- "What is SQL?"
- "Can you help me with a specific SQL query?"
- "Explain database normalization."
- Connect your own MySQL database to explore more!

## Code Overview
## 1. Configuring the Database Connection
 Uses the `configure_db` function to manage connections, supporting both SQLite (local) and MySQL (remote) databases.

```Python
@st.cache_resource(ttl="2h")
def configure_db(db_option, sqlite_db=None):
    if DB_OPTIONS["SQLite"] in db_option:
        db_path = (Path(__file__).parent / sqlite_db).absolute()
        db_uri = f"sqlite:///{db_path}"
    elif DB_OPTIONS["MySQL"] in db_option:
        if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        db_uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    else:
        st.error("Invalid database option")
        st.stop()
    
    return SQLDatabase.from_uri(db_uri)
```

## 2. Creating the Chat Agent
 Through LangChain, GPT-4 serves as the conversational agent, providing zero-shot responses to SQL queries.

```Python
def create_agent(api_key, db):
    if not api_key.strip():
        st.error("Please enter your OpenAI API Key.")
        return None

    llm = ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=api_key)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
```
The `AgentType.ZERO_SHOT_REACT_DESCRIPTION` allows the agent to make intelligent SQL-related responses based on a zero-shot learning approach.

## 3. Handling User Queries
Captures user queries, processes responses via GPT-4, and displays answers within a chat-based interface for a seamless experience.

```Python
user_query = st.chat_input(placeholder="Ask me anything about databases...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message ("user").write(user_query)

    if openai_api_key.strip():
        agent = create_agent(openai_api_key, db)
        if agent:
            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container()) 
                response = agent.run(user_query, callbacks=[st_callback])
                if response.startswith("I don't know"):
                    st.write("Sorry, I'm not familiar with that topic. However, I can suggest some resources or general advice related to databases.")
                else:
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
    else:
        st.error("Please enter your OpenAI API Key.")
```
This setup ensures real-time interaction, adding messages to the session state and displaying responses as part of the conversation flow.

## Demostration 
![sql](https://github.com/user-attachments/assets/90cae24a-afae-443e-b43e-6ce058c26599)

![sql2](https://github.com/user-attachments/assets/a9f7e9d2-14fd-4fbd-93a5-95249a8cbeb7)

![sql4](https://github.com/user-attachments/assets/6cdce97a-784b-45fa-abf3-c64c5bc7b476)

![sql5](https://github.com/user-attachments/assets/19812132-1f0c-4ccf-8c78-4e1978f59cca)

