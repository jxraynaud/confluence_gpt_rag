import streamlit as st

# local imports
from chatbot.chatbot import Chatbot

def main():
    # page setup
    st.set_page_config(
        page_title='Chatbot',
        page_icon=':book:'
    )
    
    st.header("Chatbot")

    # Add custom CSS
    with open('styles.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Placeholder for user question and chatbot response
    conversation_placeholder = st.empty()

    # initialize the session state
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = Chatbot()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize user_input in session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ''

    # Text Area Component for user input
    user_input = st.text_area("Enter your question:", value=st.session_state.user_input, height=100, key='user_input')

    # Add a button to submit the user input
    if st.button("Submit"):  # Changed from st.empty()
        # Add the question to the chat history immediately
        st.session_state.chat_history.append({'question': user_input, 'response': 'Waiting for response...'})
        display_conversation(conversation_placeholder)

        with st.spinner('Waiting for response...'):
            # Get the response from the chatbot
            conversation = st.session_state.chatbot.handle_user_input(user_input)
            # Replace the last chat history item with the full conversation
            st.session_state.chat_history[-1] = conversation

        # Clear the user input field
        # IMPORTANT: Not allowed to modify session_state value after widget has been created
        # Instead of clearing the input here, we check for a change in the next run of the script
        # st.session_state.user_input = ''
        display_conversation(conversation_placeholder)

    # Check if the user_input has changed, if yes then clear the input
    if st.session_state.user_input != user_input:
        st.session_state.user_input = ''


def display_conversation(conversation_placeholder):
    # Display the conversation
    chat_history = []
    for conversation in st.session_state.chat_history:
        chat_history.append(f'<div class="question">{conversation["question"]}</div>')
        chat_history.append(f'<div class="response">{conversation["response"]}</div>')  # assuming response is a markdown string
    conversation_placeholder.markdown('\n---\n'.join(chat_history), unsafe_allow_html=True)  # using markdown function with unsafe_allow_html

if __name__ == "__main__":
    main()
