from services.mcp_client import McpClient


def mark_task_status(task_id: str, status: str):
    """
    Marks a task as complete or pending.
    Args:
        task_id (str): The ID of the task to update.
        status (str): The new status for the task. Must be "pending" or "completed".
    Returns:
        dict: The response from the MCP client after updating the task status.
    """
    mcp_client = McpClient()
    response = mcp_client.mark_task_status(task_id, status)
    return response
