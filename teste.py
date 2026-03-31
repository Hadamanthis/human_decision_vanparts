from agents import classifier
from services.llm_client import LLMClient
from state import State
from graph import build_graph

# testes
# quero reembolso da correia dentada
# qual a garantia das peças?
# quero reembolso no radiador

state: State = {
    "user_message": "quero reembolso no radiador"
}

graph = build_graph()

config = {"configurable": {"thread_id": "1"}}
result = graph.invoke(state, config=config)

print(result)