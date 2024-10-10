import streamlit as st
from openai import OpenAI
import os

st.title('🤖 Typhoon Thai Chatbot')

#################################################
#Sidebar
st.sidebar.image(r'C:\Users\Sorawitr\Desktop\streamlit\logo.png') 
st.markdown("""
<style>
    div[data-testid="stSidebarUserContent"] img {
        background: #ffffff;
        border-radius: 20px;
        border: thick;
        border-style: inset;
        border-color: black;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("About")

st.sidebar.markdown(
    """
This app retrieves 🤖[Typhoon API](https://opentyphoon.ai/app/playground) Large Language Model optimized for Thai using🎈[Streamlit](https://streamlit.io/).


""")

st.sidebar.markdown(
    "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
)
st.sidebar.divider()

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
"""
)


#################################################
api_key_secrets= st.secrets['API_KEY_TYPHOON']

client = OpenAI(
    api_key=api_key_secrets,
    base_url="https://api.opentyphoon.ai/v1",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("ลองพิมพ์อะไรหน่อย"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    stream = client.chat.completions.create(
            model="typhoon-v1.5x-70b-instruct",
            messages=[
                {
                    "role":  m["role"],
                    "content": m["content"],
                }
                for m in st.session_state.messages
            ],
            max_tokens=512,
            temperature=0.6,
            top_p=0.95,
            #repetition_penalty=1.05,
            stream=True,)

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})