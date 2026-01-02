import os
from dotenv import load_dotenv
from services.task_storage import TaskStorage

load_dotenv()


class McpClient:
    """
    MCP Client that uses local task storage instead of HTTP requests.
    This eliminates the need for an external MCP server.
    """
    
    def __init__(self):
        # Use local task storage instead of HTTP requests
        self.storage = TaskStorage()
    
    def add_task(self, description: str):
        """Add a new task"""
        return self.storage.add_task(description)

    def view_tasks(self, status: str = None):
        """View tasks with optional status filter"""
        return self.storage.view_tasks(status)

    def update_task(self, task_id: str, new_description: str):
        """Update a task's description"""
        return self.storage.update_task(task_id, new_description)

    def mark_task_status(self, task_id: str, status: str):
        """Mark a task status"""
        return self.storage.mark_task_status(task_id, status)

    def delete_task(self, task_id: str):
        """Delete a task"""
        return self.storage.delete_task(task_id)