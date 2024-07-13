import os
from dotenv import load_dotenv
from groq import Groq

import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

load_dotenv()

st.set_page_config(
    page_title="TalkingPDF",
    page_icon="📖",
    initial_sidebar_state='auto',
    menu_items={
        "Report a Bug": "mailto:lasithdissanayake.official@gmail.com",
        "About": "https://dissanayakelyb.github.io/LasithDissanayake.github.io/"
    }
)

groq_api_key = os.getenv("groq_API")

with st.sidebar:

    model = st.selectbox(
        'Choose a model',
        ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it', 'llama3-70b-8192']
    )

    reset = st.button(
         label="Reset",
         type="primary"
         )

    if reset:
        st.session_state.chat_history = []

memory = ConversationBufferWindowMemory(k=10)

st.write("&copy; Lasith Dissanayake | 2024")
st.title("Mr. KnowItAll")

input_message = st.chat_input("Ask from expert...")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

else:
    for message in st.session_state.chat_history:
        memory.save_context({'input': message['human']}, {'output': message['AI']})

        with st.chat_message("user"):
            st.write(message["human"])

        with st.chat_message("assistant"):
            st.write(message["AI"])

if groq_api_key:
    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
        memory=memory
    )

    if input_message:

        response = conversation(input_message)
        message = {'human': input_message, 'AI': response['response']}

        st.session_state.chat_history.append(message)

        with st.chat_message("user"):
            st.write(input_message)

        with st.chat_message("assistant"):
            st.write(response['response'])
