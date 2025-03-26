import streamlit as st
import pandas as pd
from agents.workflow import setup_workflow

# Streamlit UI Setup
st.set_page_config(layout="wide")
st.title("SQL Query Generator & Executor")

 
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Database Connection")
    host = st.text_input("enter host")
    root = st.text_input("root")
    password = st.text_input("Enter MySQL Password", type="password")
    database = st.text_input("Enter Database Name")
    connect_btn = st.button("Connect")

with col2:
    st.header("Ask a Question")
    question = st.text_area("Enter your question")
    submit_btn = st.button("Submit")

# Store credentials in session state
if connect_btn:
    st.session_state["db_password"] = password
    st.session_state["db_name"] = database
    st.session_state["db_host"] = localhost
    st.session_state["db_user"] = root
    st.success("Database connection details saved!")

if submit_btn:
    if "db_password" not in st.session_state or "db_name" not in st.session_state:
        st.error("Please enter database credentials first!")
    elif not question:
        st.error("Please enter a question!")
    else:
        # ✅ Run Workflow with User Inputs
        workflow = setup_workflow()
        state = workflow.invoke({
            "host": "localhost",
            "user": "root",
            "password": st.session_state["db_password"],
            "database": st.session_state["db_name"],
            "user_q": question
        })

        query = state["query"]
        result_df = state["result"]

        st.subheader("Generated Query")
        st.code(query, language="sql")

        # ✅ Ensure result is a valid DataFrame
        if not result_df.empty:
            st.subheader("Query Result")
            st.dataframe(result_df)
        else:
            st.error("Query returned no results!")
