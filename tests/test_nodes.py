import pytest
from unittest.mock import patch
from src.nodes import contextual_adaptation, route_query, RouterSchema

def test_adaptation_for_visual_learner():
    # Arrange
    state = {
        "user_profile": {
            "user_id": "test_user",
            "name": "Test",
            "grade_level": "10",
            "learning_style_summary": "visual",
            "emotional_state_summary": "anxious",
            "mastery_level_summary": "Level 2"
        },
        "extracted_parameters": {
            "topic": "mitochondria",
            "count": 5,
            "difficulty": "medium",
            "subject": "biology"
        }
    }

    # Act
    result = contextual_adaptation(state)

    # Assert
    assert result["extracted_parameters"]["include_analogies"] is True

@patch('src.nodes.ChatPromptTemplate')
@patch('src.nodes.ChatGoogleGenerativeAI')
def test_router_selects_notemaker(mock_llm, mock_prompt):
    # Arrange
    # Create a mock for the entire chain object
    mock_chain = mock_prompt.from_messages.return_value | mock_llm.return_value.with_structured_output.return_value
    
    # Configure the final .invoke() call on the chain to return our desired object
    mock_chain.invoke.return_value = RouterSchema(tool_name="NoteMaker")
    
    state = {
        "current_query": "make me notes",
        "user_profile": {},
        "chat_history": []
    }

    # Act
    # We need to temporarily patch the 'chain' object inside the function's scope
    with patch('src.nodes.chain', mock_chain):
        result = route_query(state)

    # Assert
    assert result["selected_tool"] == "NoteMaker"