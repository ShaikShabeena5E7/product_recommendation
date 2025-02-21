from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
import json
import logging
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

from app.llm_recommender import generate_recommendations, cache_recommendations, get_cached_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(dotenv_path="app/.env")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    logging.error("HF_TOKEN is not set. Check your .env file or environment variables.")
    raise ValueError("HF_TOKEN is not set.")
else:
    print(f"Loaded HF_TOKEN: {HF_TOKEN[:5]}****")  # Print partial value for debugging

# Initialize FastAPI
app = FastAPI()

# Sample product dataset
products = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "description": "Noise-canceling wireless headphones with long battery life.", "price": 150},
    {"id": 2, "name": "Smartwatch", "category": "Wearable Tech", "description": "Waterproof smartwatch with heart rate monitoring and GPS.", "price": 200},
    {"id": 3, "name": "Yoga Mat", "category": "Fitness", "description": "Eco-friendly non-slip yoga mat for all fitness levels.", "price": 50},
    {"id": 4, "name": "Resistance Bands", "category": "Fitness", "description": "Set of resistance bands for home workouts.", "price": 30}
]

# Request model
class UserRequest(BaseModel):
    user_id: str
    browsing_history: List[str]


    # Fetch products from SQLite based on browsing history
def fetch_products(browsing_history):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Use browsing history to filter relevant products
    query = f"SELECT id, name, category, description, price FROM products WHERE category IN ({','.join(['?']*len(browsing_history))})"
    cursor.execute(query, browsing_history)

    products = [{"id": row[0], "name": row[1], "category": row[2], "description": row[3], "price": row[4]} for row in cursor.fetchall()]

    conn.close()
    return products[:3]  # Return top 3 matches

@app.post("/recommendations")
async def get_recommendations(request: UserRequest):
    try:
        logging.info(f"User ID: {request.user_id}, Browsing History: {request.browsing_history}")

        # Fetch recommendations from SQLite
        recommendations = fetch_products(request.browsing_history)

        if not recommendations:
            raise HTTPException(status_code=404, detail="No relevant products found.")

        return JSONResponse(content={"user_id": request.user_id, "recommendations": json.loads(json.dumps(recommendations, separators=(",", ":")))})
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



    