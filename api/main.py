from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from .db_handler import execute_query
from .sql_generator import nl_to_sql
from fastapi.middleware.cors import CORSMiddleware


# Initialize the FastAPI app
app = FastAPI(
    title="Baseball Data API",
    description="An API to query MLB Statcast data using natural language.",
    version="0.1.0",
)

origins = [
    "http://localhost:3000", # Keep this for local development
    "https://fullcount-ai.vercel.app/", 
    "https://mlb-saas.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the request model using Pydantic. This ensures the request body is valid.
class QueryRequest(BaseModel):
    question: str
    previous_sql: str | None = None
    seasons: list[int] | None = None # Optional for future use

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Baseball Data API!"}

@app.post("/query")
async def handle_query(request: QueryRequest):
    """
    Receives a natural language question and returns structured data.
    
    **MVP Stub:** For now, it ignores the question and runs a hardcoded SQL query.
    """
    logging.info(f"Received query request for question: '{request.question}'")
    

    try:
        # 1. Generate SQL from the natural language question
        generated_sql = nl_to_sql(request.question, request.previous_sql)

        # 2. Execute the generated SQL
        results = execute_query(generated_sql)
        
        if not results:
            logging.info("Query executed successfully but returned no results.")
        
        return {"sql_query": generated_sql, "results": results}
    
    except Exception as e:
        logging.error(f"An internal server error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the query.")