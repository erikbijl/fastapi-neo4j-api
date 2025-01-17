from fastapi import FastAPI
from app.routers import relationships
from app.routers import nodes

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Neo4j API"}

app.include_router(nodes.router, prefix="/nodes", tags=["Nodes"])
app.include_router(relationships.router, prefix="/relationships", tags=["Relationships"])
