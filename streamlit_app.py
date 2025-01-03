import streamlit as st
import requests
import json

# Streamlit UI
st.title("OIC Gen 3 XSLT Generator")

# File upload for source and target schemas
source_file = st.file_uploader("Upload Source XML/JSON Schema", type=["xml", "json"])
target_file = st.file_uploader("Upload Target XML/JSON Schema", type=["xml", "json"])

if source_file and target_file:
    # Display uploaded files
    st.text("Source Schema:")
    st.code(source_file.read().decode("utf-8"), language="xml")
    
    st.text("Target Schema:")
    st.code(target_file.read().decode("utf-8"), language="xml")

    # Button to trigger mapping generation
    if st.button("Generate XSLT"):
       # Read files as strings
        source_schema = source_file.read().decode("utf-8")
        target_schema = target_file.read().decode("utf-8")
    
        # Construct the prompt
        prompt = f"""
        Generate an XSLT that maps the following source schema to the target schema:
        - Source Schema: {source_schema}
        - Target Schema: {target_schema}
    
        Ensure the XSLT is compatible with Oracle Integration Cloud (OIC) Gen 3 standards.
        """
    
        # Call Azure OpenAI API
        api_url = "https://azeupotoaipoc.openai.azure.com/openai/deployments/gpt-4o-2024-05-13/chat/completions?api-version=2024-02-15-preview"  # Replace with your endpoint
        headers = {
            "Authorization": f"Bearer f7ff57fb377745d6837df09affdbd970",
            #"api-key": "f7ff57fb377745d6837df09affdbd970",  # Replace with your API key
            "Content-Type": "application/json"
        }
        data = {
            "model": "GPT35",  # Specify the model
            "prompt": prompt,
            "max_tokens": 1500,  # Adjust based on your needs
            "temperature": 0.5
        }
    
        response = requests.post(api_url, headers=headers, json=data)
    
        # Handle API response
        # Handle the response
        if response.status_code == 200:
            result = response.json()
            generated_text = result["choices"][0]["text"]
            print("Generated XSLT:")
            print(generated_text)
        else:
            print(f"Error {response.status_code}: {response.text}")
