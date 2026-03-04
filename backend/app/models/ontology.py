from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field,Relationship
from app.models.query_ontology import QueryOntology


if TYPE_CHECKING:
    from app.models.sparql import SparqlHistory
    
class Ontology(SQLModel, table=True):
    __tablename__ = "ontologies"

    id: uuid.UUID                   = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False)
    format: str = Field(nullable=False)
    file_name: str = Field(nullable=False)
    file_path: str = Field(nullable=False)
    file_size: int = Field(nullable=False)
    classes_count: int = Field(default=0)
    properties_count: int = Field(default=0)
    individuals_count: int = Field(default=0)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    classes : list["Class"] = Relationship(back_populates="ontology", cascade_delete=True)
    properties : list["Property"] = Relationship(back_populates="ontology", cascade_delete=True)
    individuals : list["Individual"] = Relationship(back_populates="ontology", cascade_delete=True)
    sparql_queries: List["SparqlHistory"] = Relationship(back_populates="ontologies", link_model=QueryOntology)


class Class(SQLModel, table=True):
    __tablename__ = "classes"

    id: uuid.UUID              = Field(default_factory=uuid.uuid4, primary_key=True)
    ontology_id: uuid.UUID     = Field(foreign_key="ontologies.id", nullable=False)
    uri: str = Field(nullable=False)
    label: Optional[str] = Field(default=None, nullable=True)
    prefix_form: Optional[str] = Field(default=None, nullable=True)
    parent_uri: Optional[str] = Field(default=None, nullable=True)
    children_count: int = Field(default=0)
    is_abstract: bool = Field(default=False)
    depth: int = Field(default=0)

    ontology: Optional[Ontology] = Relationship(back_populates="classes")

class Property(SQLModel, table=True):
    __tablename__ = "properties"

    id: uuid.UUID              = Field(default_factory=uuid.uuid4, primary_key=True)
    ontology_id: uuid.UUID     = Field(foreign_key="ontologies.id", nullable=False)
    uri: str = Field(nullable=False)
    label: Optional[str] = Field(default=None, nullable=True)
    prefix_form: Optional[str] = Field(default=None, nullable=True)
    type: Optional[str] = Field(default=None, nullable=True)        # owl:ObjectProperty | owl:DatatypeProperty
    domain: Optional[str] = Field(default=None, nullable=True)
    range: Optional[str] = Field(default=None, nullable=True)

    ontology: Optional[Ontology] = Relationship(back_populates="properties")


class Individual(SQLModel, table=True):
    __tablename__ = "individuals"
    
    id: uuid.UUID              = Field(default_factory=uuid.uuid4, primary_key=True)
    ontology_id: uuid.UUID     = Field(foreign_key="ontologies.id", nullable=False)
    uri: str = Field(nullable=False)
    label: Optional[str] = Field(default=None, nullable=True)
    prefix_form: Optional[str] = Field(default=None, nullable=True)
    rdf_type: Optional[str] = Field(default=None, nullable=True)
    property_count: int = Field(default=0)

    ontology: Optional[Ontology] = Relationship(back_populates="individuals")