# 🤖 AI Agentic System

A modular and extensible AI Agentic System built with Python. This system provides a foundation for building intelligent agents that can understand tasks, create execution plans, and learn from experience.

## 🌟 Features

- **Modular Architecture**: Clean separation of concerns with core modules and tools
- **Task Understanding**: Automatic analysis of task complexity and requirements
- **Smart Planning**: Rule-based planning with dependency resolution
- **Tool System**: Extensible tool framework with built-in tools
- **Learning Module**: Tracks execution history and generates insights
- **Error Handling**: Robust error handling and validation

## 📁 Project Structure

```
visualisation-ai/
├── core/                      # Core agent modules
│   ├── agent.py              # Main agentic system orchestrator
│   ├── task_understanding.py # Task analysis module
│   ├── planning.py           # Planning and step generation
│   ├── execution.py          # Plan execution engine
│   └── learning.py           # Learning and metrics tracking
├── tools/                     # Tool implementations
│   ├── base.py               # Base tool classes
│   ├── manager.py            # Tool manager
│   ├── calculator.py         # Calculator tool
│   ├── file_operations.py    # File operations tool
│   └── text_analysis.py      # Text analysis tool
├── config/                    # Configuration
│   └── settings.py           # Settings and environment config
├── tests/                     # Test suites
│   ├── test_core/            # Core module tests
│   ├── test_tools/           # Tool tests
│   └── test_integration/     # Integration tests
├── utils/                     # Utility functions
├── memory/                    # Memory and storage
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/asepsafrudin/visualisation-ai.git
cd visualisation-ai
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Running the System

Run the demo:
```bash
python main.py
```

## 🛠️ Available Tools

### Calculator Tool
Perform mathematical operations:
- Basic: add, subtract, multiply, divide
- Advanced: power, sqrt, sin, cos, tan

### File Operations Tool
File system operations:
- Read files
- Write files
- List directories
- Delete files
- Check file existence

### Text Analysis Tool
Analyze text content:
- Character count
- Word count
- Sentence count
- Line count
- Detailed statistics (optional)

## 📊 Core Modules

### Task Understanding
Analyzes incoming tasks to determine:
- Task complexity (simple, moderate, complex)
- Required tools
- Estimated execution steps

### Planning
Creates execution plans with:
- Step-by-step breakdown
- Tool assignment
- Dependency management

### Execution
Executes plans with:
- Sequential step execution
- Error handling and retry logic
- Progress tracking

### Learning
Tracks and learns from executions:
- Execution history
- Performance metrics
- Tool usage statistics
- Success rate tracking

## 🔧 Creating Custom Tools

To create a custom tool, extend the `BaseTool` class:

```python
from tools.base import BaseTool, ToolMetadata, ToolParameter

class MyCustomTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="my_tool",
            description="Description of what the tool does",
            category="my_category"
        )
        super().__init__(metadata)
        
        self.add_parameter(ToolParameter(
            "param1", "string", "Parameter description", required=True
        ))
    
    def validate_input(self, **kwargs) -> bool:
        # Validate input parameters
        return True
    
    def execute(self, **kwargs):
        # Implement tool logic
        return result
```

Register your tool:
```python
agent = AgenticSystem()
agent.register_tool(MyCustomTool())
```

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=. tests/
```

## 📈 Roadmap

This implementation covers **Phase 1-3** of the full roadmap:

- ✅ Phase 1: Foundation (Core Infrastructure)
- ✅ Phase 2: Core Modules (Task Understanding, Planning, Execution, Learning)
- ✅ Phase 3: Essential Tools (Calculator, File Ops, Text Analysis)
- ⏳ Phase 4: Communication Tools
- ⏳ Phase 5: Memory System
- ⏳ Phase 6: Advanced Features
- ⏳ Phase 7: Monitoring & Observability
- ⏳ Phase 8: Production Readiness
- ⏳ Phase 9: Advanced Capabilities
- ⏳ Phase 10: Ecosystem & Community

See [implementation_roadmap.md](docs/implementation_roadmap.md) for the complete roadmap.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with inspiration from modern AI agent frameworks and best practices in software architecture.

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

**Status**: Active Development 🚧

**Version**: 1.0.0

**Last Updated**: November 2025
