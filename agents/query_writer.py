from dotenv import load_dotenv
import os
import google.generativeai as genai
from agents.tabcol import databases
from agents.insert import cud_operation
from agents.select_query import select_operation

load_dotenv()

genai.configure(api_key=os.getenv("google"))

def query_generator(schema, user_q):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")
    
    prompt = f"""
    You are an expert in writing optimized and accurate MySQL queries.
    Given the following database schema:
    {schema}
    And the user's question:
    {user_q}
    Generate a valid MySQL query that correctly retrieves or manipulates the data.
    Ensure the query:
    - Uses proper SQL syntax.
    - Includes necessary joins, conditions, or aggregations and subquires etc..
    - Is efficient and avoids unnecessary complexity.
    - no information in scheema return wrong database selected
    Provide only the SQL query without any explanation, markdown, or code block formatting.
    """

    response = model.generate_content(prompt).text.strip()
    
    query = response.replace("```sql", "").replace("```", "").strip()
    
    return query


