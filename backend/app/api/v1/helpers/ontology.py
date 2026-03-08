
from sqlmodel import  Session

import rdflib
from rdflib import RDF, RDFS, OWL
from rdflib.term import BNode

from app.models.ontology import Ontology, Class, Property, Individual
from app.api.v1.helpers.rdf import safe_label, safe_qname


def get_depth(g: rdflib.Graph, cls, depth=0, visited=None) -> int:
    if visited is None:
        visited = set()
    if cls in visited:
        return depth
    visited.add(cls)
    parent = g.value(cls, RDFS.subClassOf)
    if not parent or parent == cls:
        return depth
    return get_depth(g, parent, depth + 1, visited)


def _detect_ontology_type(g: rdflib.Graph) -> str:
    """Returns 'owl' or 'rdfs' based on file content"""
    owl_classes = list(g.subjects(RDF.type, OWL.Class))
    owl_props   = list(g.subjects(RDF.type, OWL.ObjectProperty))
    if owl_classes or owl_props:
        return "owl"
    return "rdfs"


def _compute_ontology_details(
    g: rdflib.Graph,
    db_onto: Ontology,
    session: Session
) -> None:
    """Parse rdflib graph and insert classes, properties, individuals into DB"""

    onto_type = _detect_ontology_type(g)

    # ── Classes ──────────────────────────────────────────────────────
    class_uris = set()
    if onto_type == "owl":
        class_uris = {c for c in g.subjects(RDF.type, OWL.Class) if not isinstance(c, BNode)}
    else:
        class_uris = {c for c in g.subjects(RDF.type, RDFS.Class) if not isinstance(c, BNode)}

    # count children per class
    children_map: dict[str, int] = {}
    for cls in class_uris:
        children_map[str(cls)] = len([
            c for c in g.subjects(RDFS.subClassOf, cls)
            if not isinstance(c, BNode)
        ])

    for cls in class_uris:
        individuals_of_class = [
            i for i in g.subjects(RDF.type, cls)
            if not isinstance(i, BNode)
        ]
        db_class = Class(
            ontology_id     = db_onto.id,
            uri             = str(cls),
            label           = safe_label(g, cls),
            prefix_form     = safe_qname(g, cls),
            parent_uri      = str(g.value(cls, RDFS.subClassOf)) if g.value(cls, RDFS.subClassOf) else None,
            children_count  = children_map.get(str(cls), 0),
            is_abstract     = len(individuals_of_class) == 0,
            depth           = get_depth(g, cls),
        )
        session.add(db_class)

    # ── Properties ───────────────────────────────────────────────────
    if onto_type == "owl":
        prop_types = [
            (OWL.ObjectProperty,    "owl:ObjectProperty"),
            (OWL.DatatypeProperty,  "owl:DatatypeProperty"),
            (OWL.AnnotationProperty,"owl:AnnotationProperty"),
        ]
        for prop_type, type_label in prop_types:
            for prop in g.subjects(RDF.type, prop_type):
                if isinstance(prop, BNode):
                    continue
                domain = g.value(prop, RDFS.domain)
                range_ = g.value(prop, RDFS.range)
                db_prop = Property(
                    ontology_id = db_onto.id,
                    uri         = str(prop),
                    label       = safe_label(g, prop),
                    prefix_form = safe_qname(g, prop),
                    type        = type_label,
                    domain      = safe_qname(g, domain) if domain else None,
                    range       = safe_qname(g, range_) if range_ else None,
                )
                session.add(db_prop)
    else:
        for prop in g.subjects(RDF.type, RDF.Property):
            if isinstance(prop, BNode):
                continue
            domain = g.value(prop, RDFS.domain)
            range_ = g.value(prop, RDFS.range)
            db_prop = Property(
                ontology_id = db_onto.id,
                uri         = str(prop),
                label       = safe_label(g, prop),
                prefix_form = safe_qname(g, prop),
                type        = "rdf:Property",
                domain      = safe_qname(g, domain) if domain else None,
                range       = safe_qname(g, range_) if range_ else None,
            )
            session.add(db_prop)

    # ── Individuals (OWL only) ────────────────────────────────────────
    if onto_type == "owl":
        for ind in g.subjects(RDF.type, OWL.NamedIndividual):
            if isinstance(ind, BNode):
                continue
            rdf_type = g.value(ind, RDF.type)
            prop_count = len(list(g.predicate_objects(ind)))
            db_ind = Individual(
                ontology_id    = db_onto.id,
                uri            = str(ind),
                label          = safe_label(g, ind),
                prefix_form    = safe_qname(g, ind),
                rdf_type       = safe_qname(g, rdf_type) if rdf_type else None,
                property_count = prop_count,
            )
            session.add(db_ind)

    # ── Update counts on ontology row ────────────────────────────────
    db_onto.classes_count     = len(class_uris)
    db_onto.properties_count  = len(list(g.subjects(RDF.type, RDF.Property))) if onto_type == "rdfs" else (
        len(list(g.subjects(RDF.type, OWL.ObjectProperty))) +
        len(list(g.subjects(RDF.type, OWL.DatatypeProperty)))
    )
    db_onto.individuals_count = len(list(g.subjects(RDF.type, OWL.NamedIndividual))) if onto_type == "owl" else 0

    session.add(db_onto)
    session.commit()