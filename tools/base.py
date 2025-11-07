"""
Base Tool Implementation
File: tools/base.py
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class ToolMetadata:
    """Metadata untuk tool"""
    def __init__(self, name: str, description: str, category: str, 
                 version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.created_at = datetime.now().isoformat()


class ToolParameter:
    """Definisi parameter untuk tool"""
    def __init__(self, name: str, type: str, description: str, 
                 required: bool = True, default: Any = None):
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.default = default


class BaseTool(ABC):
    """Base class untuk semua tools"""
    
    def __init__(self, metadata: ToolMetadata):
        self.metadata = metadata
        self.parameters: List[ToolParameter] = []
        self.usage_count = 0
        self.success_count = 0
        self.error_count = 0
        self.last_used = None
        self.execution_times: List[float] = []
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Method utama yang harus diimplementasi"""
        pass
    
    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """Validasi input sebelum eksekusi"""
        pass
    
    def add_parameter(self, param: ToolParameter):
        """Tambahkan parameter definition"""
        self.parameters.append(param)
    
    def to_schema(self) -> Dict:
        """Convert tool ke Claude function calling schema"""
        properties = {}
        required = []
        
        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.required:
                required.append(param.name)
        
        return {
            "name": self.metadata.name,
            "description": self.metadata.description,
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """Wrapper untuk execute dengan error handling"""
        import time
        
        self.usage_count += 1
        self.last_used = datetime.now().isoformat()
        
        if not self.validate_input(**kwargs):
            self.error_count += 1
            return {
                "success": False,
                "error": "Invalid input parameters",
                "tool": self.metadata.name
            }
        
        try:
            start_time = time.time()
            result = self.execute(**kwargs)
            execution_time = time.time() - start_time
            
            self.execution_times.append(execution_time)
            self.success_count += 1
            
            return {
                "success": True,
                "result": result,
                "tool": self.metadata.name,
                "execution_time": execution_time
            }
        except Exception as e:
            self.error_count += 1
            return {
                "success": False,
                "error": str(e),
                "tool": self.metadata.name
            }
    
    def get_stats(self) -> Dict:
        """Dapatkan statistik penggunaan tool"""
        avg_time = (sum(self.execution_times) / len(self.execution_times) 
                   if self.execution_times else 0)
        
        return {
            "name": self.metadata.name,
            "category": self.metadata.category,
            "usage_count": self.usage_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{(self.success_count / self.usage_count * 100):.1f}%" 
                           if self.usage_count > 0 else "N/A",
            "average_execution_time": f"{avg_time:.3f}s",
            "last_used": self.last_used
        }
