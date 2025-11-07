"""
Tool Manager - Orchestrator for all tools
File: tools/manager.py
"""

from typing import Dict, List, Optional, Any
from tools.base import BaseTool


class ToolManager:
    """Manager untuk mengelola lifecycle semua tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool) -> None:
        """Register tool ke system"""
        self.tools[tool.metadata.name] = tool
        
        # Organize by category
        category = tool.metadata.category
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(tool.metadata.name)
        
        print(f"✓ Tool registered: {tool.metadata.name} ({category})")
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Ambil tool berdasarkan nama"""
        return self.tools.get(name)
    
    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute tool dengan error handling"""
        tool = self.get(name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }
        
        return tool.run(**kwargs)
    
    def list_tools(self, category: str = None) -> List[str]:
        """List tools, optionally filtered by category"""
        if category:
            return self.categories.get(category, [])
        return list(self.tools.keys())
    
    def get_schemas(self) -> List[Dict]:
        """Get all tool schemas for LLM"""
        return [tool.to_schema() for tool in self.tools.values()]
    
    def get_statistics(self) -> Dict[str, Dict]:
        """Get usage statistics for all tools"""
        return {name: tool.get_stats() for name, tool in self.tools.items()}
    
    def get_categories(self) -> Dict[str, List[str]]:
        """Get tools organized by category"""
        return self.categories
