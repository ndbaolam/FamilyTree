from app.database import db

def inspect_data():
    session = db.get_session()
    try:
        result = session.run("MATCH (n:Person) RETURN n LIMIT 5")
        for record in result:
            node = record["n"]
            print(f"Node labels: {node.labels}")
            print(f"Node properties: {dict(node)}")
            print(f"Node ID (element_id): {node.element_id}")
            print("-" * 20)
    finally:
        session.close()
        db.close()

if __name__ == "__main__":
    inspect_data()
