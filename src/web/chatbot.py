import os

from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
openai_api_key = os.getenv("OPENAIKEY")

with st.sidebar:
    "[View the source code](https://github.com/margaritaGD/utm_mvsd_bnm)"
    "[![{tred_id}](tred_id)]"

st.title("BNM codex Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)