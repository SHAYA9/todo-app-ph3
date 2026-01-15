"""MCP Tools Implementation - Function definitions for OpenAI function calling"""
from sqlmodel import Session, select
from src.database.models import Task
from src.database.config import engine
from datetime import datetime
from typing import Optional


# MCP Tool: add_task
async def mcp_add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> dict:
    """
    Create a new task
    
    Args:
        user_id: User identifier
        title: Task title
        description: Optional task description
    
    Returns:
        dict with task_id, status, and title
    """
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }


# MCP Tool: list_tasks
async def mcp_list_tasks(
    user_id: str,
    status: Optional[str] = "all"
) -> list:
    """
    Retrieve tasks from the list
    
    Args:
        user_id: User identifier
        status: Filter by status - "all", "pending", or "completed"
    
    Returns:
        Array of task objects
    """
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        
        tasks = session.exec(query).all()
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ]


# MCP Tool: complete_task
async def mcp_complete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Mark a task as complete
    
    Args:
        user_id: User identifier
        task_id: Task ID to complete
    
    Returns:
        dict with task_id, status, and title
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {
                "task_id": task_id,
                "status": "error",
                "title": None,
                "error": "Task not found"
            }
        
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


# MCP Tool: delete_task
async def mcp_delete_task(
    user_id: str,
    task_id: int
) -> dict:
    """
    Remove a task from the list
    
    Args:
        user_id: User identifier
        task_id: Task ID to delete
    
    Returns:
        dict with task_id, status, and title
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {
                "task_id": task_id,
                "status": "error",
                "title": None,
                "error": "Task not found"
            }
        
        title = task.title
        session.delete(task)
        session.commit()
        
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": title
        }


# MCP Tool: update_task
async def mcp_update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Modify task title or description
    
    Args:
        user_id: User identifier
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
    
    Returns:
        dict with task_id, status, and title
    """
    with Session(engine) as session:
        task = session.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return {
                "task_id": task_id,
                "status": "error",
                "title": None,
                "error": "Task not found"
            }
        
        if title:
            task.title = title
        if description:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        
        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }


# Map tool names to functions
MCP_TOOLS = {
    "add_task": mcp_add_task,
    "list_tasks": mcp_list_tasks,
    "complete_task": mcp_complete_task,
    "delete_task": mcp_delete_task,
    "update_task": mcp_update_task,
}


# OpenAI function calling tool definitions
def get_mcp_tool_definitions():
    """Get OpenAI function calling tool definitions"""
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's identifier"
                        },
                        "title": {
                            "type": "string",
                            "description": "The task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional task description"
                        }
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Retrieve tasks from the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's identifier"
                        },
                        "status": {
                            "type": "string",
                            "description": "Filter by status: 'all', 'pending', or 'completed'",
                            "enum": ["all", "pending", "completed"]
                        }
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's identifier"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to complete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Remove a task from the user's list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's identifier"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to delete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Modify a task's title or description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user's identifier"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The task ID to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]