# ESEMPIO 2

## 1. Crea un ambiente virtuale (SEMPRE farlo, è buona pratica)
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# oppure: venv\Scripts\activate  # Windows

## 2. Installa le dipendenze
pip3 install langchain langchain-anthropic fastapi uvicorn python-dotenv

## 3. Esegui
python3 hello.py