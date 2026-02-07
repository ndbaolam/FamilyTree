from app.database import db

def inspect_edges():
    session = db.get_session()
    try:
        result = session.run("MATCH ()-[r]->() RETURN r LIMIT 5")
        for record in result:
            rel = record["r"]
            print(f"Type: {rel.type}")
            print(f"Properties: {dict(rel)}")
            print("-" * 20)
    finally:
        session.close()
        db.close()

if __name__ == "__main__":
    inspect_edges()
