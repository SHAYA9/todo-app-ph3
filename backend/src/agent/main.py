import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from services.mcp_client import McpClient
from agent.tools.add_task import add_task
from agent.tools.view_tasks import view_tasks
from agent.tools.mark_task_status import mark_task_status
from agent.tools.delete_task import delete_task
from agent.tools.update_task import update_task

# Load environment variables from .env file
load_dotenv()

# Try Gemini API first, then OpenRouter
gemini_key = os.getenv("GEMINI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

client = None
DEFAULT_MODEL = None
AI_ENABLED = False

if gemini_key:
    try:
        # Initialize OpenAI client with Gemini API
        client = OpenAI(
            api_key=gemini_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        DEFAULT_MODEL = "gemini-2.0-flash-exp"
        AI_ENABLED = False
        print("✅ Using Google Gemini API")
    except Exception as e:
        print(f"⚠️ Gemini API failed: {e}")

if not AI_ENABLED and openrouter_key:
    try:
        # Initialize OpenAI client with OpenRouter
        client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
        DEFAULT_MODEL = "arcee-ai/trinity-mini:free"
        AI_ENABLED = True
        print("✅ Using OpenRouter API")
    except Exception as e:
        print(f"⚠️ OpenRouter API failed: {e}")

if not AI_ENABLED:
    print("⚠️ No AI API available. Using rule-based fallback.")

# Initialize MCP Client
mcp_client = McpClient()

# Map tool names to actual functions
available_functions = {
    "add_task": add_task,
    "view_tasks": view_tasks,
    "update_task": update_task,
    "mark_task_status": mark_task_status,
    "delete_task": delete_task,
}

# Define tools for OpenAI function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "The description of the task to add"
                    }
                },
                "required": ["description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_tasks",
            "description": "View all tasks or filter by status (pending/completed)",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter tasks by status: 'pending' or 'completed'. Leave empty to see all tasks.",
                        "enum": ["pending", "completed"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's description. First view tasks to get the task ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update"
                    },
                    "new_description": {
                        "type": "string",
                        "description": "The new description for the task"
                    }
                },
                "required": ["task_id", "new_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_task_status",
            "description": "Mark a task as completed or pending. First view tasks to get the task ID or use the task number shown in the list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to update status"
                    },
                    "status": {
                        "type": "string",
                        "description": "The new status: 'completed' or 'pending'",
                        "enum": ["pending", "completed"]
                    }
                },
                "required": ["task_id", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task from the todo list. First view tasks to get the task ID or use the task number shown in the list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]

# System prompt for the AI assistant
SYSTEM_PROMPT = """You are a helpful AI todo assistant. You help users manage their tasks naturally.

Key behaviors:
- Be conversational and friendly
- When users ask about tasks using numbers (like "delete task 1" or "mark 2 as done"), first call view_tasks to get the list, then extract the task ID from position in the list
- When users say vague things like "show" or "ls"or any other that u think user is asking about to show the tasks, ask them to be more specific or show all tasks
- For natural requests like "reschedule X to Y", update the task description to reflect the new time
- Always confirm actions with positive feedback
- If a task number is mentioned, view tasks first to map the number to the actual task ID
- Be proactive in understanding context and user intent

Remember: Task numbers shown to users are 1-indexed positions in the list, not the actual task IDs."""


def get_task_id_from_number(task_number: int):
    """Helper function to get task ID from task number"""
    result = view_tasks()
    if result.get("success"):
        tasks = result.get("tasks", [])
        if 0 < task_number <= len(tasks):
            return tasks[task_number - 1].get("id")
    return None


