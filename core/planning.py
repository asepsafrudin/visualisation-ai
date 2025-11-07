"""
Planning Module
File: core/planning.py
"""

from typing import List, Dict, Any
from datetime import datetime


class Step:
    """Representasi satu langkah dalam plan"""
    
    def __init__(self, step_id: int, description: str, tool: str = None, 
                 dependencies: List[int] = None):
        self.step_id = step_id
        self.description = description
        self.tool = tool
        self.dependencies = dependencies or []
        self.status = "pending"  # pending, in_progress, completed, failed
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        return {
            "step_id": self.step_id,
            "description": self.description,
            "tool": self.tool,
            "dependencies": self.dependencies,
            "status": self.status
        }


class Plan:
    """Representasi plan lengkap"""
    
    def __init__(self, task: str):
        self.task = task
        self.steps: List[Step] = []
        self.created_at = datetime.now().isoformat()
        self.status = "created"
    
    def add_step(self, step: Step):
        self.steps.append(step)
    
    def get_step(self, step_id: int) -> Step:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        return None
    
    def get_next_steps(self) -> List[Step]:
        """Dapatkan steps yang siap dieksekusi (dependencies terpenuhi)"""
        ready_steps = []
        
        for step in self.steps:
            if step.status != "pending":
                continue
            
            # Check if all dependencies are completed
            dependencies_met = all(
                self.get_step(dep_id).status == "completed"
                for dep_id in step.dependencies
            )
            
            if dependencies_met:
                ready_steps.append(step)
        
        return ready_steps
    
    def to_dict(self) -> Dict:
        return {
            "task": self.task,
            "created_at": self.created_at,
            "status": self.status,
            "steps": [step.to_dict() for step in self.steps]
        }


class Planner:
    """Modul untuk membuat execution plan"""
    
    def __init__(self):
        self.plans: List[Plan] = []
    
    def create_plan(self, task: str, analysis: Dict[str, Any]) -> Plan:
        """Buat plan berdasarkan task analysis"""
        print(f"📋 [Planner] Creating execution plan...")
        
        plan = Plan(task)
        
        # Simple rule-based planning
        complexity = analysis.get("complexity", "simple")
        required_tools = analysis.get("requires_tools", [])
        
        if complexity == "simple":
            # Single step plan
            tool = required_tools[0] if required_tools else None
            plan.add_step(Step(1, task, tool=tool))
        
        elif complexity == "moderate":
            # Multi-step plan
            for i, tool in enumerate(required_tools, 1):
                description = f"Execute {tool} for: {task}"
                dependencies = [i-1] if i > 1 else []
                plan.add_step(Step(i, description, tool=tool, dependencies=dependencies))
        
        else:  # complex
            # Detailed multi-step plan
            plan.add_step(Step(1, "Understand and break down the task"))
            
            for i, tool in enumerate(required_tools, 2):
                description = f"Execute {tool}"
                plan.add_step(Step(i, description, tool=tool, dependencies=[i-1]))
            
            final_step = len(required_tools) + 2
            plan.add_step(Step(final_step, "Synthesize results", dependencies=[final_step-1]))
        
        plan.status = "ready"
        self.plans.append(plan)
        
        print(f"   Created plan with {len(plan.steps)} steps")
        for step in plan.steps:
            print(f"   Step {step.step_id}: {step.description}")
        
        return plan
