import json
import uuid
import redis.asyncio as redis
from app.config import settings
from app.core.llm import extract_sample_from_text
from app.core.validator import validate_sample
from app.core.biosamples_client import submit_to_biosamples
from app.db.session import AsyncSessionLocal
from app.db.models import SampleRecord

redis_client = redis.from_url(settings.redis_url, decode_responses=True, socket_timeout=None)

async def enqueue_extraction(text: str) -> str:
    job_id = str(uuid.uuid4())
    job_data = {"job_id": job_id, "text": text, "status": "pending"}
    await redis_client.set(f"job:{job_id}", json.dumps(job_data), ex=3600)
    await redis_client.lpush("queue:extraction", job_id)
    return job_id

async def process_queue():
    print("Worker started. Waiting for jobs...")
    while True:
        result = await redis_client.brpop("queue:extraction", timeout=0)
        if result:
            _, job_id = result
            print(f"--> Found job {job_id}")
            job_raw = await redis_client.get(f"job:{job_id}")
            if not job_raw:
                continue
            job = json.loads(job_raw)
            job["status"] = "processing"
            await redis_client.set(f"job:{job_id}", json.dumps(job), ex=3600)
            try:
                print("--> Extracting with LLM...")
                sample = await extract_sample_from_text(job["text"])
                print(f"--> Extracted: {sample.organism}, {sample.tissue}")
                print("--> Validating...")
                validation = validate_sample(sample)
                print("--> Sending to BioSamples...")
                ebi_result = await submit_to_biosamples(sample.model_dump())
                print(f"--> EBI result: {ebi_result}")
                print("--> Saving to Database...")
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
                    print("--> DB Saved!")
                job["status"] = "completed"
                job["result"] = {
                    "sample": sample.model_dump(),
                    "validation": validation.model_dump(),
                    "ebi": ebi_result
                }
            except Exception as e:
                print(f"!!! ERROR processing job: {e}")
                job["status"] = "failed"
                job["error"] = str(e)
            await redis_client.set(f"job:{job_id}", json.dumps(job), ex=3600)
            await redis_client.publish(f"job_updates:{job_id}", json.dumps(job))
