import os

from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
openai_api_key = os.getenv("OPENAIKEY")


def initialize_conversation(thread_id):
    # Initialize a new conversation or load an existing one based on thread_id
    if "conversations" not in st.session_state:
        st.session_state["conversations"] = {}

    if thread_id not in st.session_state["conversations"]:
        # Start a new conversation if thread_id is new
        st.session_state["conversations"][thread_id] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    # Set the current conversation to the specified thread_id
    st.session_state["messages"] = st.session_state["conversations"][thread_id]


with st.sidebar:
    st.markdown("[View the source code](https://github.com/margaritaGD/utm_mvsd_bnm)")

    thread_id = st.text_input("Enter thread ID (leave empty for new conversation)", "new")

    if thread_id == "new":
        thread_id = f"thread_{len(st.session_state.get('conversations', [])) + 1}"

    # Initialize or switch conversation based on thread ID
    initialize_conversation(thread_id)

st.title("BNM codex Chatbot")

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # Append the user's message to the current conversation
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state["messages"]
    )
    msg = response.choices[0].message.content

    # Append the assistant's message to the current conversation
    st.session_state["messages"].append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    # Update the current conversation in session state
    st.session_state["conversations"][thread_id] = st.session_state["messages"]