import logging
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

os.environ["OPENAI_API_KEY"]

def get_text_chunks(text):
    logger.debug("Splitting text into chunks")
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size=1000, 
        chunk_overlap=100, 
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    logger.debug("Building vectorstore")
    print("Building vectorstore")
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)

def get_conversation_chain(vectorstore):
    logger.debug("Building conversation chain")
    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True)
    conersation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectorstore.as_retriever(), 
        memory=memory)
    return conersation_chain

def get_pdf_text(pdf_docs = None, pdf_path = None):
    logger.debug("Reading PDF")
    raw_text = ""
    if pdf_docs:
        for pdf in pdf_docs:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    raw_text += text
        return raw_text
    else:
        try:
            with open(pdf_path, "rb") as file:
                reader = PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        raw_text += text
                return raw_text
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise e