from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import uuid

from app.core.db import get_session
from app.models.namespace import AppNamespace

router = APIRouter(prefix="/namespaces", tags=["namespaces"])

@router.get("/", response_model=List[AppNamespace])
def get_namespaces(session: Session = Depends(get_session)):
    """Récupère tous les espaces de noms personnalisés."""
    return session.exec(select(AppNamespace)).all()

@router.post("/", response_model=AppNamespace)
def create_namespace(ns: AppNamespace, session: Session = Depends(get_session)):
    """Ajoute un nouvel espace de noms."""
    existing = session.exec(select(AppNamespace).where(AppNamespace.prefix == ns.prefix)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce préfixe existe déjà.")
    
    session.add(ns)
    session.commit()
    session.refresh(ns)
    return ns

@router.delete("/{ns_id}")
def delete_namespace(ns_id: uuid.UUID, session: Session = Depends(get_session)):
    """Supprime un espace de noms."""
    ns = session.get(AppNamespace, ns_id)
    if not ns:
        raise HTTPException(status_code=404, detail="Namespace non trouvé.")
    
    session.delete(ns)
    session.commit()
    return {"message": "Namespace supprimé avec succès."}
