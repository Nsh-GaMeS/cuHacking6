import os
from dotenv import load_dotenv, find_dotenv
import requests
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from routers.auth import get_transactions, get_db
from google import genai
import sys
sys.path.append("..")

# Define a new router for AI-related endpoints
router = APIRouter(
    prefix="/gemini",
    tags=["prompt"],
    responses={401: {"user": "Not authorized"}}
)

# Constants for the Gemini API
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_KEY")  

# Function to analyze spending by categorizing transactions
def analyze_spending(transactions: json) -> dict:
    categories = {}
    for transaction in transactions:
        category = transactions['category']
        amount = transactions['amount']
        store = transactions['store']
        
        if category not in categories:
            categories[category] = {
                'total_spent': 0,
                'stores': {}
            }
        
        categories[category]['total_spent'] += amount
        if store not in categories[category]['stores']:
            categories[category]['stores'][store] = 0
        categories[category]['stores'][store] += amount
    
    return categories

# Function to suggest savings based on analyzed spending
def suggest_savings(categories) -> str:
    client = genai.Client(api_key = GEMINI_API_KEY)
    with open("./prompt.txt", "r") as file:
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = json.dumps(categories, indent=4) + " " + file.read(),
        )
    
        
    return response.text

# Endpoint to analyze a user's spending and provide feedback
@router.get("/analyze_spending")
def analyze_user_spending(user_id: int, db: Session = Depends(get_db)):
    transactions = get_transactions(user_id, db)
    if "message" in transactions and transactions["message"] == "User not found":
        return transactions
    
    categories = analyze_spending(transactions)
    suggestions = suggest_savings(categories)
    
    return {
        "suggestions": suggestions
    }
