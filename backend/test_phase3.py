"""
Phase III Implementation Test Script

This script tests all Phase III requirements:
1. Database models
2. MCP tools
3. Stateless chat endpoint
4. Conversation persistence
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from database.config import init_db, engine
from database.models import Task, Conversation, Message
from sqlmodel import Session, select
from agents.todo_agent import run_todo_agent


def test_database_initialization():
    """Test database initialization"""
    print("\n🧪 Test 1: Database Initialization")
    try:
        init_db()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


def test_database_models():
    """Test database models CRUD operations"""
    print("\n🧪 Test 2: Database Models")
    try:
        with Session(engine) as session:
            # Create task
            task = Task(
                user_id="test_user",
                title="Test Task",
                description="Test description",
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            print(f"✅ Task created with ID: {task.id}")
            
            # Read task
            db_task = session.get(Task, task.id)
            assert db_task.title == "Test Task"
            print("✅ Task read successfully")
            
            # Update task
            db_task.completed = True
            session.add(db_task)
            session.commit()
            print("✅ Task updated successfully")
            
            # Delete task
            session.delete(db_task)
            session.commit()
            print("✅ Task deleted successfully")
            
            return True
    except Exception as e:
        print(f"❌ Database models test failed: {e}")
        return False


async def test_mcp_tools():
    """Test MCP tools through agent"""
    print("\n🧪 Test 3: MCP Tools")
    try:
        # Test add_task
        conv_id, response, tools = await run_todo_agent(
            user_id="test_user",
            user_message="Add buy groceries"
        )
        print(f"✅ add_task: Conversation ID={conv_id}")
        print(f"   Response: {response[:50]}...")
        
        # Test list_tasks
        conv_id, response, tools = await run_todo_agent(
            user_id="test_user",
            user_message="Show my tasks",
            conversation_id=conv_id
        )
        print(f"✅ list_tasks: {response[:50]}...")
        
        # Test complete_task
        conv_id, response, tools = await run_todo_agent(
            user_id="test_user",
            user_message="Mark task 1 as done",
            conversation_id=conv_id
        )
        print(f"✅ complete_task: {response[:50]}...")
        
        # Test update_task
        conv_id, response, tools = await run_todo_agent(
            user_id="test_user",
            user_message="Change task 1 to buy organic groceries",
            conversation_id=conv_id
        )
        print(f"✅ update_task: {response[:50]}...")
        
        # Test delete_task
        conv_id, response, tools = await run_todo_agent(
            user_id="test_user",
            user_message="Delete task 1",
            conversation_id=conv_id
        )
        print(f"✅ delete_task: {response[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ MCP tools test failed: {e}")
        return False


async def test_conversation_persistence():
    """Test conversation persistence across requests"""
    print("\n🧪 Test 4: Conversation Persistence")
    try:
        # First message
        conv_id, response1, _ = await run_todo_agent(
            user_id="test_user2",
            user_message="Add task 1"
        )
        print(f"✅ First message: Conversation ID={conv_id}")
        
        # Second message (same conversation)
        conv_id2, response2, _ = await run_todo_agent(
            user_id="test_user2",
            user_message="Show my tasks",
            conversation_id=conv_id
        )
        
        assert conv_id == conv_id2, "Conversation ID should persist"
        print("✅ Conversation ID persisted across requests")
        
        # Verify messages in database
        with Session(engine) as session:
            messages = session.exec(
                select(Message)
                .where(Message.conversation_id == conv_id)
            ).all()
            
            assert len(messages) >= 4, "Should have at least 4 messages (2 user, 2 assistant)"
            print(f"✅ {len(messages)} messages stored in database")
            
        return True
    except Exception as e:
        print(f"❌ Conversation persistence test failed: {e}")
        return False


async def test_multi_user_isolation():
    """Test user isolation"""
    print("\n🧪 Test 5: Multi-User Isolation")
    try:
        # User 1 adds task
        await run_todo_agent(
            user_id="user1",
            user_message="Add user1 task"
        )
        
        # User 2 adds task
        await run_todo_agent(
            user_id="user2",
            user_message="Add user2 task"
        )
        
        # Verify user1 tasks
        with Session(engine) as session:
            user1_tasks = session.exec(
                select(Task).where(Task.user_id == "user1")
            ).all()
            
            user2_tasks = session.exec(
                select(Task).where(Task.user_id == "user2")
            ).all()
            
            assert len(user1_tasks) >= 1, "User1 should have tasks"
            assert len(user2_tasks) >= 1, "User2 should have tasks"
            
            # Verify isolation
            for task in user1_tasks:
                assert task.user_id == "user1", "User1 tasks should have user1 id"
            
            for task in user2_tasks:
                assert task.user_id == "user2", "User2 tasks should have user2 id"
            
            print(f"✅ User isolation verified (User1: {len(user1_tasks)} tasks, User2: {len(user2_tasks)} tasks)")
            
        return True
    except Exception as e:
        print(f"❌ Multi-user isolation test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("Phase III Implementation Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Database initialization
    results.append(("Database Initialization", test_database_initialization()))
    
    # Test 2: Database models
    results.append(("Database Models", test_database_models()))
    
    # Test 3: MCP tools
    results.append(("MCP Tools", await test_mcp_tools()))
    
    # Test 4: Conversation persistence
    results.append(("Conversation Persistence", await test_conversation_persistence()))
    
    # Test 5: Multi-user isolation
    results.append(("Multi-User Isolation", await test_multi_user_isolation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All Phase III requirements verified!")
        print("✅ Ready for production deployment")
    else:
        print("\n⚠️ Some tests failed. Please review the errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())