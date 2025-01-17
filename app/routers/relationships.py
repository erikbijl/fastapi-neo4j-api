from fastapi import APIRouter, HTTPException, Depends
from app.db import db

def get_db_session():
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()

router = APIRouter()

@router.post("/add_relationship/")
async def add_relationship(node1_id: str, node2_id: str, relationship_type: str, session = Depends(get_db_session)):
    query = (
        "MATCH (a), (b) "
        "WHERE a.id = $node1_id AND b.id = $node2_id "
        "CREATE (a)-[r:" + relationship_type + "]->(b) "
        "RETURN r"
    )
    try:
        result = session.run(query, node1_id=node1_id, node2_id=node2_id)
        return {"relationship_created": result.single()["r"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating relationship: {str(e)}")

@router.get("/count_relationships_per_type/")
async def count_relationships_per_type(rel_type: str, session = Depends(get_db_session)):
    query = f"MATCH p=()-[r:{rel_type}]->() RETURN COUNT(DISTINCT r) AS relationshipCount"
    try:
        result = session.run(query)
        count = result.single()["relationshipCount"]
        return {"relationship_count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting relationships: {str(e)}")

@router.delete("/remove_relationship/")
async def remove_relationship(node1_id: str, node2_id: str, relationship_type: str, session = Depends(get_db_session)):
    query = (
        "MATCH (a)-[r:" + relationship_type + "]->(b) "
        "WHERE a.id = $node1_id AND b.id = $node2_id "
        "DELETE r"
    )
    try:
        session.run(query, node1_id=node1_id, node2_id=node2_id)
        return {"message": "Relationship removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing relationship: {str(e)}")
