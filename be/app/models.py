from pydantic import BaseModel, Field
from typing import Optional, List

class PersonBase(BaseModel):
    name: str = Field(..., example="John Doe")
    gender: str = Field(..., example="Male")
    birth_date: Optional[str] = Field(None, example="1980-01-01")
    death_date: Optional[str] = Field(None, example="2050-01-01")
    biography: Optional[str] = Field(None, example="A short biography.")
    avatar_url: Optional[str] = Field(None, example="http://example.com/avatar.jpg")

class PersonCreate(PersonBase):
    pass

class PersonUpdate(PersonBase):
    pass

class Person(PersonBase):
    id: str

class RelationshipCreate(BaseModel):
    from_person_id: str
    to_person_id: str
    relationship_type: str = Field(..., pattern="^(PARENT_OF|MARRIED_TO)$")

class GraphNode(BaseModel):
    id: str
    label: str
    data: dict

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str
    data: dict = {}

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
