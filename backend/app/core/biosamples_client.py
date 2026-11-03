import httpx
import uuid
from app.config import settings

async def submit_to_biosamples(sample_data: dict) -> dict:
    token = settings.webin_token
    payload = {
        "name": f"BioSample-AI-{uuid.uuid4().hex[:8]}",
        "characteristics": {
            "organism": [{"text": sample_data.get("organism") or "unknown"}],
            "tissue": [{"text": sample_data.get("tissue") or "unknown"}],
            "disease": [{"text": sample_data.get("disease") or "unknown"}],
            "location": [{"text": sample_data.get("location") or "unknown"}],
            "collection_date": [{"text": sample_data.get("collection_date") or "unknown"}]
        }
    }
    if token:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.biosamples_base_url}/samples",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                    timeout=15.0
                )
                response.raise_for_status()
                result = response.json()
                return {"accession": result.get("accession", "UNKNOWN"), "source": "ebi_live"}
            except Exception as e:
                print(f"EBI Submission Error: {e}")
                return {"accession": "ERROR", "source": "error"}
    else:
        return {"accession": f"SAMEA{uuid.uuid4().int % 10000000}", "source": "mock"}
