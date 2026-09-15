"""
RAG (Retrieval-Augmented Generation) Agent using LangChain and Pinecone
"""

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import pinecone
import os

class RAGAgent:
    def __init__(self, openai_api_key: str, pinecone_api_key: str, pinecone_environment: str):
        """Initialize RAG Agent with OpenAI and Pinecone"""
        
        self.openai_api_key = openai_api_key
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        
        # Initialize Pinecone
        pinecone.init(
            api_key=pinecone_api_key,
            environment=pinecone_environment
        )
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name="gpt-4",
            temperature=0.7
        )
        
        # Initialize vector store
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "ai-agent-index")
        self.vector_store = Pinecone.from_existing_index(
            self.index_name,
            self.embeddings
        )
        
        # Initialize memory for conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Create RAG chain
        self.qa_chain = self._create_qa_chain()
    
    def _create_qa_chain(self):
        """Create a QA chain with custom prompt template"""
        
        prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": prompt},
            return_source_documents=True
        )
        
        return qa_chain
    
    async def query(self, query: str, top_k: int = 5) -> dict:
        """
        Query the RAG system
        
        Args:
            query: User query string
            top_k: Number of top results to retrieve
        
        Returns:
            Dictionary with answer, sources, and confidence
        """
        try:
            # Retrieve relevant documents
            results = self.vector_store.similarity_search_with_score(query, k=top_k)
            
            # Run QA chain
            response = self.qa_chain({"query": query})
            
            # Process sources
            sources = []
            for doc, score in results:
                sources.append({
                    "content": doc.page_content[:200],
                    "score": float(score),
                    "metadata": doc.metadata
                })
            
            # Calculate confidence based on retrieval scores
            confidence = sum([s["score"] for s in sources]) / len(sources) if sources else 0.0
            
            return {
                "answer": response["result"],
                "sources": sources,
                "confidence": min(confidence, 1.0)
            }
        
        except Exception as e:
            raise Exception(f"Error in RAG query: {str(e)}")
    
    async def add_document(self, document: dict) -> dict:
        """
        Add a document to the vector store
        
        Args:
            document: Dictionary with 'title', 'content', and optional 'metadata'
        
        Returns:
            Status dictionary
        """
        try:
            from langchain.schema import Document
            
            # Create Document object
            doc = Document(
                page_content=document.get("content", ""),
                metadata={
                    "title": document.get("title", ""),
                    "source": document.get("source", ""),
                    **document.get("metadata", {})
                }
            )
            
            # Add to vector store
            self.vector_store.add_documents([doc])
            
            return {
                "status": "success",
                "message": f"Document '{document.get('title', 'Unknown')}' indexed successfully"
            }
        
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    async def get_document_count(self) -> int:
        """Get total number of indexed documents"""
        try:
            # Get index stats from Pinecone
            index = pinecone.Index(self.index_name)
            stats = index.describe_index_stats()
            return stats.total_vector_count
        except Exception as e:
            return 0