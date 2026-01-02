import pytest
from unittest.mock import patch, MagicMock
from backend.src.agent.main import run_agent
from backend.src.services.mcp_client import McpClient

@pytest.fixture
def mock_openai_client():
    with patch("backend.src.agent.main.client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_mcp_client():
    with patch("backend.src.agent.main.mcp_client") as mock_client:
        yield mock_client

def test_add_task_flow_success(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for adding a task when the agent successfully
    calls the add_task tool and the backend confirms.
    """
    # Mock the OpenAI response to indicate a tool call for 'add_task'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="add_task",
                                    arguments='{"description": "buy milk"}'
                                ),
                                id="call_123"
                            )
                        ]
                    )
                )
            ]
        ),
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="Task 'buy milk' has been added successfully.")
                )
            ]
        )
    ]

    # Mock the McpClient's add_task method to return a success response
    mock_mcp_client.add_task.return_value = {"id": "1", "description": "buy milk", "status": "pending"}

    user_message = "add a task to buy milk"
    response = run_agent(user_message)

    # Assert that add_task was called with the correct argument
    mock_mcp_client.add_task.assert_called_once_with(description="buy milk")

    # Assert the final response from the agent
    assert "Task 'buy milk' has been added successfully." in response

def test_add_task_flow_failure(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for adding a task when the backend call fails.
    """
    # Mock the OpenAI response to indicate a tool call for 'add_task'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="add_task",
                                    arguments='{"description": "buy bread"}'
                                ),
                                id="call_456"
                            )
                        ]
                    )
                )
            ]
        ),
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="An error occurred while adding the task.")
                )
            ]
        )
    ]

    # Mock the McpClient's add_task method to raise an exception
    mock_mcp_client.add_task.side_effect = Exception("Backend service unavailable")

    user_message = "add a task to buy bread"
    response = run_agent(user_message)

    # Assert that add_task was called with the correct argument
    mock_mcp_client.add_task.assert_called_once_with(description="buy bread")

    # Assert the final response from the agent indicates an error
    assert "An error occurred while adding the task." in response
    # Also check that the tool output was captured in the messages sent to OpenAI
    args, kwargs = mock_openai_client.chat.completions.create.call_args_list[1]
    tool_message_content = json.loads(kwargs['messages'][-1]['content'])
    assert "Error executing tool add_task: Backend service unavailable" in tool_message_content

