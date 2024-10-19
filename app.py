import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3

st.set_page_config(page_title="SQL Database Chat Assistant", page_icon="💬")
st.title("SQL Database Chat Assistant")

# Welcome message
st.write("👋 Welcome! This chatbot is here to help you with your SQL queries. You can Connect with your MySQL Database and chat with it!")

# Instructions and example questions
st.write("## Instructions:")
st.write("Feel free to ask me questions like:")
st.write("- What is SQL?")
st.write("- Can you help me with a specific SQL query?")
st.write("- Explain database normalization.")
st.write("- Also Questions related to your Database..")

# Database options
DB_OPTIONS = {
    "SQLite": "Use SQLite Database (student.db)",
    "MySQL": "Connect to MySQL Database"
}

# Sidebar for database selection and configuration
st.sidebar.header("Database Configuration")
selected_db = st.sidebar.radio("Choose a database:", list(DB_OPTIONS.values()))

if DB_OPTIONS["MySQL"] in selected_db:
    st.sidebar.subheader("MySQL Connection Details")
    mysql_host = st.sidebar.text_input("Host")
    mysql_user = st.sidebar.text_input("User  ")
    mysql_password = st.sidebar.text_input("Password", type="password")
    mysql_db = st.sidebar.text_input("Database Name")
else:
    st.sidebar.info("Using local SQLite database: student.db")

# OpenAI API Key input
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

@st.cache_resource(ttl="2h")
def configure_db(db_option):
    if DB_OPTIONS["SQLite"] in db_option:
        db_path = (Path(__file__).parent / "student.db").absolute()
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

db = configure_db(selected_db)

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

# Initialize or clear chat history
if "messages" not in st.session_state or st.sidebar.button("Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm your SQL Database Assistant. How can I help you today?"}]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
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