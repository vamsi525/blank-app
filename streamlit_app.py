import streamlit as st
import openai

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_base = "https://azeupotoaipoc.openai.azure.com/"
openai.api_key = "f7ff57fb377745d6837df09affdbd970"
openai.api_version = "2024-05-01-preview"

st.title("Azure OpenAI Integration")

prompt = st.text_input("Enter your prompt:")
if st.button("Generate"):
    if prompt:
        response = openai.completions.create(
            engine="gpt-4o-2024-05-13",  # Replace with your Azure deployment name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        st.write(response['choices'][0]['message']['content'])
    else:
        st.warning("Please enter a prompt.")
