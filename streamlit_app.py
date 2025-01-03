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
        # Call to Azure OpenAI API for XSLT generation
        response = requests.post(
            "https://azeupotoaipoc.openai.azure.com/openai/deployments/gpt-4o-2024-05-13/chat/completions?api-version=2024-02-15-preview",
            headers={"api-key": "f7ff57fb377745d6837df09affdbd970"},
            json={"source_schema": source_file, "target_schema": target_file}
        )

        if response.status_code == 200:
            xslt_output = response.json().get("xslt")
            st.success("XSLT Generated Successfully!")
            st.code(xslt_output, language="xml")
            
            # Download option
            st.download_button("Download XSLT", xslt_output, file_name="mapping.xslt")
        else:
            st.error("Failed to generate XSLT. Please try again.")
