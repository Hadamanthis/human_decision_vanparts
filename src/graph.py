from langgraph.graph import StateGraph
from services.knowledge_base import KnowledgeBase
from state import State
from agents.classifier import classify_intent
from agents.resolver import resolve
from agents.risk_assessment import evaluate_risk
from agents.human_approval import human_approval
from agents.final_response import final_response
from services.llm_client import LLMClient
from langgraph.checkpoint.memory import MemorySaver

def router_after_resolver(state: State) -> str:
    if state["intention"] == "reembolso":
        return "risk_assessment"
    else:
        return "final_response"
    
def router_after_risk_assessment(state: State) -> str:
    if state["risk_level"] == "high":
        return "human_approval"
    else:
        return "final_response"

def build_graph():

    llm_client = LLMClient()
    knowledge_base_client = KnowledgeBase()
    knowledge_base_client.index()
    checkpointer = MemorySaver()

    graph = StateGraph(State)

    # Adiciona o node
    graph.add_node("classifier", lambda state: classify_intent(state, llm_client))
    graph.add_node("resolver", lambda state: resolve(state, llm_client, knowledge_base_client))
    graph.add_node("risk_assessment", lambda state: evaluate_risk(state))
    graph.add_node("human_approval", lambda state: human_approval(state))
    graph.add_node("final_response", lambda state: final_response(state))

    
    # Define as conexões entre os nós
    graph.add_edge("classifier", "resolver")
    graph.add_conditional_edges("resolver", router_after_resolver)
    graph.add_conditional_edges("risk_assessment", router_after_risk_assessment)
    graph.add_edge("human_approval", "final_response")

    # Define entrada e saída
    graph.set_entry_point("classifier")
    graph.set_finish_point("final_response")

    return graph.compile(checkpointer=checkpointer, interrupt_before=["human_approval"])