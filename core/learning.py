"""
Learning Module
File: core/learning.py
"""

from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path


class LearningModule:
    """Modul untuk menyimpan dan belajar dari execution history"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path) if storage_path else Path("data/learning")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.execution_log = []
        self.performance_metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_tools_used": 0,
            "tool_usage": {}
        }
    
    def record_execution(self, plan: Dict, result: Dict[str, Any]):
        """Record execution untuk learning"""
        print(f"📊 [Learning] Recording execution...")
        
        execution_record = {
            "timestamp": datetime.now().isoformat(),
            "task": plan.get("task"),
            "plan": plan,
            "result": result,
            "success": result.get("plan_status") == "completed"
        }
        
        self.execution_log.append(execution_record)
        self._update_metrics(execution_record)
        self._save_to_disk()
        
        print(f"   Execution recorded. Total executions: {self.performance_metrics['total_executions']}")
    
    def _update_metrics(self, record: Dict):
        """Update performance metrics"""
        self.performance_metrics["total_executions"] += 1
        
        if record["success"]:
            self.performance_metrics["successful_executions"] += 1
        else:
            self.performance_metrics["failed_executions"] += 1
        
        # Track tool usage
        steps = record["plan"].get("steps", [])
        for step in steps:
            tool = step.get("tool")
            if tool:
                self.performance_metrics["total_tools_used"] += 1
                if tool not in self.performance_metrics["tool_usage"]:
                    self.performance_metrics["tool_usage"][tool] = 0
                self.performance_metrics["tool_usage"][tool] += 1
    
    def get_insights(self) -> Dict[str, Any]:
        """Generate insights dari execution history"""
        metrics = self.performance_metrics
        
        success_rate = (
            metrics["successful_executions"] / metrics["total_executions"] * 100
            if metrics["total_executions"] > 0 else 0
        )
        
        # Most used tools
        most_used_tools = sorted(
            metrics["tool_usage"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        insights = {
            "total_executions": metrics["total_executions"],
            "success_rate": f"{success_rate:.1f}%",
            "successful": metrics["successful_executions"],
            "failed": metrics["failed_executions"],
            "total_tools_used": metrics["total_tools_used"],
            "most_used_tools": [
                {"tool": tool, "count": count}
                for tool, count in most_used_tools
            ]
        }
        
        return insights
    
    def _save_to_disk(self):
        """Save execution log to disk"""
        log_file = self.storage_path / "execution_log.json"
        metrics_file = self.storage_path / "metrics.json"
        
        with open(log_file, 'w') as f:
            json.dump(self.execution_log, f, indent=2)
        
        with open(metrics_file, 'w') as f:
            json.dump(self.performance_metrics, f, indent=2)
    
    def load_from_disk(self):
        """Load execution log from disk"""
        log_file = self.storage_path / "execution_log.json"
        metrics_file = self.storage_path / "metrics.json"
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                self.execution_log = json.load(f)
        
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                self.performance_metrics = json.load(f)
        
        print(f"📊 [Learning] Loaded {len(self.execution_log)} execution records")
