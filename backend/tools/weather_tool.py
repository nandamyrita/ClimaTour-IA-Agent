import os
import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException, HTTPError
from langchain.tools import tool 

load_dotenv()

# URL da API OpenWeather 
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Mapeamento de estados brasileiros para suas capitais
STATE_TO_CITY = {
    "acre": "Rio Branco", "ac": "Rio Branco",
    "alagoas": "Maceió", "al": "Maceió",
    "amazonas": "Manaus", "am": "Manaus",
    "bahia": "Salvador", "ba": "Salvador",
    "ceara": "Fortaleza", "ce": "Fortaleza",
    "distrito federal": "Brasília", "df": "Brasília",
    "espirito santo": "Vitória", "es": "Vitória",
    "goias": "Goiânia", "go": "Goiânia",
    "maranhao": "São Luís", "ma": "São Luís",
    "mato grosso": "Cuiabá", "mt": "Cuiabá",
    "mato grosso do sul": "Campo Grande", "ms": "Campo Grande",
    "minas gerais": "Belo Horizonte", "mg": "Belo Horizonte",
    "para": "Belém", "pa": "Belém",
    "paraiba": "João Pessoa", "pb": "João Pessoa",
    "parana": "Curitiba", "pr": "Curitiba",
    "pernambuco": "Recife", "pe": "Recife",
    "piaui": "Teresina", "pi": "Teresina",
    "rio de janeiro": "Rio de Janeiro", "rj": "Rio de Janeiro",
    "rio grande do norte": "Natal", "rn": "Natal",
    "rio grande do sul": "Porto Alegre", "rs": "Porto Alegre",
    "rondonia": "Porto Velho", "ro": "Porto Velho",
    "roraima": "Boa Vista", "rr": "Boa Vista",
    "santa catarina": "Florianópolis", "sc": "Florianópolis",
    "sao paulo": "São Paulo", "sp": "São Paulo",
    "sergipe": "Aracaju", "se": "Aracaju",
    "tocantins": "Palmas", "to": "Palmas"
}

# Função para normalizar nomes de estados
def _normalize_state_name(state_name: str) -> str:
    
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ç': 'c',
        'â': 'a', 'ê': 'e', 'ô': 'o', 'ã': 'a', 'õ': 'o'
    }
    state_norm = state_name.lower().strip()
    for accented, unaccented in replacements.items():
        state_norm = state_norm.replace(accented, unaccented)
    return state_norm

# Mapear descrições de clima para categorias
def _map_weather_condition(description: str) -> str:
    desc_lower = description.lower()
    if any(k in desc_lower for k in ["céu limpo", "clear"]):
        return "Céu Limpo"
    if any(k in desc_lower for k in ["few clouds", "scattered clouds", "broken clouds"]):
        return "Parcialmente Nublado"
    if any(k in desc_lower for k in ["nublado", "cloudy", "overcast"]):
        return "Nublado"
    if any(k in desc_lower for k in ["chuva", "rain", "garoa", "tempestade", "trovoada"]):
        return "Chuvoso"
    if any(k in desc_lower for k in ["névoa", "mist", "fog", "haze"]):
        return "Nebuloso"
    if any(k in desc_lower for k in ["snow", "neve"]):
        return "Nevando"
    return description.capitalize()


# Obter o clima por estado
@tool
def get_weather_by_state(state_name: str) -> str:
    """Obtém o clima atual de um estado brasileiro fornecido pelo usuário."""
    
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