def run_agent_ai(user_message: str, conversation_history: list = None):
    """
    AI-powered agent using OpenAI SDK with function calling
    
    Args:
        user_message: The user's message
        conversation_history: Optional list of previous messages for context
    
    Returns:
        Tuple of (response_text, updated_conversation_history)
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add system message if this is the first message
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })
    
    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call OpenAI API with function calling
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=conversation_history,
            tools=tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Check if the model wants to call functions
        if assistant_message.tool_calls:
            # Add assistant's message to history
            conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Calling function: {function_name} with args: {function_args}")
                
                # Special handling for task numbers
                if function_name in ["delete_task", "mark_task_status", "update_task"]:
                    # Check if task_id looks like a number
                    task_id = function_args.get("task_id", "")
                    if task_id.isdigit():
                        # Convert task number to actual ID
                        actual_id = get_task_id_from_number(int(task_id))
                        if actual_id:
                            function_args["task_id"] = actual_id
                        else:
                            function_result = {
                                "success": False,
                                "message": f"Task number {task_id} not found. Please check the task list."
                            }
                            conversation_history.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(function_result)
                            })
                            continue
                
                # Call the function
                function_to_call = available_functions[function_name]
                function_result = function_to_call(**function_args)
                
                # Add function result to conversation
                conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(function_result)
                })
            
            # Get final response from the model after function execution
            second_response = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=conversation_history
            )
            
            final_message = second_response.choices[0].message.content
            conversation_history.append({
                "role": "assistant",
                "content": final_message
            })
            
            return final_message, conversation_history
        
        else:
            # No function calls, just return the response
            response_text = assistant_message.content
            conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return response_text, conversation_history
            
    except Exception as e:
        print(f"❌ Error in run_agent_ai: {e}")
        # Fall back to rule-based system
        raise


def run_agent_rule_based(user_message: str):
    """Enhanced rule-based agent with natural responses (no IDs shown)"""
    user_message_lower = user_message.lower()
    
    try:
        # Add task - flexible parsing
        if any(keyword in user_message_lower for keyword in ["add", "create", "new", "remind"]):
            desc = user_message
            for keyword in ["add a task to", "add task to", "create a task to", "remind me to", 
                           "add a task", "add task", "create task", "new task", "add to", "add", "create", "new"]:
                if keyword in user_message_lower:
                    idx = user_message_lower.index(keyword)
                    desc = user_message[idx + len(keyword):].strip()
                    if desc:
                        break
            
            result = add_task(description=desc)
            if result.get("success"):
                return f"✅ Got it! I've added '{desc}' to your list."
            return f"❌ Hmm, couldn't add that. {result.get('message', 'Try again?')}"
        
        # View tasks - natural responses without IDs
        elif any(keyword in user_message_lower for keyword in ["show", "list", "view", "see", "display", "what", "ls"]):
            status = None
            if "pending" in user_message_lower or "todo" in user_message_lower:
                status = "pending"
            elif "completed" in user_message_lower or "done" in user_message_lower:
                status = "completed"
            
            result = view_tasks(status=status)
            if result.get("success"):
                tasks = result.get("tasks", [])
                
                if not tasks:
                    if status == "pending":
                        return "🎉 Great! No pending tasks."
                    elif status == "completed":
                        return "📝 No completed tasks yet."
                    else:
                        return "📝 Your list is empty. Add something!"
                
                # Smart response based on filter
                if status == "pending":
                    response = f"⏳ You have {len(tasks)} pending task{'s' if len(tasks) > 1 else ''}:\n\n"
                elif status == "completed":
                    response = f"✅ You've completed {len(tasks)} task{'s' if len(tasks) > 1 else ''}:\n\n"
                else:
                    response = f"📋 Here's your list ({len(tasks)} task{'s' if len(tasks) > 1 else ''}):\n\n"
                
                for i, task in enumerate(tasks, 1):
                    icon = "✅" if task.get("status") == "completed" else "⏳"
                    response += f"{i}. {icon} {task.get('description')}\n"
                
                response += "\n💡 Tip: Use task numbers like 'mark 1 as done' or 'delete 2'"
                return response
            return f"❌ Couldn't get tasks. {result.get('message', 'Try again?')}"
        
        # Mark task - natural confirmation
        elif any(keyword in user_message_lower for keyword in ["mark", "complete", "finish", "done"]):
            words = user_message.split()
            task_id = None
            task_num = None
            status = "completed"
            
            for word in words:
                if word.isdigit():
                    task_num = int(word)
                    task_id = get_task_id_from_number(task_num)
                    break
            
            if "pending" in user_message_lower or "undo" in user_message_lower:
                status = "pending"
            
            if task_id:
                result = mark_task_status(task_id=task_id, status=status)
                if result.get("success"):
                    if status == "completed":
                        return f"✅ Awesome! Task {task_num} is done."
                    else:
                        return f"⏳ Task {task_num} marked as pending."
                return f"❌ Couldn't update. {result.get('message', 'Try again?')}"
            return "❌ Which task? Try 'mark 1 as done' or 'complete 2'."
        
        # Delete task - friendly confirmation
        elif any(keyword in user_message_lower for keyword in ["delete", "remove", "clear"]):
            words = user_message.split()
            task_id = None
            task_num = None
            
            for word in words:
                if word.isdigit():
                    task_num = int(word)
                    task_id = get_task_id_from_number(task_num)
                    break
            
            if task_id:
                result = delete_task(task_id=task_id)
                if result.get("success"):
                    return f"🗑️ Done! Removed task {task_num}."
                return f"❌ Couldn't delete. {result.get('message', 'Try again?')}"
            return "❌ Which task? Try 'delete 1' or 'remove 2'."
        
        # Update task
        elif any(keyword in user_message_lower for keyword in ["update", "change", "edit", "reschedule"]):
            words = user_message.split()
            task_id = None
            task_num = None
            
            for word in words:
                if word.isdigit():
                    task_num = int(word)
                    task_id = get_task_id_from_number(task_num)
                    break
            
            if task_id:
                new_desc = None
                for keyword in ["to", "with", "as"]:
                    if keyword in user_message_lower:
                        parts = user_message.lower().split(keyword, 1)
                        if len(parts) > 1:
                            new_desc = parts[1].strip()
                            break
                
                if new_desc:
                    result = update_task(task_id=task_id, new_description=new_desc)
                    if result.get("success"):
                        return f"✅ Updated task {task_num} to: '{new_desc}'"
                    return f"❌ Couldn't update. {result.get('message', 'Try again?')}"
                return f"❌ What to change it to? Try 'update 1 to buy milk'."
            return "❌ Which task? Try 'update 1 to new description'."
        
        # Smart default based on context
        else:
            if any(word in user_message_lower for word in ["hi", "hello", "hey", "help"]):
                return """👋 Welcome! I’m your Smart Todo Assistant
