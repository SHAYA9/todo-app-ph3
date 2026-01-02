from services.mcp_client import McpClient


def add_task(description: str):
    """
    Adds a new task to the user's todo list.
    Args:
        description (str): The description of the task to add.
    Returns:
        dict: The response from the MCP client after adding the task.
    """
    mcp_client = McpClient()
    response = mcp_client.add_task(description)
    return response
