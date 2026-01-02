import pytest
from unittest.mock import patch, MagicMock
from backend.src.agent.main import run_agent
import json

@pytest.fixture
def mock_openai_client():
    with patch("backend.src.agent.main.client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_mcp_client():
    with patch("backend.src.services.mcp_client.McpClient") as mock_mcp_client_class:
        mock_instance = mock_mcp_client_class.return_value
        yield mock_instance

def test_update_task_flow_success(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for updating a task when the agent successfully
    calls the update_task tool and the backend confirms.
    """
    # Mock the OpenAI response to indicate a tool call for 'update_task'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="update_task",
                                    arguments='{"task_id": "1", "new_description": "buy organic milk"}'
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
                    message=MagicMock(content="Task '1' updated to 'buy organic milk' successfully.")
                )
            ]
        )
    ]

    # Mock the McpClient's update_task method to return a success response
    mock_mcp_client.update_task.return_value = {"id": "1", "description": "buy organic milk", "status": "pending"}

    user_message = "change task 1 to buy organic milk"
    response = run_agent(user_message)

    # Assert that update_task was called with the correct arguments
    mock_mcp_client.update_task.assert_called_once_with(task_id="1", new_description="buy organic milk")

    # Assert the final response from the agent
    assert "Task '1' updated to 'buy organic milk' successfully." in response

def test_update_task_flow_failure(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for updating a task when the backend call fails.
    """
    # Mock the OpenAI response to indicate a tool call for 'update_task'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="update_task",
                                    arguments='{"task_id": "99", "new_description": "non-existent task"}'
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
                    message=MagicMock(content="An error occurred while updating the task.")
                )
            ]
        )
    ]

    # Mock the McpClient's update_task method to raise an exception
    mock_mcp_client.update_task.side_effect = Exception("Task not found")

    user_message = "update task 99 to non-existent task"
    response = run_agent(user_message)

    # Assert that update_task was called with the correct arguments
    mock_mcp_client.update_task.assert_called_once_with(task_id="99", new_description="non-existent task")

    # Assert the final response from the agent indicates an error
    assert "An error occurred while updating the task." in response
    # Also check that the tool output was captured in the messages sent to OpenAI
    args, kwargs = mock_openai_client.chat.completions.create.call_args_list[1]
    tool_message_content = json.loads(kwargs['messages'][-1]['content'])
    assert "Error executing tool update_task: Task not found" in tool_message_content
