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

def test_delete_task_flow_with_confirmation(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for deleting a task, including the confirmation step.
    """
    # Simulate the LLM asking for confirmation first
    mock_openai_client.chat.completions.create.side_effect = [
        # First call: User asks to delete, LLM responds by asking for confirmation
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="Are you sure you want to delete task 'buy milk'?")
                )
            ]
        ),
        # Second call: User confirms, LLM now suggests the delete_task tool
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="delete_task",
                                    arguments='{"task_id": "1"}'
                                ),
                                id="call_123"
                            )
                        ]
                    )
                )
            ]
        ),
        # Third call: LLM receives tool output, responds with final confirmation
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="Task 'buy milk' (ID: 1) has been deleted.")
                )
            ]
        )
    ]

    # Mock the McpClient's delete_task method
    mock_mcp_client.delete_task.return_value = {"message": "Task deleted successfully"}

    # Simulate user initiating the delete request
    initial_user_message = "delete task 1: buy milk"
    response_from_agent = run_agent(initial_user_message)

    # Agent should ask for confirmation
    assert "Are you sure you want to delete task 'buy milk'?" in response_from_agent
    
    # Simulate user confirming the action
    confirmation_message = "yes"
    final_response_from_agent = run_agent(confirmation_message)

    # Assert that delete_task was called with the correct argument
    mock_mcp_client.delete_task.assert_called_once_with(task_id="1")

    # Assert the final response from the agent
    assert "Task 'buy milk' (ID: 1) has been deleted." in final_response_from_agent

def test_delete_task_flow_with_denial(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for deleting a task, including the denial step.
    """
    # Simulate the LLM asking for confirmation first
    mock_openai_client.chat.completions.create.side_effect = [
        # First call: User asks to delete, LLM responds by asking for confirmation
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="Are you sure you want to delete task 'pay bills'?")
                )
            ]
        ),
        # Second call: User denies, LLM responds that it won't delete
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content="OK, I won't delete task 'pay bills'.")
                )
            ]
        )
    ]

    # Simulate user initiating the delete request
    initial_user_message = "delete task 2: pay bills"
    response_from_agent = run_agent(initial_user_message)

    # Agent should ask for confirmation
    assert "Are you sure you want to delete task 'pay bills'?" in response_from_agent
    
    # Simulate user denying the action
    denial_message = "no"
    final_response_from_agent = run_agent(denial_message)

    # Assert that delete_task was NOT called
    mock_mcp_client.delete_task.assert_not_called()

    # Assert the final response from the agent
    assert "OK, I won't delete task 'pay bills'." in final_response_from_agent