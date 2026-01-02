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
    with patch("backend.src.agent.main.mcp_client") as mock_client:
        yield mock_client

def test_mark_task_status_flow_success(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for marking a task's status when the agent successfully
    calls the mark_task_status tool and the backend confirms.
    """
    # Mock the OpenAI response to indicate a tool call for 'mark_task_status'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="mark_task_status",
                                    arguments='{"task_id": "1", "status": "completed"}'
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
                    message=MagicMock(content="Task '1' marked as completed successfully.")
                )
            ]
        )
    ]

    # Mock the McpClient's mark_task_status method to return a success response
    mock_mcp_client.mark_task_status.return_value = {"id": "1", "description": "buy milk", "status": "completed"}

    user_message = "mark task 1 as completed"
    response = run_agent(user_message)

    # Assert that mark_task_status was called with the correct arguments
    mock_mcp_client.mark_task_status.assert_called_once_with(task_id="1", status="completed")

    # Assert the final response from the agent
    assert "Task '1' marked as completed successfully." in response

def test_mark_task_status_flow_failure(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for marking a task's status when the backend call fails.
    """
    # Mock the OpenAI response to indicate a tool call for 'mark_task_status'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="mark_task_status",
                                    arguments='{"task_id": "99", "status": "pending"}'
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
                    message=MagicMock(content="An error occurred while updating the task status.")
                )
            ]
        )
    ]

    # Mock the McpClient's mark_task_status method to raise an exception
    mock_mcp_client.mark_task_status.side_effect = Exception("Task not found")

    user_message = "mark task 99 as pending"
    response = run_agent(user_message)

    # Assert that mark_task_status was called with the correct arguments
    mock_mcp_client.mark_task_status.assert_called_once_with(task_id="99", status="pending")

    # Assert the final response from the agent indicates an error
    assert "An error occurred while updating the task status." in response
    # Also check that the tool output was captured in the messages sent to OpenAI
    args, kwargs = mock_openai_client.chat.completions.create.call_args_list[1]
    tool_message_content = json.loads(kwargs['messages'][-1]['content'])
    assert "Error executing tool mark_task_status: Task not found" in tool_message_content
