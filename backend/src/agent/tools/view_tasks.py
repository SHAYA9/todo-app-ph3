from services.mcp_client import McpClient


def view_tasks(status: str = None):
    """
    Views all tasks in the user's todo list, with an optional status filter.
    Args:
        status (str, optional): The status to filter tasks by. Can be "pending" or "completed".
                                Defaults to None, showing all tasks.
    Returns:
        dict: The response from the MCP client with the list of tasks.
    """
    mcp_client = McpClient()
    response = mcp_client.view_tasks(status)
    return response
