# AI Tutor Orchestrator

## Overview
The AI Tutor Orchestrator is an intelligent, autonomous middleware system designed for the Yophoria Innovation Challenge by YoLearn.ai. It acts as a "brain" that seamlessly connects a conversational AI tutor to a wide array of educational tools (e.g., NoteMaker, FlashcardGenerator, ConceptExplainer), enabling dynamic query routing, parameter extraction, and personalized responses without manual intervention. Built with LangGraph and Google Gemini, it analyzes natural conversations, infers missing details, and adapts to user contexts like learning styles (e.g., visual), emotional states (e.g., confused), and mastery levels. This solves the problem of disjointed AI tutoring by making tool integration autonomous and scalable for 80+ potential tools.

## Core Technologies
This project leverages the following key technologies and libraries:
- **Python**: The primary programming language for the entire application.
- **FastAPI**: Used to build the main web API server for handling HTTP requests and providing endpoints like `/orchestrate`.
- **LangGraph**: Powers the agent workflow, defining states, nodes, and edges for query routing, processing, and execution.
- **LangChain**: Integrates Google Gemini for AI-driven decision-making, parameter extraction, and response generation.
- **Google Gemini**: Provides the core AI model for routing queries and adapting responses based on context.
- **Pydantic**: Employed for data validation and schema definitions, ensuring robust input/output handling.
- **Uvicorn**: Serves as the ASGI server for running the FastAPI application.
- **Python-dotenv**: Manages environment variables for secure configuration (e.g., API keys).
- **HTTPX**: Handles asynchronous HTTP requests to external mock services and tools.
- **Pytest**: Used for writing and running automated unit and integration tests.

## Project Structure
The project is organized to promote modularity, scalability, and ease of maintenance:
- **[src/main.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/src/main.py:0:0-0:0)**: The entry point for the FastAPI application, defining API endpoints like `/orchestrate` for handling user queries and returning orchestrated responses.
- **[src/graph.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/src/graph.py:0:0-0:0)**: Assembles the LangGraph workflow, including state definitions, node connections, and the overall agent graph for processing queries end-to-end.
- **[src/nodes.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/src/nodes.py:0:0-0:0)**: Contains the core functions (nodes) implementing the agent's logic, such as `route_query` for tool selection, `extract_*_parameters` for parameter inference, `contextual_adaptation` for personalization, and `execute_tool` for API calls.
- **[src/schemas.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/src/schemas.py:0:0-0:0)**: Defines Pydantic data models for validation, including RouterSchema for tool decisions and input schemas for tools like NoteMaker and FlashcardGenerator.
- **`src/graph_state.py`**: Defines the `GraphState` type for managing shared state (e.g., query, user profile, chat history) across nodes.
- **`mock_tools/`**: A directory with FastAPI-based mock servers simulating external educational tools (e.g., `mock_note_maker.py` for note creation, `mock_flashcard_generator.py` for quizzes, `mock_concept_explainer.py` for explanations).
- **`tests/`**: Contains automated tests (e.g., [test_nodes.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/tests/test_nodes.py:0:0-0:0) for node logic and [test_integration.py](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/tests/test_integration.py:0:0-0:0) for end-to-end workflows) using Pytest.
- **`requirements.txt`**: Lists all Python dependencies required for installation.
- **[.env](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/.env:0:0-0:0)**: Configuration file for environment variables, such as the Google API key.
- **`streamlit_app.py`**: (Inferred from context) A Streamlit frontend for interactive querying, allowing users to chat with the orchestrator and view responses in a web UI.

## Features
- **Autonomous Tool Routing**: Analyzes queries (e.g., "make me notes") and selects the appropriate tool using AI.
- **Intelligent Parameter Extraction**: Parses conversations to extract/infer parameters (e.g., topic from context) and validates against tool schemas.
- **Personalization**: Adapts responses based on user profiles—e.g., adds analogies for visual learners or examples for confused students.
- **State Management**: Maintains conversation context and user data across interactions.
- **Error Handling and Validation**: Gracefully handles missing params, API failures, and schema errors.
- **Scalability**: Designed for 80+ tools via extensible endpoints and LangGraph architecture.
- **Testing and Demo**: Includes unit tests, integration tests, and a Streamlit app for live interaction.

