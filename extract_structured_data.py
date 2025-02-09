from pydantic import BaseModel, create_model, Field
from typing import Dict, Any, List, Union
from google import genai

def extract_structured_data(file_path: str, model: BaseModel, client: genai.Client, model_id: str) -> BaseModel:
    file = client.files.upload(file=file_path, config={'display_name': file_path.split('/')[-1].split('.')[0]})

    prompt = f"Extract the structured data from the following PDF file"
    response = client.models.generate_content(model=model_id, contents=[prompt, file], config={'response_mime_type': 'application/json', 'response_schema': model})

    return response.text