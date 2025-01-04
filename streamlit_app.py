import os
import base64
import streamlit as st
from openai import AzureOpenAI
import json
import pandas as pd

# Azure OpenAI Configuration
endpoint = os.getenv("ENDPOINT_URL", "https://azeupotoaipoc.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "f7ff57fb377745d6837df09affdbd970")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Helper functions
def process_file(uploaded_file):
    """Process uploaded file and return its content as a dictionary."""
    if uploaded_file.name.endswith('.json'):
        return json.load(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file).to_dict(orient='records')
    else:
        st.error("Unsupported file format. Please upload a JSON or Excel file.")
        return None

def generate_xslt(client, source_schema, target_schema):
    """Generate XSLT code using OpenAI Azure Chat API."""
    chat_prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that generates XSLT mappings between source and target schemas for OIC Gen3 integrations."
        },
        {
            "role": "user",
            "content": f"Generate an XSLT that maps the following source schema to the target schema:\n\nSource Schema:\n{json.dumps(source_schema, indent=2)}\n\nTarget Schema:\n{json.dumps(target_schema, indent=2)}"
        }
    ]

    response = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )
    return response['choices'][0]['message']['content']

# Streamlit App
st.title("OIC Gen3 XSLT Generator")
st.write("Upload source and target schema files (JSON or Excel) to generate XSLT mappings.")

# File Upload Section
source_file = st.file_uploader("Upload Source Schema", type=["json", "xml"])
target_file = st.file_uploader("Upload Target Schema", type=["json", "xml"])

if source_file and target_file:
    # Process uploaded files
    source_schema = process_file(source_file)
    target_schema = process_file(target_file)

    if source_schema and target_schema:
        if st.button("Generate XSLT"):
            with st.spinner("Generating XSLT..."):
                try:
                    xslt_code = generate_xslt(client, source_schema, target_schema)
                    st.success("XSLT generated successfully!")
                    st.code(xslt_code, language="xml")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload both source and target schema files.")

