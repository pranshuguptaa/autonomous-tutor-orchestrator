import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from src.graph_state import GraphState

load_dotenv()


class RouterSchema(BaseModel):
    tool_name: str = Field(
        ..., description="Must be one of the following: 'NoteMaker', 'FlashcardGenerator', 'ConceptExplainer', or 'clarify'"
    )


def route_query(state: GraphState) -> dict:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")

    llm = ChatOpenAI(model="gpt-4o", api_key=openai_api_key).with_structured_output(RouterSchema)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert AI agent. Your job is to analyze the user's query and route it to the most appropriate educational tool. You must choose one of the following tools:\n\n- **NoteMaker**: Use this tool when the user asks to summarize, take notes, or create a study guide on a topic.\n- **FlashcardGenerator**: Use this tool when the user wants to test their knowledge, create flashcards, or practice questions.\n- **ConceptExplainer**: Use this tool when the user asks 'what is...?', 'explain...', or expresses confusion about a specific concept.\n- **clarify**: Use this if the query is a greeting, is ambiguous, or doesn't clearly fit any other tool.",
            ),
            ("human", "{query}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke({"query": state["current_query"]})

    tool_name = response.tool_name if isinstance(response, RouterSchema) else response["tool_name"]
    state["selected_tool"] = tool_name

    return {"selected_tool": tool_name}


def handle_note_maker(state: GraphState) -> dict:
    print("---ROUTED TO NOTE MAKER---")
    return {}


def handle_flashcard_generator(state: GraphState) -> dict:
    print("---ROUTED TO FLASHCARD GENERATOR---")
    return {}


def handle_concept_explainer(state: GraphState) -> dict:
    print("---ROUTED TO CONCEPT EXPLAINER---")
    return {}


def handle_clarification(state: GraphState) -> dict:
    print("---ROUTED TO CLARIFICATION---")
    return {}
