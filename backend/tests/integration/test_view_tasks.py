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

def test_view_tasks_flow_success(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for viewing tasks when the agent successfully
    calls the view_tasks tool and the backend returns tasks.
    """
    mock_tasks = [
        {"id": "1", "description": "buy milk", "status": "pending"},
        {"id": "2", "description": "walk dog", "status": "completed"}
    ]

    # Mock the OpenAI response to indicate a tool call for 'view_tasks'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="view_tasks",
                                    arguments='{}' # No status filter
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
                    message=MagicMock(content=json.dumps(mock_tasks))
                )
            ]
        )
    ]

    # Mock the McpClient's view_tasks method to return a list of tasks
    mock_mcp_client.view_tasks.return_value = mock_tasks

    user_message = "show my tasks"
    response = run_agent(user_message)

    # Assert that view_tasks was called with the correct argument
    mock_mcp_client.view_tasks.assert_called_once_with(status=None)

    # Assert the final response from the agent contains the tasks
    assert json.dumps(mock_tasks) in response
    assert mock_tasks[0]['description'] in response
    assert mock_tasks[1]['description'] in response

def test_view_tasks_flow_no_tasks(mock_openai_client, mock_mcp_client):
    """
    Test the end-to-end flow for viewing tasks when no tasks are returned.
    """
    mock_tasks = []

    # Mock the OpenAI response to indicate a tool call for 'view_tasks'
    mock_openai_client.chat.completions.create.side_effect = [
        MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        tool_calls=[
                            MagicMock(
                                function=MagicMock(
                                    name="view_tasks",
                                    arguments='{"status": "pending"}'
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
                    message=MagicMock(content=json.dumps(mock_tasks))
                )
            ]
        )
    ]

    # Mock the McpClient's view_tasks method to return an empty list
    mock_mcp_client.view_tasks.return_value = mock_tasks

    user_message = "show my pending tasks"
    response = run_agent(user_message)

    # Assert that view_tasks was called with the correct argument
    mock_mcp_client.view_tasks.assert_called_once_with(status="pending")

    # Assert the final response from the agent indicates no tasks
    assert json.dumps(mock_tasks) in response # The agent returns an empty JSON array
