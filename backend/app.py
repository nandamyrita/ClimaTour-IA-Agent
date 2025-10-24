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
chat_histories = {} 

# Reseta o contador de requisições a cada minuto
def reset_req_count():
    global req_count
    with req_lock:
        req_count = 0
    threading.Timer(60, reset_req_count).start()

#Controle de limite de requisições
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

# Conecta com o frontend
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

        if isinstance(user_input, list):
            user_input = " ".join(str(x) for x in user_input)
        else:
            user_input = str(user_input)

        user_input = user_input.strip()

        # Condições de saida para o chat
        if user_input.lower() == "sair":
            chat_histories.pop(user_id, None)
            return {"response": "👋 Até mais! Chat finalizado com sucesso."}

        from backend.tools.weather_tool import _normalize_state_name, STATE_TO_CITY
        state_norm = _normalize_state_name(user_input)

        if state_norm not in STATE_TO_CITY:
            return {"response": f"Opa! 😅 Não encontrei o estado '{user_input}'. Verifique se está escrito corretamente ou digite 'sair' para encerrar o chat!"}

        if user_id not in chat_histories:
            chat_histories[user_id] = []

        # Adiciona a mensagem do usuário ao histórico
        chat_histories[user_id].append({"role": "user", "content": user_input}) 

        # Configura o agente com o prompt e a tool
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        tools = [get_weather_by_state]
        agent = create_agent(llm, tools=tools, system_prompt=SISTEM_PROMPT)

        response = chamar_agent_com_limite(agent, {"messages": chat_histories[user_id]})

        # Processa a resposta do agente
        ai_message = ""
        if isinstance(response, dict):
            if "messages" in response and response["messages"]:
                last_msg = response["messages"][-1]
                ai_message = getattr(last_msg, "content", str(last_msg))
            else:
                ai_message = str(response)
        else:
            ai_message = str(response)

        chat_histories[user_id].append({"role": "assistant", "content": ai_message})

        return {"response": ai_message}

    except Exception as e:
        return {"response": f"Erro interno: {e}"}


