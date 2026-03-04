
import uuid
from sqlmodel import SQLModel, Field




class QueryOntology(SQLModel, table=True):
    __tablename__ = "query_ontologies"

    query_id: uuid.UUID = Field(foreign_key="sparql_history.id", primary_key=True)
    ontology_id: uuid.UUID = Field(foreign_key="ontologies.id", primary_key=True)