## Setup Instructions
Follow these steps to set up the project locally:

1. **Prerequisites**:
   - Ensure you have Python 3.9 or higher installed on your system. You can check your version with `python3 --version`.

2. **Installation**:
   - Clone the repository and navigate to the project directory.
   - Install the required dependencies by running:
     ```
     pip3 install -r requirements.txt
     ```

3. **Configuration**:
   - Create a [.env](cci:7://file:///Users/pranshugupta/Desktop/Hackathon/autonomous-tutor-orchestrator/.env:0:0-0:0) file in the root directory of the project.
   - Add the following variable, replacing `YOUR_ACTUAL_API_KEY` with your real Google AI API key obtained from Google AI Studio (it should start with `AIzaSy` and be 39 characters long):
     ```
     GOOGLE_API_KEY=AIzaSyB1mZL1cagK4-yimjxwt--0QQkne9sUeN4
     ```
     - This key is required for Google Gemini integration; without it, routing and adaptation will fail.

## Running the Application
To run the full application, start the mock servers and main server in separate terminals (as the system integrates with external simulations):

1. **Terminal 1: Start Mock Servers** (repeat for each tool):
   - Run a mock server for concept explanation:
     ```
     uvicorn mock_tools.mock_concept_explainer:app --port 8003
     ```
   - Similarly for others: `mock_note_maker` (port 8001), `mock_flashcard_generator` (port 8002).
   - This simulates external tools responding to API calls.

2. **Terminal 2: Start the Main Agent Server**:
   - Run the main FastAPI application:
     ```
     uvicorn src.main:api --reload
     ```
   - This starts the server on `http://127.0.0.1:8000` with auto-reload for development.

3. **Optional: Run the Streamlit Frontend**:
   - In a third terminal, launch the interactive UI:
     ```
     streamlit run streamlit_app.py
     ```
   - Access at `http://localhost:8501` for a chat interface.

   Once running, the system handles queries via `/orchestrate` (e.g., POST with {"query": "explain photosynthesis"}) and returns adapted responses.

## How to Test
Test the application using the following methods:

1. **Automated Tests**:
   - Run the test suite to verify node functions and overall behavior:
     ```
     python3 -m pytest tests/test_nodes.py -v
     ```
   - Also run integration tests: `python3 -m pytest tests/test_integration.py -v`.
   - This executes unit tests for core logic using Pytest.

2. **Interactive API**:
   - Access the auto-generated FastAPI documentation at `http://127.0.0.1:8000/docs` in your web browser.
   - Use the interactive Swagger UI to test the `/orchestrate` endpoint live by providing sample queries (e.g., "explain photosynthesis") and viewing JSON responses from routed tools.

3. **Live Demo via Streamlit**:
   - Use the Streamlit app at `http://localhost:8501` to chat interactively and see personalized responses in real-time.

## Architecture and Workflow
The system uses a LangGraph-based architecture for scalability:
- **State Management**: `GraphState` tracks query, profile, history.
- **Nodes**: `route_query` (selects tool), `extract_*` (infers params), `contextual_adaptation` (personalizes), `execute_tool` (calls APIs).
- **Edges**: Connect nodes for sequential processing.
- **Scalability**: Easily extend to 80+ tools by adding to `tool_endpoints` in `execute_tool`.

This aligns with the PRD's goals for autonomous integration, parameter extraction, and personalization, evaluated on accuracy, completeness, architecture, UX, and implementation.

## Demo Script for 5-Minute Video
For a quick showcase, use this script (timings included):
- [0:00-0:45] Intro: Present vision and problem-solving.
- [0:45-1:45] Overview: Highlight features and tech.
- [1:45-3:45] Live Demo: Run servers, test queries via API/Streamlit.
- [3:45-4:45] Technical: Show code, tests.
- [4:45-5:00] Conclusion: Summarize impact.

For full details, refer to the demo script in previous responses.