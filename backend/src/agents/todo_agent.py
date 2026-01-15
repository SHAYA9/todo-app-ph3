"""Todo AI Agent using OpenAI Function Calling (simulating Agents SDK behavior)"""
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from src.mcp_server.tools import get_mcp_tool_definitions, MCP_TOOLS
from sqlmodel import Session, select
from src.database.models import Conversation, Message, Task
from src.database.config import engine
from datetime import datetime
from typing import Optional, List, Dict, Tuple

load_dotenv()

# Initialize OpenAI client with fallback
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

client = None
AGENT_MODEL = None
USE_AI = False

if openai_key:
    try:
        client = OpenAI(api_key=openai_key)
        AGENT_MODEL = "gpt-4o-mini"
        USE_AI = True
        print("✅ Using OpenAI API")
    except Exception as e:
        print(f"⚠️ OpenAI failed: {e}")

if not USE_AI and openrouter_key:
    try:
        client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
        # Try multiple models in order of preference
        AGENT_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
        USE_AI = True
        print("✅ Using OpenRouter API")
    except Exception as e:
        print(f"⚠️ OpenRouter failed: {e}")

if not USE_AI:
    print("⚠️ No AI API available. Using rule-based fallback mode.")

# Agent configuration
AGENT_INSTRUCTIONS = """You are a helpful AI todo assistant. You help users manage their tasks naturally.

Key behaviors:
- Be conversational and friendly
- When users mention adding/creating/remembering something, use add_task
- When users ask to see/show/list tasks, use list_tasks with appropriate filter
- When users say done/complete/finished, use complete_task
- When users say delete/remove/cancel, use delete_task
- When users say change/update/rename, use update_task
- Always confirm actions with friendly responses
- Handle errors gracefully
- Be proactive in understanding context and user intent"""


def get_or_create_conversation(session: Session, user_id: str, conversation_id: Optional[int] = None) -> Conversation:
    """Get existing conversation or create new one"""
    if conversation_id:
        conversation = session.get(Conversation, conversation_id)
        if conversation and conversation.user_id == user_id:
            return conversation
    
    # Create new conversation
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


def get_conversation_history(session: Session, conversation_id: int) -> List[Dict]:
    """Get conversation messages as list of dicts"""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()
    
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def save_message(session: Session, user_id: str, conversation_id: int, role: str, content: str):
    """Save a message to database"""
    message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()


async def run_rule_based_agent(user_id: str, user_message: str) -> Tuple[str, List[Dict]]:
    """Rule-based agent fallback when AI is unavailable"""
    user_message_lower = user_message.lower()
    tool_calls_made = []
    
    with Session(engine) as session:
        # Add task
        if any(keyword in user_message_lower for keyword in ["add", "create", "new", "remind"]):
            # Extract task title
            title = user_message
            for keyword in ["add a task to", "add task to", "create a task to", "remind me to", 
                           "add a task", "add task", "create task", "new task", "add to", "add", "create", "new"]:
                if keyword in user_message_lower:
                    idx = user_message_lower.index(keyword)
                    title = user_message[idx + len(keyword):].strip()
                    if title:
                        break
            
            result = await MCP_TOOLS["add_task"](user_id=user_id, title=title)
            tool_calls_made.append({"name": "add_task", "arguments": json.dumps({"user_id": user_id, "title": title})})
            
            if result.get("status") == "created":
                return f"✅ Got it! I've added '{title}' to your tasks.", tool_calls_made
            return f"❌ Couldn't add that task.", tool_calls_made
        
        # List tasks
        elif any(keyword in user_message_lower for keyword in ["show", "list", "view", "see", "display", "what", "ls"]):
            status = "all"
            if "pending" in user_message_lower or "todo" in user_message_lower:
                status = "pending"
            elif "completed" in user_message_lower or "done" in user_message_lower:
                status = "completed"
            
            result = await MCP_TOOLS["list_tasks"](user_id=user_id, status=status)
            tool_calls_made.append({"name": "list_tasks", "arguments": json.dumps({"user_id": user_id, "status": status})})
            
            tasks = result if isinstance(result, list) else []
            
            if not tasks:
                if status == "pending":
                    return "🎉 Great! No pending tasks.", tool_calls_made
                elif status == "completed":
                    return "📝 No completed tasks yet.", tool_calls_made
                else:
                    return "📝 Your task list is empty. Add something!", tool_calls_made
            
            response = f"📋 Here are your {status} tasks:\n\n"
            for i, task in enumerate(tasks, 1):
                icon = "✅" if task.get("completed") else "⏳"
                response += f"{i}. {icon} {task.get('title')}\n"
            
            response += "\n💡 Try: 'mark 1 as done' or 'delete 2'"
            return response, tool_calls_made
        
        # Complete task
        elif any(keyword in user_message_lower for keyword in ["mark", "complete", "finish", "done"]):
            words = user_message.split()
            task_id = None
            
            for word in words:
                if word.isdigit():
                    # Get task by number
                    task_num = int(word)
                    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
                    if 0 < task_num <= len(tasks):
                        task_id = tasks[task_num - 1].id
                    break
            
            if task_id:
                result = await MCP_TOOLS["complete_task"](user_id=user_id, task_id=task_id)
                tool_calls_made.append({"name": "complete_task", "arguments": json.dumps({"user_id": user_id, "task_id": task_id})})
                
                if result.get("status") == "completed":
                    return f"✅ Awesome! Task completed: {result.get('title')}", tool_calls_made
                return "❌ Couldn't complete that task.", tool_calls_made
            return "❌ Which task? Try 'mark 1 as done'.", tool_calls_made
        
        # Delete task
        elif any(keyword in user_message_lower for keyword in ["delete", "remove", "clear"]):
            words = user_message.split()
            task_id = None
            
            for word in words:
                if word.isdigit():
                    task_num = int(word)
                    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
                    if 0 < task_num <= len(tasks):
                        task_id = tasks[task_num - 1].id
                    break
            
            if task_id:
                result = await MCP_TOOLS["delete_task"](user_id=user_id, task_id=task_id)
                tool_calls_made.append({"name": "delete_task", "arguments": json.dumps({"user_id": user_id, "task_id": task_id})})
                
                if result.get("status") == "deleted":
                    return f"🗑️ Done! Removed task: {result.get('title')}", tool_calls_made
                return "❌ Couldn't delete that task.", tool_calls_made
            return "❌ Which task? Try 'delete 1'.", tool_calls_made
        
        # Default response
        else:
            if any(word in user_message_lower for word in ["hi", "hello", "hey", "help"]):
                return """👋 Welcome! I'm your AI Todo Assistant

I can help you:
• Add tasks: "Add buy groceries"
• View tasks: "Show my tasks"
• Complete: "Mark 1 as done"
• Delete: "Delete task 2"

What would you like to do?""", tool_calls_made
            else:
                return """🤔 I can help with:
• Adding: "Add buy milk"
• Viewing: "Show tasks"  
• Completing: "Mark 1 done"
• Deleting: "Delete 2"

Try one of these?""", tool_calls_made


