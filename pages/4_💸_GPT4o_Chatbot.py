import streamlit as st
from openai import OpenAI

st.set_page_config(layout='centered', page_title="OPENAI API", page_icon="😎")
st.title('💸 GPT4o Chatbot')

#################################################
#Sidebar
st.sidebar.image('logo.png') 
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
This app retrieves 💸[OPENAI API](https://platform.openai.com/docs/api-reference/introduction). (Max Tokens --> 512))


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
def reset():
    st.session_state.messages_gpt = []
    st.session_state.reset_gpt = False

api_key_secrets= st.secrets['API_KEY_P_KOH']

client = OpenAI(
    api_key=api_key_secrets,
)

if "messages_gpt" not in st.session_state:
    st.session_state.messages_gpt = []
if "reset_gpt" not in st.session_state:
    st.session_state.reset_gpt = False

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages_gpt:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Say something"):

    # Store and display the current prompt.
    st.session_state.messages_gpt.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role":  m["role"],
                    "content": m["content"],
                }
                for m in st.session_state.messages_gpt
            ],
            max_tokens=512,
            stream=True,)

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages_gpt.append({"role": "assistant", "content": response})
    st.session_state.reset_gpt = True

if st.session_state.reset_gpt:
    st.button('reset chat',on_click=reset)