from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from app.database import SessionLocal, engine
from app.models import Base, GPTLabel
from sqlalchemy.orm import Session
from app.gpt_labeling import get_gpt_label
from datetime import datetime
import uuid

import traceback

Base.metadata.create_all(bind=engine)

app = FastAPI()

class JournalEntry(BaseModel):
    text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auto_label")
def auto_label(entry: JournalEntry, db: Session = Depends(get_db)):
    try:
        result = get_gpt_label(entry.text)
        entry_id = str(uuid.uuid4())
        label = GPTLabel(
            id=entry_id,
            text=entry.text,
            score=result["score"],
            reasoning=result["reasoning"],
            confidence=result.get("confidence", 0.5),
            timestamp=str(datetime.utcnow())
        )
        db.add(label)
        db.commit()
        return {
            "entry_id": entry_id,
            "text": entry.text,
            "score": result["score"],
            "reasoning": result["reasoning"],
            "confidence": result.get("confidence", 0.5)
        }
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        # raise HTTPException(status_code=500, detail="GPT labeling failed")

