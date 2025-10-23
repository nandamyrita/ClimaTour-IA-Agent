import os
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException, HTTPError
from langchain.tools import tool 

load_dotenv()

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
STATE_TO_CITY = {
    "acre": "Rio Branco", "alagoas": "Maceió", "amapa": "Macapá", "amazonas": "Manaus",
    "bahia": "Salvador", "ceara": "Fortaleza", "distrito federal": "Brasília",
    "espirito santo": "Vitória", "goias": "Goiânia", "maranhao": "São Luís",
    "mato grosso": "Cuiabá", "mato grosso do sul": "Campo Grande",
    "minas gerais": "Belo Horizonte", "para": "Belém", "paraiba": "João Pessoa",
    "parana": "Curitiba", "pernambuco": "Recife", "piaui": "Teresina",
    "rio de janeiro": "Rio de Janeiro", "rio grande do norte": "Natal",
    "rio grande do sul": "Porto Alegre", "rondonia": "Porto Velho",
    "roraima": "Boa Vista", "santa catarina": "Florianópolis",
    "sao paulo": "São Paulo", "sergipe": "Aracaju", "tocantins": "Palmas"
}

def _normalize_state_name(state_name: str) -> str:
    
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ç': 'c',
        'â': 'a', 'ê': 'e', 'ô': 'o', 'ã': 'a', 'õ': 'o'
    }
    state_norm = state_name.lower().strip()
    for accented, unaccented in replacements.items():
        state_norm = state_norm.replace(accented, unaccented)
    return state_norm

def _map_weather_condition(description: str) -> str:
    desc_lower = description.lower()
    if any(k in desc_lower for k in ["céu limpo", "ensolarado"]):
        return "Ensolarado"
    if any(k in desc_lower for k in ["chuva", "garoa", "tempestade", "trovoada"]):
        return "Chuvoso"
    if any(k in desc_lower for k in ["nublado", "nuvens", "névoa", "nevoeiro"]):
        return "Nublado"
    return description.capitalize()


@tool(description="Obtém o clima atual de um estado brasileiro fornecido pelo usuário.")
def get_weather_by_state(state_name: str) -> str:
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Erro: Chave da API OpenWeather (OPENWEATHER_API_KEY) não encontrada."
    
    state_norm = _normalize_state_name(state_name)
    city = STATE_TO_CITY.get(state_norm)
    
    if not city:
        return f"Erro: Estado '{state_name}' não reconhecido."

    params = {
        "q": f"{city},BR", "appid": api_key,
        "units": "metric", "lang": "pt_br"
    }

    try:
        resp = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        temperatura = data["main"]["temp"]
        condicao_raw = data["weather"][0]["description"]
        condicao_mapeada = _map_weather_condition(condicao_raw)

        
        return f"Clima em {city} ({state_name}): {condicao_mapeada}, {temperatura:.1f}°C."

    except HTTPError as e:
        if e.response.status_code == 401:
            return "Erro: Chave da API OpenWeather inválida."
        return f"Erro HTTP: {e.response.status_code}."
    except RequestException:
        return "Erro: Não foi possível conectar à API de clima."
    except Exception as e:
        return f"Erro inesperado ao processar o clima: {e}"