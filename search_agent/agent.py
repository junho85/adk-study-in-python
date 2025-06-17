"""
sub_agents 속성을 사용하면 400 INVALID_ARGUMENT - Tool use with function calling is unsupported 오류가 발생함
참고: https://github.com/google/adk-python/issues/53#issuecomment-2798906767
"""
from google.adk.agents import Agent
from google.adk.tools import google_search, agent_tool

MODEL = "gemini-2.5-flash-preview-05-20"
search_agent = Agent(
    model=MODEL,
    name="SearchAgent",
    instruction="""
    You're a specialist in Google Search.
    """,
    tools=[google_search]
)

root_agent = Agent(
    name="RootAgent",
    model=MODEL,
    description="Root Agent",
    tools=[agent_tool.AgentTool(agent=search_agent)],
    # sub_agents=[search_agent], # 400 INVALID_ARGUMENT - Tool use with function calling is unsupported
)