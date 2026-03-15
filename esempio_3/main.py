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


# llm   = ChatAnthropic(model="claude-haiku-4-5", max_tokens=256)
# graph = build_graph(llm)

# state = {
#     "messages":       [],
#     "intent":         None,
#     "contact_step":   None,
#     "contact_reason": None,
#     "contact_email":  None,
# }

# def chat(user_input: str) -> str:
#     global state
#     state = {**state, "messages": state["messages"] + [HumanMessage(content=user_input)]}
#     state = graph.invoke(state)
#     return state["messages"][-1].content

# ── Loop interattivo ──────────────────────────────────────────────────
# print("🤖 Chatbot pronto. Scrivi 'esci' per uscire.\n")

# while True:
#     user_input = input("Tu:  ").strip()

#     if not user_input:
#         continue
#     if user_input.lower() in ("esci", "exit", "quit"):
#         print("Bot: A presto! 👋")
#         break

#     risposta = chat(user_input)
#     print(f"Bot: {risposta}")
#     print(f"     ↳ intent: {state['intent']}\n")



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
    sid = req.session_id or str(uuid.uuid4())
    if sid not in sessions:
        sessions[sid] = nuova_sessione()

    state = sessions[sid]
    state = {**state, "messages": state["messages"] + [HumanMessage(content=req.message)]}
    state = app.state.graph.invoke(state)
    sessions[sid] = state

    ai_msgs = [m for m in state["messages"] if isinstance(m, AIMessage)]
    return ChatResponse(
        session_id = sid,
        reply      = ai_msgs[-1].content if ai_msgs else "",
        intent     = state.get("intent")
    )

# ── Endpoint HTML ─────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index():
    with open("chat.html") as f:
        return f.read()