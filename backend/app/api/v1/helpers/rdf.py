

from pathlib import Path
from typing import Optional
from rdflib.namespace import RDF, RDFS, OWL, XSD
import rdflib
from rdflib import URIRef, Literal, BNode

from sqlmodel import Session
from app.models.rdf import Graph, Subject, Predicate, Object


_WELL_KNOWN_PREFIXES: dict[str, str] = {
    str(RDF):   "rdf",
    str(RDFS):  "rdfs",
    str(OWL):   "owl",
    str(XSD):   "xsd",
    "http://xmlns.com/foaf/0.1/":          "foaf",
    "http://schema.org/":                  "schema",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://purl.org/dc/elements/1.1/":    "dc",
    "http://purl.org/dc/terms/":           "dcterms",
    "http://www.w3.org/ns/prov#":          "prov",
}

_FORMAT_MAP: dict[str, str] = {
    ".ttl":    "turtle",
    ".n3":     "n3",
    ".nt":     "nt",
    ".nq":     "nquads",
    ".trig":   "trig",
    ".rdf":    "xml",
    ".xml":    "xml",
    ".owl":    "xml",
    ".jsonld": "json-ld",
    ".json":   "json-ld",
    ".trix":   "trix",
}
_MIME_FORMAT_MAP: dict[str, str] = {
    "text/turtle":                    "turtle",
    "application/x-turtle":          "turtle",
    "text/n3":                        "n3",
    "application/n-triples":          "nt",
    "application/n-quads":            "nquads",
    "application/trig":               "trig",
    "application/rdf+xml":            "xml",
    "application/owl+xml":            "xml",
    "application/ld+json":            "json-ld",
    "application/json":               "json-ld",
}


def _detect_rdf_format(filename: str, content_type: Optional[str]) -> str:
    ext = Path(filename).suffix.lower()
    if ext in _FORMAT_MAP:
        return _FORMAT_MAP[ext]
    if content_type and content_type in _MIME_FORMAT_MAP:
        return _MIME_FORMAT_MAP[content_type]
    return "turtle" 



def _prefix_form(uri: str, ns_bindings: dict[str, str]) -> Optional[str]:
    """Return 'prefix:local' if the URI matches a known namespace, else None."""
    for ns_uri, prefix in ns_bindings.items():
        if uri.startswith(ns_uri):
            local = uri[len(ns_uri):]
            if local:
                return f"{prefix}:{local}"
    return None


def _build_ns_bindings(g: rdflib.Graph) -> dict[str, str]:
    """Merge graph-declared namespaces with well-known ones (graph wins on conflict)."""
    bindings: dict[str, str] = dict(_WELL_KNOWN_PREFIXES)
    for prefix, ns in g.namespaces():
        if prefix:
            bindings[str(ns)] = str(prefix)
    return bindings

def _node_kind(node) -> str:
    if isinstance(node, URIRef):
        return "uri"
    if isinstance(node, BNode):
        return "blank"
    return "literal"



def _compute_graph_details(
    rdf_graph: rdflib.Graph,
    db_graph: Graph,
    db: Session,
) -> None:

    ns_bindings = _build_ns_bindings(rdf_graph)

    #   subjecturi -> { predicate_count, rdf_type}
    subj_map: dict[str, dict] = {}
    # predicate uri -> { usage_count, domain_set, range_set}
    pred_map: dict[str, dict] = {}
    # object value ->  { kind,,, datatype, language, referenced_by, prefix_form}
    obj_map: dict[str, dict] = {}

    RDF_TYPE = str(RDF.type)

    for s, p, o in rdf_graph:
        s_str = str(s)
        p_str = str(p)
        o_str = str(o)

        if s_str not in subj_map:
            subj_map[s_str] = {"predicate_count": 0, "rdf_type": None}
        subj_map[s_str]["predicate_count"] += 1
        if p_str == RDF_TYPE and subj_map[s_str]["rdf_type"] is None:
            subj_map[s_str]["rdf_type"] = o_str

        if p_str not in pred_map:
            pred_map[p_str] = {"usage_count": 0, "domains": set(), "ranges": set()}
        pred_map[p_str]["usage_count"] += 1

        if p_str == str(RDFS.domain):
            if s_str in pred_map:
                pred_map[s_str]["domains"].add(o_str)
        if p_str == str(RDFS.range):
            if s_str in pred_map:
                pred_map[s_str]["ranges"].add(o_str)

        kind = _node_kind(o)
        obj_key = o_str  

        if obj_key not in obj_map:
            obj_map[obj_key] = {
                "kind": kind,
                "datatype": None,
                "language": None,
                "prefix_form": None,
                "referenced_by": 0,
            }
            if kind == "uri":
                obj_map[obj_key]["prefix_form"] = _prefix_form(o_str, ns_bindings)
            elif kind == "literal":
                lit: Literal = o  
                if lit.datatype:
                    obj_map[obj_key]["datatype"] = str(lit.datatype)
                if lit.language:
                    obj_map[obj_key]["language"] = lit.language
        obj_map[obj_key]["referenced_by"] += 1

    for p_str, info in pred_map.items():
        info["domain"] = ", ".join(sorted(info.pop("domains"))) or None
        info["range"]  = ", ".join(sorted(info.pop("ranges"))) or None

    db.bulk_insert_mappings(
        Subject,
        [
            {
                "graph_id":        db_graph.id,
                "uri":             uri,
                "prefix_form":     _prefix_form(uri, ns_bindings),
                "rdf_type":        info["rdf_type"],
                "predicate_count": info["predicate_count"],
            }
            for uri, info in subj_map.items()
        ],
    )

    db.bulk_insert_mappings(
        Predicate,
        [
            {
                "graph_id":    db_graph.id,
                "uri":         uri,
                "prefix_form": _prefix_form(uri, ns_bindings),
                "usage_count": info["usage_count"],
                "domain":      info["domain"],
                "range":       info["range"],
            }
            for uri, info in pred_map.items()
        ],
    )

    db.bulk_insert_mappings(
        Object,
        [
            {
                "graph_id":      db_graph.id,
                "value":         value,
                "kind":          info["kind"],
                "prefix_form":   info["prefix_form"],
                "datatype":      info["datatype"],
                "language":      info["language"],
                "referenced_by": info["referenced_by"],
            }
            for value, info in obj_map.items()
        ],
    )

    db.commit()