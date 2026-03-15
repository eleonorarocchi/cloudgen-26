# agents/kb.py
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from state import State

# La knowledge base vive qui, vicino all'agente che la usa
DOCS = [
    {
        "keywords": ["prezzo", "costo", "piano", "€"],
        "content":  "Piano Base: 29€/mese — Piano Pro: 79€/mese — Enterprise: su richiesta."
    },
    {
        "keywords": ["trial", "gratis", "prova", "free"],
        "content":  "Trial gratuito di 14 giorni, senza carta di credito."
    },
    {
        "keywords": ["funzioni", "feature", "api", "export"],
        "content":  "Dashboard real-time, API REST, export CSV/PDF, SSO (Pro ed Enterprise)."
    },
    {
        "keywords": ["supporto", "assistenza", "orari", "help"],
        "content":  "Supporto lun-ven 9-18. Pro: risposta entro 4h. Enterprise: CSM dedicato."
    },
]


def _search(query: str) -> str:
    """Cerca i documenti rilevanti per keyword. Funzione privata del modulo."""
    q       = query.lower()
    trovati = [d["content"] for d in DOCS if any(k in q for k in d["keywords"])]
    return "\n".join(trovati) if trovati else "\n".join(d["content"] for d in DOCS)
    #                                          ↑ fallback: restituisce tutto


def kb_node(state: State, llm: ChatAnthropic) -> dict:
    """Cerca nella KB e genera una risposta basata sui documenti trovati."""
    query   = state["messages"][-1].content
    context = _search(query)

    r = llm.invoke([
        SystemMessage(content=(
            "Rispondi SOLO con le informazioni qui sotto. "
            "Se non ci sono informazioni pertinenti, dillo chiaramente.\n\n"
            f"--- KNOWLEDGE BASE ---\n{context}\n----------------------"
        )),
        HumanMessage(content=query)
    ])
    return {"messages": [AIMessage(content=r.content)]}