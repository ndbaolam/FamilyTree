from fastapi import FastAPI
from .db import driver

app = FastAPI()

@app.get("/")
def health():
    with driver.session() as session:
        result = session.run("RETURN 'Neo4j connected' AS msg")
        return {"status": result.single()["msg"]}
