"""
File Operations Tool
File: tools/file_operations.py
"""

from tools.base import BaseTool, ToolMetadata, ToolParameter
import os
from pathlib import Path
from typing import Any


class FileOperationTool(BaseTool):
    """Tool untuk operasi file"""
    
    def __init__(self, allowed_dirs: list = None):
        metadata = ToolMetadata(
            name="file_operation",
            description="Read, write, list, or delete files. Operations: read, write, list, delete, exists",
            category="file_system"
        )
        super().__init__(metadata)
        
        # Security: restrict to allowed directories
        self.allowed_dirs = allowed_dirs or [os.getcwd()]
        
        self.add_parameter(ToolParameter(
            "operation", "string", 
            "Operation: read, write, list, delete, exists",
            required=True
        ))
        self.add_parameter(ToolParameter(
            "path", "string", "File or directory path", required=True
        ))
        self.add_parameter(ToolParameter(
            "content", "string", "Content to write (for write operation)", 
            required=False
        ))
    
    def validate_input(self, **kwargs) -> bool:
        operation = kwargs.get("operation")
        path = kwargs.get("path")
        
        if operation not in ["read", "write", "list", "delete", "exists"]:
            return False
        if not path:
            return False
        if operation == "write" and not kwargs.get("content"):
            return False
        
        # Security check
        abs_path = os.path.abspath(path)
        if not any(abs_path.startswith(allowed) for allowed in self.allowed_dirs):
            return False
        
        return True
    
    def execute(self, **kwargs) -> Any:
        operation = kwargs["operation"]
        path = kwargs["path"]
        
        if operation == "read":
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif operation == "write":
            content = kwargs["content"]
            # Create parent directories if needed
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File written successfully: {path}"
        
        elif operation == "list":
            if os.path.isdir(path):
                items = os.listdir(path)
                return {"files": items, "count": len(items)}
            return "Path is not a directory"
        
        elif operation == "delete":
            if os.path.exists(path):
                os.remove(path)
                return f"File deleted: {path}"
            return "File does not exist"
        
        elif operation == "exists":
            return {"exists": os.path.exists(path), "path": path}
