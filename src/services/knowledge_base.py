import chromadb
from pathlib import Path
import hashlib
import logging

class KnowledgeBase:
    def __init__(self, knowledge_base_dir="./data/knowledge_base", vector_base_dir="./vector_base"):
        self.knowledge_path = Path(knowledge_base_dir)
        self.client = chromadb.PersistentClient(path=vector_base_dir)
        self.collection = self.client.get_or_create_collection(name="max-vanparts")
        self.logger = logging.getLogger(__name__)

    def index(self) -> None:
        """ Indexa a base de conhecimento em um vector database """

        self.logger.info(f"Iniciando indexação da knowledge base {self.knowledge_path.name}")

        for _file in self.knowledge_path.glob("*.txt"):

            self.logger.info(f"Iniciando indexação do arquivo {_file.name}.")

            with open(_file, "r", encoding="utf-8") as f:
                content = f.read()

                file_hash = hashlib.md5(content.encode()).hexdigest()

                # Buscando se existe a primeira sentença desse arquivo na base
                existing_file = self.collection.get(ids=[f"{_file.stem}_{0}"])

                # Se já existe na base, não precisa indexar novamente
                if existing_file["ids"]:
                    if existing_file["metadatas"][0]["hash"] == file_hash:
                        
                        self.logger.info(f"{_file.name} já estava presente na vector base.")

                        continue

                for index, sentence in enumerate(content.split(sep="\n\n")):
                    sentence_id = f"{_file.stem}_{index}" 

                    self.collection.upsert(
                        ids=[sentence_id],
                        documents=[sentence],
                        metadatas=[{"hash": file_hash, "source": _file.stem}]
                    )
        
        self.logger.info(f"Indexação do arquivo {_file.name} concluída.")

    def search(self, query: str, n_results: int = 1, source: str | None = None) -> list[str]:
        """ Busca por um trecho de texto na base de conhecimento e retorna os n_results trechos mais relevantes """

        self.logger.info(f"Realizando busca na knowledge base, query: '{query}'")

        if source is None:
            query_results = self.collection.query(query_texts=[query], n_results=n_results).get("documents")
        else:
            query_results = self.collection.query(query_texts=[query], n_results=n_results, where={"source": source}).get("documents")

        documents_flat = [document for sublist in query_results for document in sublist]

        results = list(set(documents_flat))

        return results
