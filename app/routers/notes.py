from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Note, Category
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse, status_code=201)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    if data.category_id is not None:
        category = db.query(Category).filter(
            Category.id == data.category_id
        ).first()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    db_note = Note(
        title=data.title,
        content=data.content,
        category_id=data.category_id
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def get_notes(
    category_id: int | None = None,
    is_archived: bool | None = None,
    db: Session = Depends(get_db),
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100)
):
    query = db.query(Note)

    if category_id is not None:
        query = query.filter(Note.category_id == category_id)

    if is_archived is not None:
        query = query.filter(Note.is_archived == is_archived)

    if search:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{search}%"),
                Note.content.ilike(f"%{search}%")
        )
    )
    return query.offset(skip).limit(limit).all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db)
):
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    data = note.model_dump(exclude_unset=True)

    if "category_id" in data and data["category_id"] is not None:
        category = db.query(Category).filter(
            Category.id == data["category_id"]
            ).first()

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    for field, value in data.items():
        setattr(db_note, field, value)

    db.commit()
    db.refresh(db_note)

    return db_note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()


@router.patch("/{note_id}/archive", response_model=NoteResponse)
def archive_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_archived = True
    db.commit()
    db.refresh(note)

    return note


@router.patch("/{note_id}/restore", response_model=NoteResponse)
def restore_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.is_archived = False
    db.commit()
    db.refresh(note)

    return note


