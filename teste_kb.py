from services.knowledge_base import KnowledgeBase
import logging

logging.basicConfig(level=logging.INFO)

kb = KnowledgeBase()
kb.index()

results = kb.search("reembolso acima de 500 reais")

print(results)