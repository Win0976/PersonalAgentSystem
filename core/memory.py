import chromadb
from chromadb.utils import embedding_functions

class MemorySystem:
    def __init__(self):
        # Initialisiert die Vektordatenbank lokal im Ordner 'chroma_db'
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="imperium_gedaechtnis",
            embedding_function=self.ef
        )

    def speichern(self, text: str, metadaten: dict = None):
        """Speichert einen neuen Gedanken im Gedächtnis."""
        doc_id = str(hash(text))  # Einfache ID-Generierung
        self.collection.add(
            documents=[text],
            metadatas=[metadaten or {}],
            ids=[doc_id]
        )

    def abrufen(self, query: str, n_results: int = 3):
        """Sucht nach ähnlichen Gedanken (semantische Suche)."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0]