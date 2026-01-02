import json
import os
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
import uuid


class TaskStorage:
    """Simple JSON-based task storage system"""
    
    def __init__(self, storage_file: str = "tasks.json"):
        # Store tasks.json in backend directory
        self.storage_path = Path(__file__).parent.parent.parent / storage_file
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Ensure the storage file exists"""
        if not self.storage_path.exists():
            self._save_tasks([])
    
    def _load_tasks(self) -> List[Dict]:
        """Load tasks from storage"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_tasks(self, tasks: List[Dict]):
        """Save tasks to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump(tasks, f, indent=2)
    
    def add_task(self, description: str) -> Dict:
        """Add a new task"""
        tasks = self._load_tasks()
        task = {
            "id": str(uuid.uuid4()),
            "description": description,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        tasks.append(task)
        self._save_tasks(tasks)
        return {"success": True, "task": task, "message": "Task added successfully"}
    
    def view_tasks(self, status: Optional[str] = None) -> Dict:
        """View all tasks or filter by status"""
        tasks = self._load_tasks()
        if status:
            tasks = [t for t in tasks if t.get("status") == status]
        return {"success": True, "tasks": tasks, "count": len(tasks)}
    
    def update_task(self, task_id: str, new_description: str) -> Dict:
        """Update a task's description"""
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                return {"success": True, "task": task, "message": "Task updated successfully"}
        return {"success": False, "message": f"Task with ID {task_id} not found"}
    
    def mark_task_status(self, task_id: str, status: str) -> Dict:
        """Mark a task as completed or pending"""
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                return {"success": True, "task": task, "message": f"Task marked as {status}"}
        return {"success": False, "message": f"Task with ID {task_id} not found"}
    
    def delete_task(self, task_id: str) -> Dict:
        """Delete a task"""
        tasks = self._load_tasks()
        initial_count = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]
        
        if len(tasks) < initial_count:
            self._save_tasks(tasks)
            return {"success": True, "message": "Task deleted successfully"}
        return {"success": False, "message": f"Task with ID {task_id} not found"}