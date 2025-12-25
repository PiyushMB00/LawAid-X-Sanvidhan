from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.post("/trigger")
def trigger_sos(user: str = "anonymous"):
    return {
        "message": "SOS triggered successfully",
        "user": user,
        "time": datetime.now()
    }
