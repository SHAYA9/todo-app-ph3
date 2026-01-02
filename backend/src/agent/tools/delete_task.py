from services.mcp_client import McpClient


def delete_task(task_id: str):
    """
    Deletes a task from the user's todo list.
    Args:
        task_id (str): The ID of the task to delete.
    Returns:
        dict: The response from the MCP client after deleting the task.
    """
    mcp_client = McpClient()
    response = mcp_client.delete_task(task_id)
    return response
