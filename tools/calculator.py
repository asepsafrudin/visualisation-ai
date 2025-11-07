"""
Calculator Tool
File: tools/calculator.py
"""

from tools.base import BaseTool, ToolMetadata, ToolParameter
import math


class CalculatorTool(BaseTool):
    """Tool untuk operasi matematika"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="calculator",
            description="Perform mathematical operations: add, subtract, multiply, divide, power, sqrt, sin, cos, tan",
            category="computation"
        )
        super().__init__(metadata)
        
        # Define parameters
        self.add_parameter(ToolParameter(
            "operation", "string", 
            "Operation: add, subtract, multiply, divide, power, sqrt, sin, cos, tan",
            required=True
        ))
        self.add_parameter(ToolParameter(
            "a", "number", "First number", required=True
        ))
        self.add_parameter(ToolParameter(
            "b", "number", "Second number (not required for sqrt, sin, cos, tan)", 
            required=False
        ))
    
    def validate_input(self, **kwargs) -> bool:
        operation = kwargs.get("operation")
        a = kwargs.get("a")
        b = kwargs.get("b")
        
        valid_ops = ["add", "subtract", "multiply", "divide", "power", 
                     "sqrt", "sin", "cos", "tan"]
        
        if operation not in valid_ops:
            return False
        if a is None:
            return False
        if operation not in ["sqrt", "sin", "cos", "tan"] and b is None:
            return False
        
        return True
    
    def execute(self, **kwargs) -> float:
        operation = kwargs["operation"]
        a = float(kwargs["a"])
        b = float(kwargs.get("b", 0))
        
        operations = {
            "add": lambda x, y: x + y,
            "subtract": lambda x, y: x - y,
            "multiply": lambda x, y: x * y,
            "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero",
            "power": lambda x, y: x ** y,
            "sqrt": lambda x, y: math.sqrt(x),
            "sin": lambda x, y: math.sin(x),
            "cos": lambda x, y: math.cos(x),
            "tan": lambda x, y: math.tan(x)
        }
        
        return operations[operation](a, b)
