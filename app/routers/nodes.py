from fastapi import APIRouter, HTTPException, Depends
from app.db import db

def get_db_session():
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

router = APIRouter()

@router.post("/create_node/")
async def create_node(node_id: str, properties: dict, session = Depends(get_db_session)):
    query = (
        "CREATE (n {id: $node_id, properties: $properties}) "
        "RETURN n"
    )
    try:
        result = session.run(query, node_id=node_id, properties=properties)
        return {"node_created": result.single()["n"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating node: {str(e)}")

@router.get("/count_nodes/")
async def count_nodes(session = Depends(get_db_session)):
    query = "MATCH (n) RETURN count(n) as node_count"
    try:
        result = session.run(query)
        count = result.single()["node_count"]
        return {"node_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting nodes: {str(e)}")

@router.delete("/delete_node/")
async def delete_node(node_id: str, session = Depends(get_db_session)):
    query = "MATCH (n {id: $node_id}) DETACH DELETE n"
    try:
        session.run(query, node_id=node_id)
        return {"message": "Node deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting node: {str(e)}")
