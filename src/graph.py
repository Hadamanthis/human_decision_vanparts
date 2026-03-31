from langgraph.graph import StateGraph
from state import State
from agents.classifier import classify_intent
from services.llm_client import LLMClient

llm_client = LLMClient()

def build_graph():
    graph = StateGraph(State)

    # Adiciona o node
    graph.add_node("classifier", lambda state: classify_intent(state, llm_client))
    
    # Define entrada e saída
    graph.set_entry_point("classifier")
    graph.set_finish_point("classifier")

    return graph.compile()