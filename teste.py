from agents import classifier
from services.llm_client import LLMClient
from state import State
from graph import build_graph

state: State = {
    "user_message": "quero reembolso da correia dentada",
    "intent": None
}

graph = build_graph()

result = graph.invoke(state)

print(result)