# main.py
import uuid
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage

from graph import build_graph

load_dotenv()

# ── Sessioni in memoria ───────────────────────────────────────────────
sessions: dict = {}


def nuova_sessione():
    return {
        "messages":       [],
        "intent":         None,
        "contact_step":   None,
        "contact_reason": None,
        "contact_email":  None,
    }


# ── App FastAPI ───────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    llm = ChatAnthropic(model="claude-haiku-4-5", max_tokens=256)
    app.state.graph = build_graph(llm)
    print("✅ Grafo pronto")
    yield

app = FastAPI(lifespan=lifespan)


# ── Schema ────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    session_id: str | None = None
    message:    str


class ChatResponse(BaseModel):
    session_id: str
    reply:      str
    intent:     str | None


# ── Endpoint API ──────────────────────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    
    # Crea sessione per l'utente se non esiste già, o recupera lo stato
    sid = req.session_id or str(uuid.uuid4())
    if sid not in sessions:
        sessions[sid] = nuova_sessione()

    state = sessions[sid]
    
    # Aggiungi il nuovo messaggio dell'utente allo stato
    state = {**state, "messages": state["messages"] +
             [HumanMessage(content=req.message)]}
    
    # Manda lo state al grafo LangGraph e aspetta la risposta. 
    state = app.state.graph.invoke(state)
    
    # Salva lo stato aggiornato in memoria
    sessions[sid] = state

    # Estrae l'ultima risposta dell'AI
    ai_msgs = [m for m in state["messages"] if isinstance(m, AIMessage)]
    
    # Ritorna la risposta al client, insieme all'intent estratto e alla session_id
    return ChatResponse(
        session_id=sid,
        reply=ai_msgs[-1].content if ai_msgs else "",
        intent=state.get("intent")
    )


# ── Endpoint HTML ─────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index():
    with open("chat.html") as f:
        return f.read()