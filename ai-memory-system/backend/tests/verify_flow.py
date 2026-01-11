import sys
import os
import asyncio
import shutil
sys.path.append(os.getcwd())
# Also try adding the directory containing 'app' explicitly if getcwd is wrong
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

print(f"DEBUG: sys.path: {sys.path}")

from unittest.mock import MagicMock

# Mock config BEFORE imports to bypass pydantic-settings missing
mock_config = MagicMock()
mock_config.settings.VECTOR_DB_PATH = "data/memory_index_test" 
sys.modules["app.core.config"] = mock_config

from app.services.agent_service import AgentService

# Mock LLM
class MockLLM:
    async def generate(self, prompt, context):
        return f"MOCKED RESPONSE to '{prompt}' with context len {len(context)}"

async def main():
    print("--- STARTING VERIFICATION ---")
    
    # 1. Clean data
    if os.path.exists("data"):
        shutil.rmtree("data")
    os.makedirs("data")

    # 2. Init Agent
    agent = AgentService()
    agent.llm = MockLLM() # Patch LLM
    
    # 3. Add initial memory
    task_id = "task_001"
    print(f"Storing memory for {task_id}")
    agent.memory.store_context(task_id, "User says hello", "Hi there")
    
    # 4. Schedule callback (resumption)
    print("Scheduling resume callback in 1s...")
    agent.scheduler.schedule_callback(task_id, {"context_hint": "check status"}, 1, type="resume")
    
    # 5. Simulate time pass and "Startup" recovery
    print("Waiting 1.5s...")
    await asyncio.sleep(1.5)
    
    print("Simulating Startup Recovery...")
    # Create new agent instance to simulate restart (reloads persistence)
    new_agent = AgentService()
    new_agent.llm = MockLLM()
    
    # Force recovery
    await new_agent.scheduler.recover()
    
    # Give time for callback to execute
    await asyncio.sleep(0.5)
    
    # 6. Check if callback executed. The callback calls 'store_context' with 'Resumed task'.
    print("Verifying memory for resumption record...")
    memories = new_agent.memory.store.search(task_id, "Resumed task")
    found = any("Resumed task" in m["content"] for m in memories)
    
    if found:
        print("SUCCESS: Resumption trace found in memory!")
    else:
        print("FAILURE: Resumption trace NOT found.")
        # Debug
        print("All memories:", [m["content"] for m in new_agent.memory.store.metadata])
        
    # 7. Test Feedback
    print("Testing Feedback Loop...")
    # Retrieve
    context = new_agent.memory.retrieve_context(task_id, "hello")
    if context:
        print(f"Retrieved {len(context)} memories.")
        top_mem = context[0]
        original_score = top_mem.get('score', 0)
        print(f"Top memory score before: {original_score}")
        
        # Apply positive feedback
        print("Applying positive feedback...")
        new_agent.memory.apply_feedback([top_mem["id"]], True)
        
        # Check score again 
        new_score = new_agent.memory.rl.rewards.get(top_mem["id"])
        print(f"Top memory score after: {new_score}")
        
        if new_score > original_score:
             print("SUCCESS: Score increased!")
        else:
             print("FAILURE: Score did not increase.")
    else:
        print("FAILURE: No context retrieved to test feedback.")

if __name__ == "__main__":
    asyncio.run(main())
