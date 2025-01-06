import os
import json
import xml.etree.ElementTree as ET
import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv("./example.env")

# Azure OpenAI Configuration
endpoint =  os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT")
subscription_key = os.getenv("AZURE_OPENAI_KEY")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=os.getenv("AZURE_OPENAI_API_VERSION") 
)


def generate_xslt(client, source_xml, target_xml):
    """Generate XSLT code using OpenAI Azure Chat API."""
    chat_prompt = [
        {
            "role": "system",
            "content": "You are an AI assistant that generates XSLT mappings between source and target schemas for OIC Gen3 integrations."
        },
        {
            "role": "user",
            "content": f"Generate an XSLT that maps the following source schema to the target schema:\n\nSource XML:\n{source_xml}\n\nTarget XML:\n{target_xml}\n\nXSLT:\nEnsure the XSLT is compatible with Oracle Integration Cloud (OIC) Gen 3 standards\nThe XSLT should not use templates or variables, and should use namespace prefixes"
        },
       
          # {
          #    "role": "user",
          #    "content": f"Could you please generate an XSLT mapping that transforms the following source XML schema to the target XML schema? The transformation should be compatible with Oracle Integration Cloud (OIC) Gen 3 standards:\n\nSource Schema:\n{json.dumps(source_schema, indent=2)}\n\nTarget Schema:\n{json.dumps(target_schema, indent=2)}"
          # },
    ]
    st.write(chat_prompt)
    response = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=1000,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )
    #return response['choices'][0]['message']['content']
    return response.choices[0].message.content

# Streamlit App
st.title("OIC Gen3 XSLT Generator")
st.write("Upload source and target schema files (JSON, XML, or a combination) to generate XSLT mappings.")

# Create columns for side-by-side upload buttons
col1, col2 = st.columns(2)

# File upload section with side-by-side buttons
with col1:
    uploaded_source_file = st.file_uploader("Upload Source XML file", type="xml")

with col2:
    uploaded_target_file = st.file_uploader("Upload Target Xml file", type="xml")



if source_file and target_file:
    source_xml_content = uploaded_source_file.read().decode("utf-8")
    target_xml_content = uploaded_target_file.read().decode("utf-8")

    if source_xml_content and target_xml_content:
        if st.button("Generate XSLT"):
            with st.spinner("Generating XSLT..."):
                try:
                    xslt_code = generate_xslt(client, source_xml_content, target_xml_content)
                    st.success("XSLT generated successfully!")
                    st.code(xslt_code, language="xml")

                   
                except Exception as e:
                    st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload both source and target schema files.")
