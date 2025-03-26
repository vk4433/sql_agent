from langgraph.graph import StateGraph, END, START
from typing import TypedDict
from dotenv import load_dotenv
import os
import pandas as pd
import google.generativeai as genai

load_dotenv()

from agents.tabcol import databases
from agents.insert import cud_operation
from agents.select_query import select_operation
from agents.query_writer import query_generator

genai.configure(api_key=os.getenv("google"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

class WorkflowState(TypedDict):
    schema: str
    user_q: str
    query: str
    host: str
    user: str
    password: str
    database: str
    result: pd.DataFrame  # ✅ Added result field

# ✅ Fetch schema (with database credentials)
def fetch_schema(state: WorkflowState) -> WorkflowState:
    schema = databases(state["host"], state["user"], state["password"], state["database"])
    return {
        "schema": schema,
        "query": "",
        "user_q": state["user_q"],
        "host": state["host"],
        "user": state["user"],
        "password": state["password"],
        "database": state["database"],
        "result": pd.DataFrame()   
    }

 
def generate_query(state: WorkflowState) -> WorkflowState:
    query = query_generator(state["schema"], state["user_q"])
    return {**state, "query": query}


def execute_query(state: WorkflowState) -> WorkflowState:
    query = state["query"]
    host, user, password, database = state["host"], state["user"], state["password"], state["database"]

    try:
        if query.lower().startswith(("select", "show", "describe")):
            result = select_operation(query, host, user, password, database)
        else:
            result = cud_operation(query, host, user, password, database)
            result = pd.DataFrame({"Status": [result]})   

        return {**state, "result": result}

    except Exception as e:
        return {**state, "result": pd.DataFrame({"Error": [str(e)]})}   

# ✅ Setup LangGraph workflow
def setup_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("fetch_schema", fetch_schema)
    graph.add_node("generate_query", generate_query)
    graph.add_node("execute_query", execute_query)

    graph.set_entry_point("fetch_schema")
    graph.add_edge("fetch_schema", "generate_query")
    graph.add_edge("generate_query", "execute_query")
    graph.add_edge("execute_query", END)

    return graph.compile()
