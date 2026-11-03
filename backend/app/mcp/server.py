from mcp.server.fastmcp import FastMCP 
from app.core.llm import extract_sample_from_text 
from app.core.validator import validate_sample 
 
mcp = FastMCP("BioSample Gateway") 
 
@mcp.tool() 
async def extract_and_validate(text: str) -> dict: 
    """Extract biological sample metadata from natural language and validate it against bioinformatics checklists.""" 
    sample = await extract_sample_from_text(text) 
    validation = validate_sample(sample) 
    return { 
        "sample": sample.model_dump(), 
        "validation": validation.model_dump() 
    } 
