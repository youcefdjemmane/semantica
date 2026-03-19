# app/api/v1/routes/reasoning.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
import rdflib
import owlrl
import time
import uuid

from app.core.db import get_session
from app.models.rdf import Graph
from app.models.ontology import Ontology
from app.api.v1.helpers.rdf import safe_label, safe_qname

router = APIRouter(prefix="/reasoning", tags=["reasoning"])

FORMALISM_MAP = {
    "RDFS":        owlrl.RDFS_Semantics,
    "OWL-RL":      owlrl.OWLRL_Semantics,
    "RDFS+OWL-RL": owlrl.RDFS_OWLRL_Semantics,
    "OWL-QL":      owlrl.OWLRL_Semantics,
    "OWL-EL":      owlrl.OWLRL_Semantics,
    "OWL-DL":      owlrl.RDFS_OWLRL_Semantics,
}

class ReasoningRequest(BaseModel):
    graph_id:     uuid.UUID
    ontology_ids: list[uuid.UUID] = []
    formalism:    str              # "RDFS" | "OWL-RL" | "OWL-QL"


@router.post("/run")
def run_reasoning(
    body:    ReasoningRequest,
    session: Session = Depends(get_session)
):
    graph_row = session.get(Graph, body.graph_id)
    if not graph_row:
        raise HTTPException(status_code=404, detail="Graph not found.")

    g = rdflib.ConjunctiveGraph()
    try:
        g.parse(graph_row.file_path, format=graph_row.format)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to load graph: {exc}")

    for onto_id in body.ontology_ids:
        onto_row = session.get(Ontology, onto_id)
        if not onto_row:
            continue
        try:
            g.parse(onto_row.file_path, format=onto_row.format)
        except Exception:
            continue   # skip bad ontology, don't crash

    original_triples = set(g.triples((None, None, None)))

    semantics = FORMALISM_MAP.get(body.formalism)
    if not semantics:
        raise HTTPException(status_code=400, detail=f"Unknown formalism: {body.formalism}")

    start = time.time()
    try:
        owlrl.DeductiveClosure(semantics).expand(g)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {exc}")
    elapsed = round((time.time() - start) * 1000, 2)

    expanded_triples = set(g.triples((None, None, None)))
    inferred         = expanded_triples - original_triples

    grouped: dict[str, dict] = {}
    for s, p, o in inferred:
        key = str(s)
        if key not in grouped:
            grouped[key] = {
                "subject":     key,
                "label":       safe_label(g, s),
                "prefix_form": safe_qname(g, s),
                "triples":     []
            }
        grouped[key]["triples"].append({
            "predicate":       str(p),
            "predicate_label": safe_qname(g, p),
            "object":          str(o),
            "object_label":    safe_qname(g, o) if not isinstance(o, rdflib.term.Literal) else str(o),
            "object_type":     "literal" if isinstance(o, rdflib.term.Literal) else "uri",
        })

    # Sort subjects by number of new triples descending
    subjects_out = sorted(
        grouped.values(),
        key=lambda x: len(x["triples"]),
        reverse=True
    )

    return {
        "formalism":       body.formalism,
        "graph_name":      graph_row.name,
        "original_count":  len(original_triples),
        "inferred_count":  len(inferred),
        "total_count":     len(original_triples) + len(inferred),
        "execution_time":  elapsed,
        "subjects":        subjects_out,
    }