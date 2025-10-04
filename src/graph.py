import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph

from src.graph_state import GraphState
from src.nodes import (
    handle_clarification,
    handle_concept_explainer,
    handle_flashcard_generator,
    handle_note_maker,
    route_query,
)

load_dotenv()


def decide_next_node(state: GraphState) -> str:
    """
    Determines the next node to execute based on the router's decision.
    """
    selected_tool = state.get("selected_tool", "").lower()

    if "notemaker" in selected_tool:
        return "note_maker_node"
    elif "flashcardgenerator" in selected_tool:
        return "flashcard_generator_node"
    elif "conceptexplainer" in selected_tool:
        return "concept_explainer_node"
    else:
        return "clarification_node"


workflow = StateGraph(GraphState)

workflow.add_node("router", route_query)
workflow.add_node("note_maker_node", handle_note_maker)
workflow.add_node("flashcard_generator_node", handle_flashcard_generator)
workflow.add_node("concept_explainer_node", handle_concept_explainer)
workflow.add_node("clarification_node", handle_clarification)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    decide_next_node,
    {
        "note_maker_node": "note_maker_node",
        "flashcard_generator_node": "flashcard_generator_node",
        "concept_explainer_node": "concept_explainer_node",
        "clarification_node": "clarification_node",
    },
)

app = workflow.compile()


if __name__ == "__main__":
    user_profile_data = {
        "user_id": "test_user",
        "name": "Test",
        "grade_level": "10",
        "learning_style_summary": "visual",
        "emotional_state_summary": "calm",
        "mastery_level_summary": "Level 5",
    }
    chat_history_data = []

    query = "Hi there!"

    inputs = {
        "current_query": query,
        "user_profile": user_profile_data,
        "chat_history": chat_history_data,
    }

    result = app.invoke(inputs)
    print("\n---FINAL STATE---")
    print(result)
