import streamlit as st
from Chatbot import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid


# ✅ Always return string, not UUID object
def generate_thread_id():
    return str(uuid.uuid4())


# ✅ Add new thread and reset state
def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_threads(thread_id)
    st.session_state["message_history"] = []


# ✅ Store thread IDs in session
def add_threads(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


# ✅ Load conversation from LangGraph checkpoint memory
def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    messages = state.values.get("messages", [])
    temp_messages = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        temp_messages.append({"role": role, "content": msg.content})
    return temp_messages


# --- Initialize session state ---
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_threads(st.session_state["thread_id"])

# --- Sidebar ---
st.sidebar.title("Chat Logs")
if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.header("Previous Conversations")
for thread_id in st.session_state["chat_threads"]:
    if st.sidebar.button(thread_id):
        st.session_state["thread_id"] = thread_id
        st.session_state["message_history"] = load_conversation(thread_id)
        st.rerun()

# --- Main Chat UI ---
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ✅ Use current thread_id (fix hardcoded bug)
    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    # ✅ Stream AI response and save it
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

    # Save assistant message locally
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
