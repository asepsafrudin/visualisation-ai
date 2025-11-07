"""
Task Understanding Module
File: core/task_understanding.py
"""

from typing import Dict, Any
from datetime import datetime


class TaskUnderstanding:
    """Modul untuk memahami dan menganalisis task"""
    
    def __init__(self, llm_client=None):
        self.client = llm_client
    
    def analyze(self, task: str) -> Dict[str, Any]:
        """Analisis task dan ekstrak informasi penting"""
        print(f"🧠 [TaskUnderstanding] Analyzing task...")
        
        analysis = {
            "original_task": task,
            "complexity": self._assess_complexity(task),
            "requires_tools": self._detect_tool_needs(task),
            "estimated_steps": self._estimate_steps(task),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"   Complexity: {analysis['complexity']}")
        print(f"   Potential tools: {', '.join(analysis['requires_tools']) if analysis['requires_tools'] else 'None detected'}")
        
        return analysis
    
    def _assess_complexity(self, task: str) -> str:
        """Estimasi kompleksitas task"""
        word_count = len(task.split())
        
        # Count complexity indicators
        complexity_indicators = [
            "then", "after", "before", "if", "when", "multiple",
            "calculate", "analyze", "compare", "find"
        ]
        
        indicator_count = sum(1 for word in complexity_indicators if word in task.lower())
        
        if word_count < 10 and indicator_count == 0:
            return "simple"
        elif word_count < 30 and indicator_count < 3:
            return "moderate"
        else:
            return "complex"
    
    def _detect_tool_needs(self, task: str) -> list:
        """Deteksi tools yang mungkin dibutuhkan"""
        task_lower = task.lower()
        tools = []
        
        # Tool detection patterns
        if any(word in task_lower for word in ["calculate", "compute", "math", "add", "multiply"]):
            tools.append("calculator")
        
        if any(word in task_lower for word in ["file", "read", "write", "save", "load"]):
            tools.append("file_operation")
        
        if any(word in task_lower for word in ["analyze text", "count words", "statistics"]):
            tools.append("text_analysis")
        
        if any(word in task_lower for word in ["search", "find online", "web"]):
            tools.append("web_search")
        
        if any(word in task_lower for word in ["database", "query", "sql"]):
            tools.append("database")
        
        return tools
    
    def _estimate_steps(self, task: str) -> int:
        """Estimasi jumlah langkah yang dibutuhkan"""
        complexity = self._assess_complexity(task)
        
        if complexity == "simple":
            return 1
        elif complexity == "moderate":
            return 3
        else:
            return 5
