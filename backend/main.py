# backend/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from dotenv import load_dotenv
import os
from app.main import app as main_app # Import the actual FastAPI app from app/main.py

# Load environment variables from the .env file (if it exists)
load_dotenv()

# This root main.py is primarily for local development and running the app.
# The actual FastAPI application logic resides in app/main.py.
app = main_app # Use the app imported from app/main.py

# Custom exception handler for Pydantic validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler to sanitize validation error messages,
    preventing sensitive data like passwords from being exposed.
    """
    errors = []
    for error in exc.errors():
        # Create a copy of the error to modify
        sanitized_error = error.copy()
        
        # Check if 'password' is in the location path and remove it from input
        if "password" in sanitized_error.get("loc", []):
            if "input" in sanitized_error:
                sanitized_error["input"] = {k: v for k, v in sanitized_error["input"].items() if k != "password"}
            sanitized_error["msg"] = "Field required (password omitted for security)" # Generic message
        
        errors.append(sanitized_error)
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )

# Optional: Entry point for running the server locally (for simple testing)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
