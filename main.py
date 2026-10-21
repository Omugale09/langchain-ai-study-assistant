import os
from typing import Annotated
from typing_extensions import TypedDict

import serpapi
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from local_openai import ChatOpenAI_mock

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


@tool
def internet_search(query: str) -> str:
    """Search Google for current information."""
    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        return "SERPAPI_KEY is missing from .env."

    try:
        client = serpapi.Client(api_key=api_key, timeout=20)
        results = client.search({
            "engine": "google",
            "q": query,
            "num": 5,
        })

        items = results.get("organic_results", [])

        if not items:
            return "No search results found."

        return "\n\n".join(
            f"Title: {item.get('title', '')}\n"
            f"Summary: {item.get('snippet', '')}\n"
            f"URL: {item.get('link', '')}"
            for item in items
        )

    except Exception as error:
        return f"Search failed: {error}"


def build_graph():
    model_name = os.getenv("LM_STUDIO_CHAT_MODEL")

    if not model_name:
        raise ValueError(
            "Set LM_STUDIO_CHAT_MODEL in your .env file."
        )

    llm = ChatOpenAI_mock(
        model=model_name,
        temperature=0
    )

    tools = [internet_search]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        system_message = SystemMessage(
            content=(
                "You are a helpful AI assistant. "
                "Explain concepts simply. Use internet_search "
                "when current information is needed."
            )
        )

        response = llm_with_tools.invoke(
            [system_message] + state["messages"]
        )

        return {"messages": [response]}

    builder = StateGraph(State)

    builder.add_node("chatbot", chatbot)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "chatbot")

    builder.add_conditional_edges(
        "chatbot",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        }
    )

    builder.add_edge("tools", "chatbot")

    return builder.compile()


def main():
    graph = build_graph()
    messages = []

    print("AI Assistant started!")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            result = graph.invoke({
                "messages": messages + [
                    HumanMessage(content=question)
                ]
            })

            messages = result["messages"]
            print("\nAI:", messages[-1].content, "\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()
