# backend/main.py

from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if it exists)
load_dotenv()

# Initialize the main FastAPI application
app = FastAPI(title="In-House ERP API", version="0.1.0")

# Define a simple endpoint to test the server is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the ERP Backend! API is running."}

# Optional: Entry point for running the server locally (for simple testing)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
