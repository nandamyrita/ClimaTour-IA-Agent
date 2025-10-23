import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent 
from prompts import SISTEM_PROMPT 
from tools.weather_tool import get_weather_by_state
import threading

REQ_LIMIT = 10
req_count = 0

def reset_req_count():
    global req_count
    req_count = 0
    threading.Timer(60, reset_req_count).start()

reset_req_count()

def chamar_agent_com_limite(agent, mensagens):
    global req_count
    if req_count >= REQ_LIMIT:
        return "Desculpe, o limite de requisições por minuto foi atingido. Por favor, tente novamente mais tarde."
    try:
        req_count += 1  
        response = agent.invoke({"messages": mensagens})
        return response
    except Exception as e:
        if hasattr(e, "response") and getattr(e.response, "status_code", None) == 429:
            return "Desculpe, o limite de requisições por minuto foi atingido. Por favor, tente novamente mais tarde."
        return f"Ops! Ocorreu um erro inesperado: {e}"

def main():
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        print("Defina a variável de ambiente GOOGLE_API_KEY.")
        return
    if not os.getenv("OPENWEATHER_API_KEY"):
        print("Defina a variável de ambiente OPENWEATHER_API_KEY.")
        return

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, request_timeout=20, max_retries=0)
    tools = [get_weather_by_state]

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=SISTEM_PROMPT
    )

    print("Bem-vindo ao ClimaTour! 🌞🌧️")
    print("Eu posso ajudar você a descobrir o clima nos estados do Brasil e sugerir atividades legais com base nisso.")
    print("Digite o nome de um estado brasileiro para começar.")
    print("Digite 'sair' para encerrar.")

    chat_history = [] 

    while True:
        try:
            user_input = input("\nVocê: ")
            if user_input.lower() in ["sair", "exit", "quit"]:
                print("Obrigado por usar o ClimaTour! Até a próxima! 👋")
                break

            clima_resposta = get_weather_by_state(user_input)
            if "Erro" not in clima_resposta:
                print(f"ClimaTour: {clima_resposta}")
                continue

            chat_history.append({"role": "user", "content": user_input})
            response = chamar_agent_com_limite(agent, chat_history)

            if isinstance(response, str):
                print(f"ClimaTour: {response}")
                continue

            ai_response_message = response["messages"][-1]
            ai_text_content = ""
            if isinstance(ai_response_message.content, list) and len(ai_response_message.content) > 0:
                ai_text_content = ai_response_message.content[0].get("text", "")
            elif isinstance(ai_response_message.content, str):
                ai_text_content = ai_response_message.content

            chat_history.append(ai_response_message)
            print(f"ClimaTour: {ai_text_content}")

        except Exception as e:
            print(f"Ops! Ocorreu um erro inesperado: {e}")
            break

if __name__ == "__main__":
    main()
