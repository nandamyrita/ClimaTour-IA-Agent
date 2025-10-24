from backend.tools.weather_tool import get_weather_by_state

def test_get_weather_estado_valido():
    result = get_weather_by_state("São Paulo")
    assert "Clima em" in result or "Erro" not in result

def test_get_weather_estado_invalido():
    result = get_weather_by_state("EstadoFake")
    assert "Erro" in result
