import json
import os
import time
import streamlit as st
from dotenv import load_dotenv

from src.main.ai.assistant import AssistantBuilder
from src.main.utils.commons import PathUtils

load_dotenv(PathUtils.DOT_ENV_FILE)
assistant_builder = AssistantBuilder(model_title="BNM Expert")
with st.sidebar:
    "[View the source code](https://github.com/margaritaGD/utm_mvsd_bnm)"
    thread_id = st.text_input("Enter your thread ID")

st.title(f"💬 Chatbot with {assistant_builder.model_title}")
st.caption("🚀 A Streamlit chatbot for MVSD Project at UTM")
assistant = assistant_builder.build()
if os.getenv("OPENAI_API_KEY", None) is None:
    st.warning("Please enter your OpenAI API key in the .env file.")
    st.stop()

if not thread_id:
    thread = assistant_builder.client.beta.threads.create()
else:
    thread = assistant_builder.client.beta.threads.retrieve(thread_id)

thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Assistant", "content": "Bună ziua, cu ce vă pot ajuta?"}]
messages = assistant_builder.client.beta.threads.messages.list(thread.id).data

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input for new message
if prompt := st.chat_input("Type your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # Create new message in the thread
    assistant_builder.client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    # Run the assistant
    run = assistant_builder.client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while True:
        run_status = assistant_builder.client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            st.write("Run failed:", run_status.last_error)
            break
        time.sleep(1)

    # Fetch updated messages
    messages = list(assistant_builder.client.beta.threads.messages.list(
        thread_id=thread.id
    ).data)
    message = messages[0]
    role = message.role
    for content in message.content:
        if role == "assistant":
            try:
                if content.text.value.startswith("```json"):
                    data = json.loads(content.text.value[7:-3])
                    msg = data["title"] + "\n\n" + data["content"]
                else:
                    data = json.loads(content.text.value)
                    msg = data["title"] + "\n\n" + data["content"]
            except Exception as e:
                msg = content.text.value
                st.chat_message(role).write(msg)
            st.chat_message("assistant").write(msg)
            st.session_state.messages.append({"role": role, "content": msg})