async def run_ai_agent(
    user_id: str,
    user_message: str,
    conversation_id: int,
    session: Session
) -> Tuple[str, List[Dict]]:
    """AI-powered agent using OpenAI function calling"""
    # Get conversation history
    history = get_conversation_history(session, conversation_id)
    
    # Build messages array with system instruction
    messages = [
        {"role": "system", "content": AGENT_INSTRUCTIONS}
    ] + history + [
        {"role": "user", "content": user_message}
    ]
    
    # Get MCP tool definitions
    tools = get_mcp_tool_definitions()
    
    # Track tool calls
    tool_calls_made = []
    
    # Call OpenAI with function calling
    response = client.chat.completions.create(
        model=AGENT_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    
    # Check if tools were called
    if assistant_message.tool_calls:
        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Ensure user_id is in arguments
            function_args["user_id"] = user_id
            
            # Track tool call
            tool_calls_made.append({
                "name": function_name,
                "arguments": json.dumps(function_args)
            })
            
            # Call the MCP tool
            tool_function = MCP_TOOLS[function_name]
            tool_result = await tool_function(**function_args)
            
            # Add tool result to messages
            messages.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [{"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}} for tc in assistant_message.tool_calls]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })
        
        # Get final response after tool execution
        second_response = client.chat.completions.create(
            model=AGENT_MODEL,
            messages=messages
        )
        
        final_response = second_response.choices[0].message.content
    else:
        # No tools called
        final_response = assistant_message.content
    
    return final_response, tool_calls_made


async def run_todo_agent(
    user_id: str,
    user_message: str,
    conversation_id: Optional[int] = None
) -> Tuple[int, str, List[Dict]]:
    """
    Run the todo agent (AI or rule-based fallback)
    
    Args:
        user_id: User identifier
        user_message: User's message
        conversation_id: Optional conversation ID
    
    Returns:
        Tuple of (conversation_id, response, tool_calls)
    """
    with Session(engine) as session:
        # Get or create conversation
        conversation = get_or_create_conversation(session, user_id, conversation_id)
        
        # Save user message
        save_message(session, user_id, conversation.id, "user", user_message)
        
        try:
            if USE_AI:
                # Try AI agent
                final_response, tool_calls_made = await run_ai_agent(
                    user_id, user_message, conversation.id, session
                )
            else:
                # Use rule-based agent
                final_response, tool_calls_made = await run_rule_based_agent(user_id, user_message)
        except Exception as e:
            print(f"⚠️ AI agent failed, using rule-based fallback: {e}")
            # Fallback to rule-based
            final_response, tool_calls_made = await run_rule_based_agent(user_id, user_message)
        
        # Save assistant response
        save_message(session, user_id, conversation.id, "assistant", final_response)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()
        
        return conversation.id, final_response, tool_calls_made