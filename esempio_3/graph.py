# graph.py
from functools import partial
from typing import Literal

from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic

from state import State
from agents.router  import router_node
from agents.general import general_node
from agents.kb      import kb_node
from agents.contact import contact_node


def scegli_nodo(state: State) -> Literal["general", "kb_search", "contact"]:
    return state.get("intent") or "general"


def build_graph(llm: ChatAnthropic):
    builder = StateGraph(State)

    builder.add_node("router",    partial(router_node,  llm=llm))
    builder.add_node("general",   partial(general_node, llm=llm))
    builder.add_node("kb_search", partial(kb_node,      llm=llm))
    builder.add_node("contact",   contact_node)   # non usa llm

    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router", scegli_nodo,
        {"general": "general", "kb_search": "kb_search", "contact": "contact"}
    )

    for nodo in ("general", "kb_search", "contact"):
        builder.add_edge(nodo, END)

    return builder.compile()