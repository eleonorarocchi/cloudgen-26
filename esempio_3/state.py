# state.py
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages:       Annotated[list, add_messages]
    intent:         str | None
    contact_step:   str | None   # None | "ask_reason" | "ask_email" | "done"
    contact_reason: str | None
    contact_email:  str | None