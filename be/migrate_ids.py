from app.database import db
from uuid import uuid4

def migrate_ids():
    session = db.get_session()
    try:
        # Find all Person nodes without an id property
        result = session.run("MATCH (n:Person) WHERE n.id IS NULL RETURN n")
        count = 0
        for record in result:
            node = record["n"]
            # Generate a new UUID
            new_id = str(uuid4())
            # Update the node
            # We use elementId(n) or id(n) depending on version, but here we can just match by internal ID from the node object if we are careful, 
            # or better yet, do it in a single query if possible, but python iteration is safer for unique UUID generation per node.
            
            # Using the element_id is the modern way in neo4j driver 5.x, but let's see what we have.
            # The previous output showed element_id.
            
            session.run("MATCH (n:Person) WHERE elementId(n) = $eid SET n.id = $new_id", eid=node.element_id, new_id=new_id)
            count += 1
            print(f"Updated node {node.get('name', 'Unknown')} with id {new_id}")
            
        print(f"Migration complete. Updated {count} nodes.")
    finally:
        session.close()
        db.close()

if __name__ == "__main__":
    migrate_ids()
