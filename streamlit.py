import logging
import streamlit as st
from htmlTemplates import css, bot_template, user_template
from utils import get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain

def handle_userinput(user_question):
    if st.session_state.conversation is not None:
        response = st.session_state.conversation({"question": user_question})
        st.session_state.chat_history = response["chat_history"]
        st.session_state.answer = response["answer"]
        st.session_state.question = response["question"]
        logging.info(f"chat_history: {st.session_state.chat_history}")

        st.write(user_template.replace("{{MSG}}", st.session_state.question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", st.session_state.answer), unsafe_allow_html=True)
    else:
        st.warning("Please upload a PDF document then press the process button.")

def main():
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs=pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == "__main__":
    logging.info("Starting streamlit")
    main()