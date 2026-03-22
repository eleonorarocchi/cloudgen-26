# state.py

# Dizionario condiviso per tenere traccia dello stato della conversazione
# che viaggia attraverso il grafo ad ogni invocazione. 
# contact_step dice dove siamo nel flusso, 
# contact_reason e contact_email accumulano i dati raccolti.

from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages:       Annotated[list, add_messages] # La lista dei messaggi, con decoratore per accumularli
    intent:         str | None   # "general" | "kb_search" | "contact"
    contact_step:   str | None   # None | "ask_reason" | "ask_email" | "done"
    contact_reason: str | None   # Il motivo per cui l'utente vuole essere ricontattato
    contact_email:  str | None   # L'email dell'utente