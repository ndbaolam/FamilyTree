from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from neo4j import Session
from uuid import uuid4
from typing import List

from app.database import get_db_session, db
from app.models import Person, PersonCreate, PersonUpdate, RelationshipCreate, GraphData, GraphNode, GraphEdge


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
def shutdown_event():
    db.close()

@app.post("/people", response_model=Person)
def create_person(person: PersonCreate, session: Session = Depends(get_db_session)):
    query = """
    CREATE (p:Person {
        id: $id,
        name: $name,
        gender: $gender,
        birth_date: $birth_date,
        death_date: $death_date,
        biography: $biography,
        avatar_url: $avatar_url
    })
    RETURN p
    """
    person_id = str(uuid4())
    result = session.run(query, id=person_id, **person.dict())
    record = result.single()
    if not record:
        raise HTTPException(status_code=500, detail="Failed to create person")
    
    node = record["p"]
    return Person(**dict(node))

@app.get("/people/{person_id}", response_model=Person)
def get_person(person_id: str, session: Session = Depends(get_db_session)):
    query = "MATCH (p:Person {id: $id}) RETURN p"
    result = session.run(query, id=person_id)
    record = result.single()
    if not record:
        raise HTTPException(status_code=404, detail="Person not found")
    
    node = record["p"]
    return Person(**dict(node))

@app.put("/people/{person_id}", response_model=Person)
def update_person(person_id: str, person: PersonUpdate, session: Session = Depends(get_db_session)):
    query = """
    MATCH (p:Person {id: $id})
    SET p += $props
    RETURN p
    """
    result = session.run(query, id=person_id, props=person.dict(exclude_unset=True))
    record = result.single()
    if not record:
        raise HTTPException(status_code=404, detail="Person not found")
    
    node = record["p"]
    return Person(**dict(node))

@app.delete("/people/{person_id}")
def delete_person(person_id: str, session: Session = Depends(get_db_session)):
    query = "MATCH (p:Person {id: $id}) DETACH DELETE p"
    session.run(query, id=person_id)
    return {"message": "Person deleted"}

@app.post("/relationships")
def create_relationship(rel: RelationshipCreate, session: Session = Depends(get_db_session)):
    query = f"""
    MATCH (p1:Person {{id: $from_id}}), (p2:Person {{id: $to_id}})
    MERGE (p1)-[r:{rel.relationship_type}]->(p2)
    RETURN r
    """
    result = session.run(query, from_id=rel.from_person_id, to_id=rel.to_person_id)
    if not result.single():
        raise HTTPException(status_code=404, detail="One or both persons not found")
    return {"message": "Relationship created"}

@app.delete("/relationships/{relationship_id}")
def delete_relationship(relationship_id: str, session: Session = Depends(get_db_session)):
    query = "MATCH ()-[r]-() WHERE elementId(r) = $id OR id(r) = toInteger($id) DELETE r"
    session.run(query, id=relationship_id)
    return {"message": "Relationship deleted"}

@app.get("/tree", response_model=GraphData)
def get_tree(session: Session = Depends(get_db_session)):
    # Fetch all nodes and relationships
    # Fetch all nodes
    query_nodes = "MATCH (n:Person) RETURN n"
    nodes_result = session.run(query_nodes)
    
    nodes = {}
    for record in nodes_result:
        n = record["n"]
        if n and n.get("id"):
             nodes[n["id"]] = GraphNode(
                id=n["id"],
                label=n.get("name", "Unknown"),
                data=dict(n)
            )

    # Fetch all relationships
    query_edges = "MATCH (n:Person)-[r]->(m:Person) RETURN n, r, m"
    edges_result = session.run(query_edges)
    
    edges = []
    for record in edges_result:
        n = record["n"]
        r = record["r"]
        m = record["m"]
        
        # Ensure source/target exist in our nodes list to avoid broken edges
        if n["id"] in nodes and m["id"] in nodes:
            edges.append(GraphEdge(
                id=str(r.element_id) if hasattr(r, 'element_id') else str(r.id), 
                source=n["id"],
                target=m["id"],
                label=r.type,
                data=dict(r)
            ))
    
    return GraphData(nodes=list(nodes.values()), edges=edges)
