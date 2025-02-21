# Remove imports from the top
from fastapi import APIRouter

router = APIRouter()

@router.get("/recommendations")
def get_recommendations():
    from app.services import generate_recommendations  # Import inside the function
    return generate_recommendations()
