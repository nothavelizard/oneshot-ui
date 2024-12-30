import streamlit as st
from openai import OpenAI

# Load your OpenAI API key
openai_api_key = st.secrets.OPENAI_API_KEY
client = OpenAI(api_key=openai_api_key)
models_available = client.models.list()
model_names = [model.id for model in models_available.data]

# Set page config
st.set_page_config(page_title="OpenAI API Demo", page_icon="🤖")

# App title
st.title("🤖 OpenAI API Streamlit App")

# Sidebar for model selection and parameters
with st.sidebar:
    st.header("Parameters")
    model = st.selectbox(
        "Choose a model",
        model_names,
        help="Select the OpenAI model to use for generating responses."
    )
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        help="Controls the randomness of the output."
    )
    max_tokens = st.slider(
        "Max Tokens",
        min_value=50,
        max_value=1000,
        value=150,
        help="Maximum number of tokens to generate."
    )

# Text input for user prompt
prompt = st.text_area(
    "Enter your prompt:",
    height=200,
    help="Type in the prompt you want to send to the OpenAI API."
)

# Generate button
if st.button("Generate Response"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating response..."):
            try:
                # Use ChatCompletion for chat-based models
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                generated_text = response.choices[0].message.content.strip()

                # Display the response
                st.success("Generated Response:")
                st.write(generated_text)

            except Exception as e:
                st.error(f"An error occurred: {e}")