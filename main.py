import streamlit as st
from response import respond_query, diagnose_injury

st.markdown("""
        <style>
            .st-emotion-cache-1v0mbdj > img {
                border-radius: 50%;
            }
        
            .st-emotion-cache-1gv3huu > div {
                background-color: #efeee7;
            }
        </style>
        """, unsafe_allow_html=True)

st.title("Talk to PacePal")

diagnosis = ["None"]
accuracy = ["None"]

chat_history = ["Nothing has been chatted yet."]
max_len = 5

# initializing chat history with user
if "messages" not in st.session_state:
        st.session_state.messages = []

# display all messages from history
for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

# user input
prompt = st.chat_input("Describe your injury")
if prompt:
    # display user input
    with st.chat_message("user", avatar="user.png"):
        st.markdown(prompt)
    # store message in chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "user.png"})

    response = respond_query(prompt, chat_history)
    # display bot response
    with st.chat_message("assistant", avatar="chat.png"):
        st.markdown(response)
    # store response in chat history
    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": "chat.png"})

    if (len(chat_history) < 5):
         chat_history.append(f"User: {prompt} /n Assistant: {response}")
    else:
         chat_history = chat_history[1:]
         chat_history.append(f"User: {prompt} /n Assistant: {response}")

    # print(chat_history)

    try:
        diagnosis, accuracy = diagnose_injury(prompt, chat_history)
    except:
         diagnosis = ["No Diagnosis Found", "No Diagnosis Found"]
         accuracy = ["0", "0"]

    if (prompt == "clr"):
        st.session_state.messages = []
    
with st.sidebar:
    st.image("run-relief.png")
    for i in range(len(diagnosis)):
         st.write(f"# Diagnosis {i+1}")
         st.write(diagnosis[i])
         st.write(f"# Confidence Score {i+1}")
         st.write(accuracy[i])
         st.write()
