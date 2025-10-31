"""
Document Processor - Handles large document chunking and semantic search
"""
import json
import numpy as np
from typing import List, Tuple
from google import genai


class DocumentProcessor:
    """Handles large document processing with chunking and semantic search"""
    
    def __init__(self, api_key="YOUR_API_KEY"):
        """
        Initialize the document processor.
        
        Args:
            api_key: Gemini API key for embeddings
        """
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
        self.document_chunks = []
        self.chunk_embeddings = []
        self.chunk_size = 2000  # characters per chunk
        self.chunk_overlap = 200  # overlap between chunks
        
    def load_documents(self, doc_path: str):
        """
        Load a large document and prepare it for search.
        
        Args:
            doc_path: Path to the document
        """
        print("\n📄 Loading large document...")
        
        # Load document
        with open(doc_path, 'r', encoding='utf-8') as f:
            doc_content = f.read()
            
        print(f"  ✓ Document: {len(doc_content):,} characters")
        
        # Chunk the document
        print(f"\n✂️  Chunking document (chunk_size={self.chunk_size}, overlap={self.chunk_overlap})...")
        self.document_chunks = self._chunk_text(doc_content, source="main_doc")
        print(f"  ✓ Created {len(self.document_chunks)} chunks total")
        
        # Create embeddings for all chunks
        print(f"\n🔢 Creating embeddings for chunks...")
        self.chunk_embeddings = self._create_embeddings([chunk['text'] for chunk in self.document_chunks])
        print(f"  ✓ Generated {len(self.chunk_embeddings)} embeddings")
        
        # Save processed chunks to cache
        self._save_cache()
        
    def load_from_cache(self, cache_path="results/document_cache.json"):
        """
        Load previously processed chunks and embeddings from cache.
        
        Args:
            cache_path: Path to cache file
            
        Returns:
            bool: True if cache loaded successfully, False otherwise
        """
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                self.document_chunks = cache_data['chunks']
                self.chunk_embeddings = [np.array(emb) for emb in cache_data['embeddings']]
                print(f"  ✓ Loaded {len(self.document_chunks)} chunks from cache")
                return True
        except FileNotFoundError:
            print(f"  ⚠️  Cache file not found: {cache_path}")
            return False
        except Exception as e:
            print(f"  ⚠️  Error loading cache: {e}")
            return False
    
    def _save_cache(self, cache_path="results/document_cache.json"):
        """Save processed chunks and embeddings to cache."""
        import os
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        
        cache_data = {
            'chunks': self.document_chunks,
            'embeddings': [emb.tolist() for emb in self.chunk_embeddings]
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"  ✓ Saved cache to {cache_path}")
    
    def _chunk_text(self, text: str, source: str) -> List[dict]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            source: Source identifier (doc1 or doc2)
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                last_period = chunk_text.rfind('.')
                last_question = chunk_text.rfind('?')
                last_exclamation = chunk_text.rfind('!')
                last_newline = chunk_text.rfind('\n\n')
                
                # Use the last sentence boundary found
                boundary = max(last_period, last_question, last_exclamation, last_newline)
                if boundary > self.chunk_size * 0.5:  # Only if we're not cutting too much
                    end = start + boundary + 1
                    chunk_text = text[start:end]
            
            chunks.append({
                'id': f"{source}_chunk_{chunk_id}",
                'text': chunk_text.strip(),
                'source': source,
                'start_pos': start,
                'end_pos': end
            })
            
            chunk_id += 1
            start = end - self.chunk_overlap  # Overlap chunks
            
        return chunks
    
    def _create_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """
        Create embeddings for a list of texts using Gemini embeddings.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        batch_size = 100  # Process in batches to avoid rate limits
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            print(f"    Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
            
            # Create embeddings for batch
            batch_embeddings = []
            for text in batch:
                result = self.client.models.embed_content(
                    model='models/text-embedding-004',
                    contents=text
                )
                batch_embeddings.append(np.array(result.embeddings[0].values))
            
            embeddings.extend(batch_embeddings)
        
        return embeddings
    
    def search_relevant_chunks(self, query: str, work_title: str, author_name: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """
        Search for the most relevant chunks for a given work and author.
        
        Args:
            query: Additional search query (optional)
            work_title: Title of the work
            author_name: Name of the author
            top_k: Number of top chunks to return
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        # Create search query combining work title, author, and additional query
        search_text = f"{work_title} {author_name}"
        if query:
            search_text = f"{search_text} {query}"
        
        print(f"    🔍 Searching for relevant chunks: '{search_text[:100]}...'")
        
        # Create embedding for search query
        result = self.client.models.embed_content(
            model='models/text-embedding-004',
            contents=search_text
        )
        query_embedding = np.array(result.embeddings[0].values)
        
        # Calculate cosine similarity with all chunks
        similarities = []
        for chunk_emb in self.chunk_embeddings:
            similarity = self._cosine_similarity(query_embedding, chunk_emb)
            similarities.append(similarity)
        
        # Get top-k chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [(self.document_chunks[i], similarities[i]) for i in top_indices]
        
        print(f"    ✓ Found {len(results)} relevant chunks (scores: {[f'{s:.3f}' for _, s in results]})")
        
        return results
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def get_context_for_work(self, work_title: str, author_name: str, top_k: int = 5) -> str:
        """
        Get relevant context from documents for a specific work.
        
        Args:
            work_title: Title of the work
            author_name: Name of the author
            top_k: Number of chunks to retrieve
            
        Returns:
            Concatenated relevant text
        """
        if not self.document_chunks:
            return ""
        
        relevant_chunks = self.search_relevant_chunks("", work_title, author_name, top_k=top_k)
        
        # Concatenate chunk texts
        context_parts = []
        for chunk, score in relevant_chunks:
            context_parts.append(f"[Source: {chunk['source']}, Relevance: {score:.3f}]\n{chunk['text']}")
        
        return "\n\n---\n\n".join(context_parts)
