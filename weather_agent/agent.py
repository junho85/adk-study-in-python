from typing import Dict

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

# MODEL = "gemini-2.0-flash-exp"
MODEL = "gemini-2.5-flash-preview-05-20"
ANTHROPIC_MODEL = "anthropic/claude-3-sonnet-20240229"


def get_weather(city: str) -> Dict:
    # 모범 사례: 더욱 쉬운 디버깅을 위한 도구 실행 기록
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "")  # 기본 입력 정규화

    # 단순화를 위한 모의 날씨 데이터(1단계 구조와 일치)
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
        "chicago": {"status": "success", "report": "The weather in Chicago is sunny with a temperature of 25°C."},
        "toronto": {"status": "success", "report": "It's partly cloudy in Toronto with a temperature of 30°C."},
        "chennai": {"status": "success", "report": "It's rainy in Chennai with a temperature of 15°C."},
    }

    # 모범 사례: 도구 내에서 잠재적 오류를 적절하게 처리
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}


greeting_agent = Agent(
    model=LiteLlm(model=ANTHROPIC_MODEL),
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. " "Do not engage in any other conversation or tasks.",
    # 위임에 중요한 점: 기능에 대한 명확한 설명
    description="Handles simple greetings and hellos",

)

farewell_agent = Agent(
    model=LiteLlm(model=ANTHROPIC_MODEL),
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                "Do not perform any other actions.",
    # 위임에 중요한 점: 기능에 대한 명확한 설명
    description="Handles simple farewells and goodbyes",
)

root_agent = Agent(
    name="weather_agent_v2",
    model=MODEL,
    description="You are the main Weather Agent, coordinating a team. - Your main task: Provide weather using the `get_weather` tool. Handle its 'status' response ('report' or 'error_message'). - Delegation Rules: - If the user gives a simple greeting (like 'Hi', 'Hello'), delegate to `greeting_agent`. - If the user gives a simple farewell (like 'Bye', 'See you'), delegate to `farewell_agent`. - Handle weather requests yourself using `get_weather`. - For other queries, state clearly if you cannot handle them.",
    tools=[get_weather],  # 루트 에이전트에는 여전히 날씨 도구가 필요함
    sub_agents=[greeting_agent, farewell_agent]
)
