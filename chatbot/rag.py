from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatOllama(model="llama3",streaming=True)

prompt = ChatPromptTemplate.from_template(
    """You are a helpful AI assistant like ChatGPT.

Use the context to answer clearly and conversationally.
If needed, explain in detail.

Context:
{context}

Question:
{question}

Answer:"""
)





def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



def create_vectorstore(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)

    vectorstore = Chroma.from_documents(docs, embeddings)
    return vectorstore



def ask_question(vectorstore, query):
    retriever = vectorstore.as_retriever()

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    response = chain.invoke(query)
    return response.content