# Gemini Data Extractor 📝

A Streamlit application that uses Google's Gemini AI to extract structured data from documents based on user-defined schemas.

## Features

- Dynamic schema builder interface
- Support for multiple field types:
    - String
    - Integer
    - Float
    - Boolean
    - List variations (String, Integer, Float, Boolean)


- File upload capability
- Automated data extraction using Gemini AI
- Real-time JSON output

## Technical Details

- Built with Streamlit for the web interface
- Uses Pydantic for data validation and schema generation
- Integrates with Google's Gemini AI for document processing
- Supports dynamic schema creation based on user input

## To get started:

 - Clone the repository
 - Install the required dependencies
 - Add your Gemini API key in the .env
 - Run the Streamlit app - `streamlit run app.py`