Powered🔥by Xpertsphere

I can help you to stay organized in seconds. Just try commands like:

• “Add buy groceries”
• “Show my tasks”
• “Mark task 1 as done”
• “Delete task 2”

✨ Fast. Simple. Productive.
What would you like to do today?"""
            else:
                return """🤔 Not sure what you mean.

I can help with:
• Adding: "Add buy milk"
• Viewing: "Show tasks"
• Completing: "Mark 1 done"
• Deleting: "Delete 2"
• Updating: "Update 1 to buy eggs"

Try one of these?"""
            
    except Exception as e:
        print(f"Error in run_agent_rule_based: {e}")
        return f"❌ Error: {str(e)}"


def run_agent(user_message: str, conversation_history: list = None):
    """
    Main agent function - tries AI first, falls back to rule-based
    
    Args:
        user_message: The user's message
        conversation_history: Optional list of previous messages for context
    
    Returns:
        Tuple of (response_text, updated_conversation_history)
    """
    if AI_ENABLED:
        try:
            return run_agent_ai(user_message, conversation_history)
        except Exception as e:
            print(f"⚠️ AI agent failed, using rule-based fallback: {e}")
            # Fall back to rule-based
            if conversation_history is None:
                conversation_history = []
            response = run_agent_rule_based(user_message)
            return response, conversation_history
    else:
        # Use rule-based directly
        if conversation_history is None:
            conversation_history = []
        response = run_agent_rule_based(user_message)
        return response, conversation_history


if __name__ == "__main__":
    if AI_ENABLED:
        print("🤖 AI Todo Assistant initialized!")
        print("💡 Try natural commands like:")
        print("   - 'Add buy milk and eggs'")
        print("   - 'Show my tasks'")
        print("   - 'Mark task 1 as done'")
        print("   - 'Reschedule my meeting to 3 PM'")
    else:
        print("🤖 Todo Assistant initialized (Rule-based mode)")
        print("💡 Try commands like:")
        print("   - 'Add buy milk'")
        print("   - 'Show tasks'")
        print("   - 'Mark task 1 as done'")
    
    print("   - 'Delete task 1'\n")
    
    conversation = []
    
    while True:
        user_input = input("\n🧑 You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            break
        
        response, conversation = run_agent(user_input, conversation)
        print(f"\n🤖 Assistant: {response}")