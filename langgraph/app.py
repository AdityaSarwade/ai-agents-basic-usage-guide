from langgraph.graph import StateGraph, MessagesState
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage


@tool
def search(query: str):
    """Simulate a Web Search

    Args:
        query (str): Query for web search
    """
    if "weather" in query.lower():
        return "It is sunny"

    return "No data available"


tools = [search]
tool_node = ToolNode(tools)

workflow = StateGraph(MessagesState)

model = AzureChatOpenAI(
    azure_deployment="REDACTED",
    api_key="REDACTED",
    azure_endpoint="REDACTED",
    api_version="REDACTED",
    temperature=0,
).bind_tools(tools, tool_choice="auto")

messages = [{"role": "user", "content": "hey"}]  # noqa E501


def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState):
    if state["messages"][-1].tool_calls:
        return "tools"
    return "END"


workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")


checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)


# Test cases
queries = [
    "What is the weather today?",  # Should use search tool
    "Please repeat: Hello world",  # Should respond directly
]

for query in queries:
    print("\n----- Testing:", query)
    final_state = app.invoke(
        {"messages": [HumanMessage(content=query)]},
        config={"configurable": {"thread_id": 1}},
    )
    print("Response:", final_state["messages"][-1].content)
