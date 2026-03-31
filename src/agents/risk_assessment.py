from services.knowledge_base import KnowledgeBase
from state import State


def evaluate_risk(state: State, knowledge_base_client: KnowledgeBase) -> State:
    knowledge_base_client.search(state["product"])
