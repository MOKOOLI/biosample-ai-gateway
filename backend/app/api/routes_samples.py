from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.llm import extract_sample_from_text
from app.core.validator import validate_sample
from app.core.biosamples_client import submit_to_biosamples
from app.db.session import AsyncSessionLocal
from app.db.models import SampleRecord
from app.models.schemas import JobResponse
import json
import uuid
import redis.asyncio as redis
from app.config import settings

router = APIRouter()
redis_client = redis.from_url(settings.redis_url, decode_responses=True, socket_timeout=None)

class SampleRequest(BaseModel):
    text: str

@router.post("/extract")
async def extract_sample_sync(req: SampleRequest):
    sample = await extract_sample_from_text(req.text)
    validation = validate_sample(sample)
    ebi_result = await submit_to_biosamples(sample.model_dump())
    
    async with AsyncSessionLocal() as db:
        record = SampleRecord(
            organism=sample.organism,
            tissue=sample.tissue,
            disease=sample.disease,
            location=sample.location,
            collection_date=sample.collection_date,
            raw_metadata=sample.model_dump(),
            biosamples_accession=ebi_result.get("accession")
        )
        db.add(record)
        await db.commit()
        print("--> DB Saved (Sync)!")
        
    return {
        "sample": sample.model_dump(),
        "validation": validation.model_dump(),
        "ebi": ebi_result
    }

@router.post("/extract/async", response_model=JobResponse)
async def extract_sample_async(req: SampleRequest):
    job_id = str(uuid.uuid4())
    job_data = {"job_id": job_id, "text": req.text, "status": "pending"}
    await redis_client.set(f"job:{job_id}", json.dumps(job_data), ex=3600)
    await redis_client.lpush("queue:extraction", job_id)
    return JobResponse(job_id=job_id, status="pending", message="Job queued.")

@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job_raw = await redis_client.get(f"job:{job_id}")
    if not job_raw:
        raise HTTPException(status_code=404, detail="Job not found")
    return json.loads(job_raw)