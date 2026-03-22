# agents/contact.py

# L'agente contatto deve fare tre domande in sequenza:
#   su turni separati, 
#   ricordando le risposte precedenti.
# Lo fa utilizzando State, uno TypedDict condiviso.

import re
from langchain_core.messages import AIMessage
from state import State

EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")

# Funzione di utilità per capire se un testo sembra un'email.
def _sembra_email(testo: str) -> bool:
    return bool(EMAIL_REGEX.search(testo))


def contact_node(state: State) -> dict:
    # dove siamo nel flusso
    step  = state.get("contact_step")
    #cosa ha scritto l'utente 
    testo = state["messages"][-1].content.strip()

    # ── Turno 1: primo contatto con l'utente
    if step is None:
        return {
            "messages": [AIMessage(content=(
                "Certo! 😊 **Per quale motivo vorresti essere contattata?**\n"
                "_(es. richiesta commerciale, supporto tecnico, partnership)_"
            ))],
            "contact_step": "ask_reason"
        }

    # ── Turno 2: aspettiamo il motivo 
    if step == "ask_reason":
        # Si aspetta il motivo, ma prima controlla se l'utente ha scritto un'email al posto del motivo.
        
        # In quel caso rimane sullo stesso step invece di andare avanti. 
        if _sembra_email(testo):
            return {
                "messages": [AIMessage(content=(
                    "Ho visto che hai già scritto la tua email! 👀\n"
                    "Prima però dimmi: **per quale motivo vorresti essere contattata?**"
                ))],
                "contact_step": "ask_reason"   # restiamo qui
            }

        # Se il testo sembra un motivo valido, lo salva in contact_reason e avanza.
        return {
            "messages": [AIMessage(content=(
                f"Perfetto, ho preso nota: _{testo}_\n\n"
                "**Qual è la tua email** per essere ricontattata?"
            ))],
            "contact_step":   "ask_email",
            "contact_reason": testo
        }

    # ── Turno 3: aspettiamo l'email ───────────────────────────────────
    if step == "ask_email":
        match = EMAIL_REGEX.search(testo)

        # Cerca un'email con regex nel testo. 
        # Se non la trova, rimanda indietro senza aggiornare contact_step — al prossimo turno si ritorna qui. 
        if not match:
            return {"messages": [AIMessage(content=(
                "Non trovo un'email valida nel messaggio. 🤔\n"
                "Potresti riprovare? _(es. nome@esempio.com)_"
            ))]}

        # Se la trova, salva l'email e chiude il flusso con "done".
        email  = match.group(0)
        reason = state.get("contact_reason", "—")
        return {
            "messages": [AIMessage(content=(
                f"✅ **Registrato!**\n"
                f"📌 Motivo: {reason}\n"
                f"📧 Email: {email}\n\n"
                "Ti risponderemo entro 1-2 giorni lavorativi. Grazie! 🙏"
            ))],
            "contact_step":  "done",
            "contact_email": email
        }

    # ── Flusso già completato ─────────────────────────────────────────
    return {"messages": [AIMessage(content=(
        "La tua richiesta è già stata registrata. "
        "Riceverai presto una risposta. Posso aiutarti con altro?"
    ))]}
    