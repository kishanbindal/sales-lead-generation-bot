from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

class VectorStore:
    """
    FAISS Vector Store API for the Chatbot

    Can be used to ingest data into a FAISS Vector Store and perform vector search on the data.
    """

    def __init__(self, store_path: str):
        """
        Initialize the FAISS Vector Store

        Args:
            store_path: str - The path to the FAISS Vector Store
        """
        self.store_path = store_path
        # self.embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={"device": device})
        self.embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={"device": device})


    def ingest_data(self, file_path: str):
        """
        Ingest data into a FAISS Vector Store
        """
        try:
            with open(file_path, "r") as f:
                data = f.read()
            print(device)
            splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=150)
            chunks = splitter.split_text(data)
            metadatas = [{"source": file_path} for _ in range(len(chunks))]
            vs = FAISS.from_texts(chunks, self.embedder, metadatas=metadatas)
            vs.save_local(self.store_path)
            return True
        except Exception as e:
            print(e)
            return False

    def vector_search(self, query: str, k: int = 5):
        """
        Perform vector search on the data
        """
        vs = FAISS.load_local(self.store_path, self.embedder, allow_dangerous_deserialization=True) 
        output = vs.similarity_search_with_score(query, k=k)
        # return output
        return "\n".join([f"""
        Chunk:
        {item[0].page_content}

        Source:
        {item[0].metadata.get('source', '')}

        Score:
        {item[1]}
        """ for item in output])