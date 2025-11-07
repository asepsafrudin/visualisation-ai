"""
Simple Test Script
File: test_system.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.agent import AgenticSystem
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationTool
from tools.text_analysis import TextAnalysisTool


def test_tool_creation():
    """Test tool creation"""
    print("Testing tool creation...")
    
    calc = CalculatorTool()
    assert calc.metadata.name == "calculator"
    print("✓ Calculator tool created")
    
    file_ops = FileOperationTool()
    assert file_ops.metadata.name == "file_operation"
    print("✓ File operations tool created")
    
    text_analysis = TextAnalysisTool()
    assert text_analysis.metadata.name == "text_analysis"
    print("✓ Text analysis tool created")


def test_calculator_operations():
    """Test calculator operations"""
    print("\nTesting calculator operations...")
    
    calc = CalculatorTool()
    
    # Test addition
    result = calc.run(operation="add", a=5, b=3)
    assert result["success"] == True
    assert result["result"] == 8
    print("✓ Addition: 5 + 3 = 8")
    
    # Test multiplication
    result = calc.run(operation="multiply", a=4, b=7)
    assert result["success"] == True
    assert result["result"] == 28
    print("✓ Multiplication: 4 × 7 = 28")
    
    # Test square root
    result = calc.run(operation="sqrt", a=144)
    assert result["success"] == True
    assert result["result"] == 12.0
    print("✓ Square root: √144 = 12")


def test_text_analysis():
    """Test text analysis"""
    print("\nTesting text analysis...")
    
    text_tool = TextAnalysisTool()
    
    test_text = "Hello World! This is a test."
    result = text_tool.run(text=test_text)
    
    assert result["success"] == True
    assert result["result"]["words"] == 6
    print(f"✓ Text analysis: '{test_text}'")
    print(f"  Words: {result['result']['words']}")
    print(f"  Characters: {result['result']['characters']}")


def test_agent_system():
    """Test agent system initialization"""
    print("\nTesting agent system...")
    
    agent = AgenticSystem()
    
    # Register tools
    agent.register_tool(CalculatorTool())
    agent.register_tool(TextAnalysisTool())
    
    # List tools
    tools_info = agent.list_tools()
    assert len(tools_info["tools"]) == 2
    print(f"✓ Agent system initialized with {len(tools_info['tools'])} tools")


def test_task_understanding():
    """Test task understanding module"""
    print("\nTesting task understanding...")
    
    from core.task_understanding import TaskUnderstanding
    
    task_module = TaskUnderstanding()
    
    # Simple task
    analysis = task_module.analyze("Calculate 5 + 3")
    assert analysis["complexity"] in ["simple", "moderate"]
    assert "calculator" in analysis["requires_tools"]
    print(f"✓ Simple task analyzed: complexity={analysis['complexity']}")
    
    # Complex task
    analysis = task_module.analyze("Calculate the sum, then multiply by 2, and finally find the square root")
    assert analysis["complexity"] in ["simple", "moderate", "complex"]
    print(f"✓ Complex task analyzed: complexity={analysis['complexity']}")
    print(f"  Tools detected: {', '.join(analysis['requires_tools'])}")
    print(f"  Estimated steps: {analysis['estimated_steps']}")


def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Running System Tests")
    print("="*60)
    
    try:
        test_tool_creation()
        test_calculator_operations()
        test_text_analysis()
        test_agent_system()
        test_task_understanding()
        
        print("\n" + "="*60)
        print("✅ All tests passed successfully!")
        print("="*60)
        return 0
    
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
