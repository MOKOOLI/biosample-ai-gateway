import ollama 
import traceback 
from app.config import settings 
from app.models.schemas import SampleExtraction 
 
async def extract_sample_from_text(text: str) -> SampleExtraction: 
    prompt = f"Extract sample metadata from this text and return JSON with keys: organism, tissue, disease, location, collection_date. If a field is missing, set it to null. Text: {text}" 
    try: 
        client = ollama.AsyncClient(host=settings.ollama_base_url) 
        print(f"Connecting to Ollama at {settings.ollama_base_url} with model {settings.ollama_model}...") 
        response = await client.chat( 
            model=settings.ollama_model, 
            messages=[{"role": "user", "content": prompt}], 
            format="json", 
            options={"temperature": 0} 
        ) 
        print("RAW LLM RESPONSE:", response["message"]["content"]) 
        return SampleExtraction.model_validate_json(response["message"]["content"]) 
    except Exception as e: 
        print("ERROR: LLM failed with exception:") 
        traceback.print_exc() 
        return SampleExtraction() 
