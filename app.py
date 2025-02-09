import streamlit as st
from typing import Dict, Any, List, Union
from pydantic import BaseModel, create_model, Field
from extract_structured_data import extract_structured_data
from generate_pydantic_class import generate_pydantic_class
from pathlib import Path
import os
from google import genai

api_key = os.getenv("gemini_api_key") 

client = genai.Client(api_key=api_key)
 
model_id =  "gemini-2.0-flash" 


if 'rows' not in st.session_state:
    st.session_state.rows = 1
    
st.set_page_config(
    page_title="Gemini Data Extractor 📝",
    page_icon="🧊",
)
    
st.header("Gemini Data Extractor 📝")

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

col1, col2 = st.columns(2)
with col1:
    st.button("➕ Add Field", on_click=lambda: setattr(st.session_state, 'rows', st.session_state.rows + 1))
with col2:
    st.button("➖ Remove Field", on_click=lambda: setattr(st.session_state, 'rows', max(1, st.session_state.rows - 1)))


with st.form("schema_builder"):
    fields_data = []
    
    for i in range(st.session_state.rows):
        st.markdown(f"### Field {i+1}")
        cols = st.columns(3)
        
        with cols[0]:
            name = st.text_input(
                "Field Name",
                key=f"name_{i}",
            )
        
        with cols[1]:
            field_type = st.selectbox(
                "Type",
                ["String", "Integer", "Float", "Boolean", "List[String]", "List[Integer]", "List[Float]", "List[Boolean]"],
                key=f"type_{i}"
            )
            
        with cols[2]:
            description = st.text_area(
                "Description",
                key=f"desc_{i}"
            )
            
        if field_type == "Array":
            item_type = st.selectbox(
                "Array Item Type",
                ["String", "Integer", "Float", "Boolean"],
                key=f"item_type_{i}"
            )
        else:
            item_type = None
            
        if name and field_type:
            field_data = {
                "name": name,
                "type": field_type,
                "description": description,
            }
            if item_type:
                field_data["item_type"] = item_type
            fields_data.append(field_data)
    
    submitted = st.form_submit_button("Generate Schema")
    st.write(fields_data)
    
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Save the file to disk
    file_path = UPLOAD_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File successfully uploaded to {file_path}")
    if st.button("Perform Extraction"):
        with st.spinner("Processing..."):
            result = extract_structured_data(str(file_path), generate_pydantic_class(fields_data), client, model_id)
        
        st.title("Extraction Result")
        st.json(result)
