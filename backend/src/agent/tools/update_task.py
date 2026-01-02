from services.mcp_client import McpClient


def update_task(task_id: str, new_description: str):
    """
    Updates the description of an existing task.
    Args:
        task_id (str): The ID of the task to update.
        new_description (str): The new description for the task.
    Returns:
        dict: The response from the MCP client after updating the task.
    """
    mcp_client = McpClient()
    response = mcp_client.update_task(task_id, new_description)
    return response
