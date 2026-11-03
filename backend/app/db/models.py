from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class SampleRecord(Base):
    __tablename__ = "samples"

    id = Column(Integer, primary_key=True, index=True)
    organism = Column(String, nullable=True)
    tissue = Column(String, nullable=True)
    disease = Column(String, nullable=True)
    location = Column(String, nullable=True)
    collection_date = Column(String, nullable=True)
    raw_metadata = Column(JSON, nullable=True)  # برای ذخیره کل خروجی LLM
    biosamples_accession = Column(String, nullable=True)  # آیدی که از EBI برمی‌گرده
    created_at = Column(DateTime(timezone=True), server_default=func.now())