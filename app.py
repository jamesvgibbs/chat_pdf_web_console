import argparse
import subprocess
import logging
from dotenv import load_dotenv
from utils import get_pdf_text, get_text_chunks, get_vectorstore, get_conversation_chain

load_dotenv()

PDF_PATH = "read/Dreamweaver-print.pdf"

def main(): 
    raw_text = get_pdf_text(pdf_path=PDF_PATH)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    conversation = get_conversation_chain(vectorstore)
    while True:
        query = input("Enter your question (type 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        elif query == "":
            continue
        try:
            response = conversation({"question": query})
            chat_history = response["answer"]
            print(f"\nBot: {chat_history}\n")
        except Exception as e:
            print(e)
            raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--streamlit", help="Run as a Streamlit app", action="store_true")
    args = parser.parse_args()
    if args.streamlit:
        logging.debug("Running as a Streamlit app")
        subprocess.call(["streamlit", "run", "streamlit.py"])
    else:
        logging.debug("Running as a console app")
        main()