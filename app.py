import streamlit as st
from huggingface_hub import InferenceClient
from country import countries_with_flags

st.set_page_config(page_title="GlobeInsight")

st.markdown("<h1 style='text-align: center; background-color: #f0f0f0; color: black;'>GlobeInsight 🌎</h1>", unsafe_allow_html=True)

st.divider()

option = st.selectbox("Select a country", (countries_with_flags), index=None, placeholder="Select Country")
st.write("You selected:", option)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🙍🏻‍♂️" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user", avatar="🙍🏻‍♂️").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Initialize the InferenceClient
    client = InferenceClient(
        "meta-llama/Meta-Llama-3-8B-Instruct",
        token=st.secrets["api_token"],  # Replace with your actual token securely
    )

    # Generate response from the model
    response_message = ""
    for message in client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        stream=True,
    ):
        response_message += message.choices[0].delta.content

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response_message)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_message})
