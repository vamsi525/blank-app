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

# Helper functions
def parse_json(file):
    """Parse JSON content."""
    try:
        return json.load(file)
    except json.JSONDecodeError:
        st.error("Failed to parse JSON file.")
        return None

def parse_xml(file):
    """Parse XML content into a dictionary."""
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        return xml_to_dict(root)
    except ET.ParseError:
        st.error("Failed to parse XML file.")
        return None

def xml_to_dict(element):
    """Convert an XML element into a dictionary."""
    return {
        element.tag: (
            element.text if len(element) == 0 else {child.tag: xml_to_dict(child) for child in element}
        )
    }

def process_file(file):
    """Identify file type and process accordingly."""
    if file.name.endswith(".json"):
        return parse_json(file)
    elif file.name.endswith(".xml"):
        return parse_xml(file)
    else:
        st.error("Unsupported file format. Please upload JSON or XML files.")
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
            "content": f"Generate an XSLT that maps the following source schema to the target schema:\n\nSource Schema:\n{json.dumps(source_schema, indent=2)}\n\nTarget Schema:\n{json.dumps(target_schema, indent=2)}\nEnsure the XSLT is compatible with Oracle Integration Cloud (OIC) Gen 3 standards"
        },
          # {
          #    "role": "user",
          #    "content": f"Could you please generate an XSLT mapping that transforms the following source XML schema to the target XML schema? The transformation should be compatible with Oracle Integration Cloud (OIC) Gen 3 standards:\n\nSource Schema:\n{json.dumps(source_schema, indent=2)}\n\nTarget Schema:\n{json.dumps(target_schema, indent=2)}"
          # },
    ]

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
    source_file = st.file_uploader("Upload Source Schema", type=["json", "xml"])

with col2:
    target_file = st.file_uploader("Upload Target Schema", type=["json", "xml"])

# # File Upload Section
# source_file = st.file_uploader("Upload Source Schema", type=["json", "xml"])
# target_file = st.file_uploader("Upload Target Schema", type=["json", "xml"])

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
