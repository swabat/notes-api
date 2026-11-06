from fastapi import FastAPI

from app.database import engine
from app.models.base import Base
from app.models import Note
from app.routers.notes import router as notes_router
from app.routers.categories import router as categories_router


app = FastAPI(
    title="Notes API"
)

app.include_router(notes_router)
app.include_router(categories_router)
 
@app.get("/")
def root():
    return {"message": "Notes API is running"}