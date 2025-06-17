from google.adk.agents import Agent
from google.adk.tools import google_search, agent_tool

# MODEL="gemini-2.0-flash"
MODEL = "gemini-2.5-flash-preview-05-20"
# MODEL = "gemini-1.5-flash-latest" # {"error": "Google search tool can not be used with other tools in Gemini 1.x."}

idea_agent = Agent(
    model=MODEL,
    name="IdeaAgent",
    description="Brainstorms creative and exciting weekend travel ideas based on user preferences or requests.",
    instruction="You are a creative travel agent. Use the tool to brainstorm and respond to the user with 3 exciting weekend trip ideas based on the user's request.",
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

refiner_agent = Agent(
    model=MODEL,
    name="RefinerAgent",
    description="Reviews provided travel ideas and selects only those estimated to cost under the provided budget for a weekend trip.",
    instruction="Use your tools to review the provided trip ideas. Respond ONLY with the ideas likely under the provided budget for a weekend. If none seem to fit, say so",
    tools=[google_search],
    disallow_transfer_to_peers=True,
)

print("""1. First, use "{idea_agent}" to brainstorm ideas based on the user's request.
        2. Then, use "{refiner_agent}" to take those ideas to filter them for the provided budget.""")

root_agent = Agent(
    model=MODEL,
    name="PlannerAgent",
    description="Root agent",
    instruction=f"""You are a Trip Planner, coordinating specialist agents.
    Your goal is to provide budget-friendly weekend trip ideas. For each user request, follow the below instructions:
        1. First, use "{idea_agent}" to brainstorm ideas based on the user's request.
        2. Then, use "{refiner_agent}" to take those ideas to filter them for the provided budget.
        3. Present the final, refined list to the user along with the budget.
    """,
    # sub_agents=[idea_agent, refiner_agent],
    tools=[agent_tool.AgentTool(agent=idea_agent), agent_tool.AgentTool(agent=refiner_agent)],
)
