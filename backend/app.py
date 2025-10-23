import os
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from backend.prompts import SISTEM_PROMPT
from backend.tools.weather_tool import get_weather_by_state

REQ_LIMIT = 10
req_count = 0
req_lock = threading.Lock()
chat_histories = {}  # Histórico por "usuário"

def reset_req_count():
    global req_count
    with req_lock:
        req_count = 0
    threading.Timer(60, reset_req_count).start()

def chamar_agent_com_limite(agent, mensagens):
    global req_count
    with req_lock:
        if req_count >= REQ_LIMIT:
            return "Desculpe, o limite de requisições por minuto foi atingido. Tente novamente mais tarde."
        req_count += 1
    try:
        response = agent.invoke(mensagens)
        return response
    except Exception as e:
        with req_lock:
            req_count -= 1
        return f"Erro inesperado: {e}"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")
        user_id = data.get("user_id", "default")  

        if not user_input.strip():
            return {"response": "Digite um estado válido."}

        
        if user_id not in chat_histories:
            chat_histories[user_id] = []

        chat_histories[user_id].append({"role": "user", "content": user_input})

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        tools = [get_weather_by_state]

        agent = create_agent(llm, tools=tools, system_prompt=SISTEM_PROMPT)

        response = chamar_agent_com_limite(agent, {"messages": chat_histories[user_id]})

       
        if isinstance(response, dict) and "messages" in response:
            ai_message = response["messages"][-1].content
        else:
            ai_message = str(response)

        chat_histories[user_id].append({"role": "assistant", "content": ai_message})

        return {"response": ai_message}

    except Exception as e:
        return {"response": f"Erro interno: {e}"}
