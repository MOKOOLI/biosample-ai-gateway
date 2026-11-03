from app.models.schemas import SampleExtraction, ValidationResult 
 
def validate_sample(sample: SampleExtraction) -> ValidationResult: 
    missing = [] 
    warnings = [] 
 
    # Rule 1: organism is always required 
    if not sample.organism: 
        missing.append("organism") 
 
    # Rule 2: if human + blood, disease is required 
    if sample.organism and sample.organism.lower() == "human": 
        if sample.tissue and sample.tissue.lower() == "blood": 
            if not sample.disease: 
                missing.append("disease") 
 
    # Rule 3: location warning 
    if not sample.location: 
        warnings.append("Location is missing. It is recommended for spatiotemporal tracking.") 
 
    # Rule 4: date warning 
    if not sample.collection_date: 
        warnings.append("Collection date is missing. This affects temporal analysis.") 
 
    is_valid = len(missing) == 0 
    return ValidationResult(is_valid=is_valid, missing_fields=missing, warnings=warnings) 
