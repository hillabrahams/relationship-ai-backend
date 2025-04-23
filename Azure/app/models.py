from sqlalchemy import Column, String, Float, Text
from app.database import Base

class GPTLabel(Base):
    __tablename__ = "gpt_labels"

    id = Column(String, primary_key=True, index=True)
    text = Column(Text)
    score = Column(Float)
    reasoning = Column(Text)
    confidence = Column(Float)
    timestamp = Column(String)

