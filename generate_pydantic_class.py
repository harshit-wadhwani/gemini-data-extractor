from pydantic import BaseModel, create_model, Field
from typing import Dict, Any, List, Union


def generate_pydantic_class(field_definitions: List[Dict[str, str]]) -> BaseModel:
    type_mapping = {
        'String': str,
        'Integer': int,
        'Float': float,
        'Boolean': bool,
        'List[String]': List[str],
        'List[Integer]': List[int],
        'List[Float]': List[float],
        'List[Boolean]': List[bool],
    }
    
    model_fields = {}
    for field in field_definitions:
        name = field['name']
        type_str = field['type']
        description = field['description']
        
        python_type = type_mapping.get(type_str)
        if python_type is None:
            raise ValueError(f"Unsupported type: {type_str}")

        model_fields[name] = (python_type, Field(..., description=description))
    
    DynamicModel = create_model(
        'DynamicModel',
        **model_fields
    )
    
    return DynamicModel