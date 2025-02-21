import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import redis
import json
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse


# Setup logging
logging.basicConfig(level=logging.INFO)

# Connect to Redis
try:
    redis_client = redis.Redis(
        host="redis-13612.c212.ap-south-1-1.ec2.redns.redis-cloud.com",
        port=13612,
        decode_responses=True,
        username="default",
        password="2C6B34rpKS0W1tKHacVz7Tr8HA6oqJ0M"
    )
except redis.ConnectionError:
    logging.error("Failed to connect to Redis. Make sure Redis is running.")
    redis_client = None
    redis_client.ping()
    logging.info("Connected to Redis successfully.")
except redis.ConnectionError:
    logging.error("Failed to connect to Redis. Make sure Redis is running.")
    redis_client = None

# Load a lightweight model for faster response
MODEL_NAME = "distilgpt2"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.to("cpu")  # Run on CPU for efficiency
    logging.info(f"Loaded model: {MODEL_NAME}")
except Exception as e:
    logging.error(f"Error loading model: {str(e)}")
    tokenizer, model = None, None

# Sample product dataset
products = [
    {"id": 1, "name": "Wireless Headphones", "category": "Electronics", "description": "Noise-canceling wireless headphones with long battery life.", "price": 150},
    {"id": 2, "name": "Smartwatch", "category": "Wearable Tech", "description": "Waterproof smartwatch with heart rate monitoring and GPS.", "price": 200},
    {"id": 3, "name": "Yoga Mat", "category": "Fitness", "description": "Eco-friendly non-slip yoga mat for all fitness levels.", "price": 50},
    {"id": 4, "name": "Resistance Bands", "category": "Fitness", "description": "Set of resistance bands for home workouts.", "price": 30}
]

# Cache recommendations in Redis (Expire in 1 hour)
def cache_recommendations(user_id, recommendations):
    if redis_client:
        redis_client.setex(f"user:{user_id}:recommendations", 3600, json.dumps(recommendations))

# Retrieve cached recommendations
def get_cached_recommendations(user_id):
    if redis_client:
        cached = redis_client.get(f"user:{user_id}:recommendations")
        return json.loads(cached) if cached else None
    return None

# Request model
class UserRequest(BaseModel):
    user_id: str
    browsing_history: List[str]

# Generate recommendations based on browsing history
def generate_recommendations(browsing_history):
    if tokenizer is None or model is None:
        raise HTTPException(status_code=500, detail="LLM Model failed to load.")

    input_text = " ".join(browsing_history)  # Combine input categories
    inputs = tokenizer(input_text, return_tensors="pt")
    
    try:
        outputs = model.generate(**inputs, max_length=50)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logging.info(f"LLM Generated: {generated_text}")

        # Simulate matching from the dataset (modify as needed)
        recommended_products = [
            p for p in products if any(term.lower() in p["description"].lower() for term in generated_text.split())
        ]
        return recommended_products[:3]

    except Exception as e:
        logging.error(f"LLM Model error: {str(e)}")
        raise HTTPException(status_code=500, detail="LLM Model failed to generate recommendations.")

# FastAPI app
app = FastAPI()

@app.post("/recommendations")
async def get_recommendations(request: UserRequest):
    try:
        # Check Redis cache
        cached_recs = get_cached_recommendations(request.user_id)
        if cached_recs:
            logging.info(f"Cache hit for user {request.user_id}")
            return JSONResponse(content=json.loads(json.dumps({"user_id": request.user_id, "recommendations": cached_recs}, indent=2, separators=(",", ": "))))

        # Generate recommendations
        recommendations = generate_recommendations(request.browsing_history)
        # Log the recommendations to check what is being generated
        logging.info(f"Generated Recommendations: {recommendations}")

        if not recommendations:
            logging.error(f"No recommendations found for user {request.user_id} with history {request.browsing_history}")
            raise HTTPException(status_code=404, detail="No relevant products found.")
            
        # Cache recommendations
        cache_recommendations(request.user_id, recommendations)

        return JSONResponse(content=json.loads(json.dumps({"user_id": request.user_id, "recommendations": recommendations}, indent=2, separators=(",", ": "))))

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
