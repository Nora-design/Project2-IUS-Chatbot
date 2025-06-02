import streamlit as st
from scripts.chatbot import ask_chatbot

st.set_page_config(page_title="IUS AI Assistant", page_icon="🎓")

st.title("IUS Chatbot")
st.subheader("Ask me anything about IUS!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if prompt := st.chat_input("Your question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Retrieve answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_context = st.session_state.messages[-6:]  # only last 6 messages for speed
            chat_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in full_context])
            answer = ask_chatbot(prompt, history=chat_text)
            st.markdown(answer)
            

    # Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": answer})