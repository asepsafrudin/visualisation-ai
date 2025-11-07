"""
Main Agent Implementation
File: core/agent.py
"""

from typing import Dict, Any
from core.task_understanding import TaskUnderstanding
from core.planning import Planner
from core.execution import Executor
from core.learning import LearningModule
from tools.manager import ToolManager
from config.settings import settings


class AgenticSystem:
    """Main Agentic System orchestrator"""
    
    def __init__(self, llm_client=None):
        print("🤖 Initializing Agentic System...")
        
        # Initialize modules
        self.tool_manager = ToolManager()
        self.task_understanding = TaskUnderstanding(llm_client)
        self.planner = Planner()
        self.executor = Executor(self.tool_manager)
        self.learning = LearningModule()
        
        # Load previous learning data
        self.learning.load_from_disk()
        
        print("✓ Agentic System initialized successfully")
    
    def register_tool(self, tool):
        """Register a tool to the system"""
        self.tool_manager.register(tool)
    
    def process_task(self, task: str) -> Dict[str, Any]:
        """Process a task end-to-end"""
        print(f"\n{'='*60}")
        print(f"🎯 Processing Task: {task}")
        print(f"{'='*60}\n")
        
        # Step 1: Understand the task
        analysis = self.task_understanding.analyze(task)
        
        # Step 2: Create execution plan
        plan = self.planner.create_plan(task, analysis)
        
        # Step 3: Execute the plan
        result = self.executor.execute_plan(plan)
        
        # Step 4: Learn from execution
        self.learning.record_execution(plan.to_dict(), result)
        
        # Return comprehensive result
        return {
            "task": task,
            "analysis": analysis,
            "plan": plan.to_dict(),
            "execution_result": result,
            "status": result.get("plan_status")
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "tools": self.tool_manager.get_statistics(),
            "learning": self.learning.get_insights()
        }
    
    def list_tools(self) -> Dict[str, Any]:
        """List all available tools"""
        return {
            "tools": self.tool_manager.list_tools(),
            "categories": self.tool_manager.get_categories()
        }
