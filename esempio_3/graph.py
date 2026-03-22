# graph.py

# assembla il grafo LangGraph e lo restituisce
# Registra i nodi
# Definisce i percorsi
# Compila e restituisce

from functools import partial
from typing import Literal

from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic

from state import State
from agents.router  import router_node
from agents.general import general_node
from agents.kb      import kb_node
from agents.contact import contact_node


# LangGraph passa lo state aggiornato, e usa il valore restituito per scegliere quale nodo attivare
def scegli_nodo(state: State) -> Literal["general", "kb_search", "contact"]:
    return state.get("intent") or "general"


def build_graph(llm: ChatAnthropic):
    # crea un grafo vuoto, riceve e restituisce uno stato
    builder = StateGraph(State)

    builder.add_node("router",    partial(router_node,  llm=llm))
    builder.add_node("general",   partial(general_node, llm=llm))
    builder.add_node("kb_search", partial(kb_node,      llm=llm))
    builder.add_node("contact",   contact_node)   # non usa llm

    # Punto di ingresso: router
    builder.add_edge(START, "router")
    
    # Condizionale: dopo che il router ha girato, 
    # LangGraph chiama scegli_nodo(state) per decidere dove andare. 
    builder.add_conditional_edges(
        "router", scegli_nodo, 
        {"general": "general", "kb_search": "kb_search", "contact": "contact"}
    )

    # Tutti e tre gli agenti terminali portano a END.
    for nodo in ("general", "kb_search", "contact"):
        builder.add_edge(nodo, END)

    # Congela tutto. Da qui in poi il grafo è immutabile e ottimizzato per l'esecuzione. 
    # invoke(state) lo attraverserà sempre nello stesso modo.
    return builder.compile()