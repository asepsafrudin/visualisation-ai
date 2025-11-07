"""
Execution Module
File: core/execution.py
"""

from typing import Dict, Any
from datetime import datetime
from core.planning import Plan, Step
from tools.manager import ToolManager


class Executor:
    """Modul untuk mengeksekusi plan"""
    
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
        self.execution_history = []
    
    def execute_plan(self, plan: Plan) -> Dict[str, Any]:
        """Execute plan step by step"""
        print(f"⚙️  [Executor] Starting plan execution...")
        
        plan.status = "executing"
        results = []
        
        while True:
            # Get next executable steps
            next_steps = plan.get_next_steps()
            
            if not next_steps:
                # Check if all steps are completed
                all_completed = all(step.status == "completed" for step in plan.steps)
                if all_completed:
                    plan.status = "completed"
                    break
                else:
                    # Some steps failed or blocked
                    plan.status = "failed"
                    break
            
            # Execute each ready step
            for step in next_steps:
                result = self._execute_step(step, plan)
                results.append(result)
        
        execution_result = {
            "plan_status": plan.status,
            "steps_executed": len([s for s in plan.steps if s.status == "completed"]),
            "steps_failed": len([s for s in plan.steps if s.status == "failed"]),
            "results": results
        }
        
        self.execution_history.append({
            "plan": plan.to_dict(),
            "result": execution_result,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"   Execution completed: {plan.status}")
        return execution_result
    
    def _execute_step(self, step: Step, plan: Plan) -> Dict[str, Any]:
        """Execute single step"""
        print(f"   Executing Step {step.step_id}: {step.description}")
        
        step.status = "in_progress"
        step.started_at = datetime.now().isoformat()
        
        try:
            if step.tool:
                # Execute using tool
                # This is simplified - in real implementation, 
                # you'd parse parameters from step description
                result = self.tool_manager.execute(step.tool)
                step.result = result
                
                if result.get("success"):
                    step.status = "completed"
                else:
                    step.status = "failed"
                    step.error = result.get("error")
            else:
                # No tool needed, mark as completed
                step.status = "completed"
                step.result = {"message": "Step completed without tool execution"}
            
            step.completed_at = datetime.now().isoformat()
            
            return {
                "step_id": step.step_id,
                "status": step.status,
                "result": step.result
            }
        
        except Exception as e:
            step.status = "failed"
            step.error = str(e)
            step.completed_at = datetime.now().isoformat()
            
            return {
                "step_id": step.step_id,
                "status": "failed",
                "error": str(e)
            }
    
    def get_history(self) -> list:
        """Get execution history"""
        return self.execution_history
