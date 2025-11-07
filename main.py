"""
Main Entry Point
File: main.py
"""

from core.agent import AgenticSystem
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationTool
from tools.text_analysis import TextAnalysisTool
from config.settings import settings
import json


def main():
    """Main function to run the agentic system"""
    
    # Validate settings
    settings.validate()
    
    # Initialize the agentic system
    agent = AgenticSystem()
    
    # Register tools
    print("\n📦 Registering tools...")
    agent.register_tool(CalculatorTool())
    agent.register_tool(FileOperationTool())
    agent.register_tool(TextAnalysisTool())
    
    print("\n" + "="*60)
    print("🤖 AI Agentic System Ready!")
    print("="*60)
    
    # Example tasks
    example_tasks = [
        "Calculate 25 + 37",
        "Analyze the text 'Hello World! This is a test.'",
        "Calculate the square root of 144"
    ]
    
    print("\n📋 Running example tasks...\n")
    
    for task in example_tasks:
        result = agent.process_task(task)
        print(f"\n✅ Task completed: {result['status']}\n")
    
    # Show statistics
    print("\n" + "="*60)
    print("📊 System Statistics")
    print("="*60)
    
    stats = agent.get_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n" + "="*60)
    print("🎉 Demo completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
