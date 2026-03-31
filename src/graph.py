from langgraph.graph import StateGraph
from services.knowledge_base import KnowledgeBase
from state import State
from agents.classifier import classify_intent
from agents.resolver import resolve
from services.llm_client import LLMClient

llm_client = LLMClient()
knowledge_base_client = KnowledgeBase()
knowledge_base_client.index()

def build_graph():
    graph = StateGraph(State)

    # Adiciona o node
    graph.add_node("classifier", lambda state: classify_intent(state, llm_client))
    graph.add_node("resolver", lambda state: resolve(state, llm_client, knowledge_base_client))
    
    # Define as conexões entre os nós
    graph.add_edge("classifier", "resolver")

    # Define entrada e saída
    graph.set_entry_point("classifier")
    graph.set_finish_point("resolver")

    return graph.compile()