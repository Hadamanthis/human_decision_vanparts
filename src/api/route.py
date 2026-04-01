from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()

class MessageRequest(BaseModel):
    thread_id: str
    user_message: str

class ApprovalRequest(BaseModel):
    approved: bool

@router.post("/message")
def message(request: Request, body: MessageRequest):
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": body.thread_id}}

    result = graph.invoke({"user_message": body.user_message}, config=config)

    snapshot = graph.get_state(config)

    return {
        "thread_id": body.thread_id,
        "final_message": result.get("final_message"),
        "awaiting_approval": snapshot.next == ("human_approval",)
    }

@router.post("/approve/{thread_id}")
def approve(request: Request, thread_id: str, body: ApprovalRequest):
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": thread_id}}

    graph.update_state(config, {"approved": body.approved})
    result = graph.invoke(None, config=config)

    return {
        "thread_id": thread_id,
        "final_message": result.get("final_message")
    }

@router.get("/status/{thread_id}")
def status(request: Request, thread_id: str):
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": thread_id}}
    snapshot = graph.get_state(config)

    return {
        "thread_id": thread_id,
        "state": snapshot.values,
        "awaiting_approval": snapshot.next == ("human_approval",)
    }