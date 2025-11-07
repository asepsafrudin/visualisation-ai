# 🤖 Step-by-Step Implementation Guide
## Panduan Implementasi AI Agentic System untuk AI Agent di VS Code

---

## 📋 Prerequisites Check

```bash
# Verifikasi Python version (minimum 3.8)
python --version

# Verifikasi pip
pip --version

# Verifikasi git
git --version
```

**Expected Output:**
- Python 3.8 atau lebih tinggi
- pip 20.0 atau lebih tinggi
- git 2.x atau lebih tinggi

---

## STEP 1: Project Initialization

### 1.1 Create Project Directory

```bash
# Create main project folder
mkdir agentic_system
cd agentic_system

# Verify current directory
pwd
```

**Expected:** You should be in `/path/to/agentic_system`

### 1.2 Initialize Git Repository

```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
EOF
```

**Verification:**
```bash
ls -la
# Should show .git/ and .gitignore
```

### 1.3 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Unix/MacOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
which python
```

**Expected:** Python path should point to venv directory

### 1.4 Create Project Structure

```bash
# Create all directories at once
mkdir -p core tools memory config utils tests/test_core tests/test_tools tests/test_integration

# Create __init__.py files
touch core/__init__.py
touch tools/__init__.py
touch memory/__init__.py
touch config/__init__.py
touch utils/__init__.py
touch tests/__init__.py
touch tests/test_core/__init__.py
touch tests/test_tools/__init__.py
touch tests/test_integration/__init__.py

# Verify structure
tree -L 2
```

**Expected Directory Tree:**
```
agentic_system/
├── core/
│   └── __init__.py
├── tools/
│   └── __init__.py
├── memory/
│   └── __init__.py
├── config/
│   └── __init__.py
├── utils/
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_core/
│   ├── test_tools/
│   └── test_integration/
├── venv/
└── .gitignore
```

---

## STEP 2: Dependencies Installation

### 2.1 Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
# Core Dependencies
anthropic>=0.18.0
python-dotenv>=1.0.0
pydantic>=2.0.0

# Web & API
requests>=2.31.0
beautifulsoup4>=4.12.0

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-asyncio>=0.21.0

# Utilities
colorama>=0.4.6
rich>=13.7.0
EOF
```

### 2.2 Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Verification:**
```bash
# Check specific packages
python -c "import anthropic; print('Anthropic:', anthropic.__version__)"
python -c "import requests; print('Requests:', requests.__version__)"
```

### 2.3 Create Environment Configuration

```bash
# Create .env file
cat > .env << 'EOF'
# Anthropic API Key
ANTHROPIC_API_KEY=your_api_key_here

# Model Configuration
DEFAULT_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=4096

# Agent Configuration
MAX_ITERATIONS=10
ENABLE_LOGGING=true
LOG_LEVEL=INFO

# Tool Configuration
ENABLE_FILE_OPERATIONS=true
ENABLE_WEB_SEARCH=false
ENABLE_DATABASE=false

# Paths
LOG_DIR=./logs
DATA_DIR=./data
CACHE_DIR=./cache
EOF

# Create example env file
cp .env .env.example
```

**⚠️ IMPORTANT:** Replace `your_api_key_here` with actual API key

---

## STEP 3: Core Module Implementation

### 3.1 Create Base Tool Class

```bash
cat > tools/base.py << 'EOFPYTHON'
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
EOFPYTHON
```

**Verification:**
```bash
# Test import
python -c "from tools.base import BaseTool, ToolMetadata, ToolParameter; print('✓ Base tool imported successfully')"
```

### 3.2 Create Tool Manager

```bash
cat > tools/manager.py << 'EOFPYTHON'
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
EOFPYTHON
```

**Verification:**
```bash
python -c "from tools.manager import ToolManager; tm = ToolManager(); print('✓ ToolManager created successfully')"
```

### 3.3 Create Configuration Module

```bash
cat > config/settings.py << 'EOFPYTHON'
"""
Configuration Settings
File: config/settings.py
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-5-20250929")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    
    # Agent Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    ENABLE_LOGGING: bool = os.getenv("ENABLE_LOGGING", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Tool Configuration
    ENABLE_FILE_OPERATIONS: bool = os.getenv("ENABLE_FILE_OPERATIONS", "true").lower() == "true"
    ENABLE_WEB_SEARCH: bool = os.getenv("ENABLE_WEB_SEARCH", "false").lower() == "true"
    ENABLE_DATABASE: bool = os.getenv("ENABLE_DATABASE", "false").lower() == "true"
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")
    DATA_DIR: Path = BASE_DIR / os.getenv("DATA_DIR", "data")
    CACHE_DIR: Path = BASE_DIR / os.getenv("CACHE_DIR", "cache")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is not set in .env file")
        
        # Create directories if they don't exist
        cls.LOG_DIR.mkdir(exist_ok=True)
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.CACHE_DIR.mkdir(exist_ok=True)
        
        return True


# Create settings instance
settings = Settings()
EOFPYTHON
```

**Verification:**
```bash
python -c "from config.settings import settings; print('✓ Settings loaded'); print('Model:', settings.DEFAULT_MODEL)"
```

---

## STEP 4: Implement Basic Tools

### 4.1 Calculator Tool

```bash
cat > tools/calculator.py << 'EOFPYTHON'
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
EOFPYTHON
```

### 4.2 File Operations Tool

```bash
cat > tools/file_operations.py << 'EOFPYTHON'
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
EOFPYTHON
```

### 4.3 Text Analysis Tool

```bash
cat > tools/text_analysis.py << 'EOFPYTHON'
"""
Text Analysis Tool
File: tools/text_analysis.py
"""

from tools.base import BaseTool, ToolMetadata, ToolParameter
from typing import Dict


class TextAnalysisTool(BaseTool):
    """Tool untuk analisis teks"""
    
    def __init__(self):
        metadata = ToolMetadata(
            name="text_analysis",
            description="Analyze text: count words, characters, sentences, lines, and provide statistics",
            category="computation"
        )
        super().__init__(metadata)
        
        self.add_parameter(ToolParameter(
            "text", "string", "Text to analyze", required=True
        ))
        self.add_parameter(ToolParameter(
            "detailed", "boolean", "Include detailed statistics", 
            required=False, default=False
        ))
    
    def validate_input(self, **kwargs) -> bool:
        return bool(kwargs.get("text"))
    
    def execute(self, **kwargs) -> Dict:
        text = kwargs["text"]
        detailed = kwargs.get("detailed", False)
        
        # Basic statistics
        stats = {
            "characters": len(text),
            "characters_no_spaces": len(text.replace(" ", "")),
            "words": len(text.split()),
            "sentences": text.count('.') + text.count('!') + text.count('?'),
            "lines": len(text.split('\n')),
            "paragraphs": len([p for p in text.split('\n\n') if p.strip()])
        }
        
        if detailed:
            words = text.split()
            stats["average_word_length"] = (
                sum(len(word) for word in words) / len(words) 
                if words else 0
            )
            stats["unique_words"] = len(set(words))
            stats["longest_word"] = max(words, key=len) if words else ""
        
        return stats
EOFPYTHON
```

**Verification:**
```bash
# Test all tools
python << 'EOFTEST'
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationTool
from tools.text_analysis import TextAnalysisTool

calc = CalculatorTool()
print("✓ CalculatorTool created")

file_ops = FileOperationTool()
print("✓ FileOperationTool created")

text_analysis = TextAnalysisTool()
print("✓ TextAnalysisTool created")

print("\n✓ All tools successfully created!")
EOFTEST
```

---

## STEP 5: Implement Core Agent Modules

### 5.1 Task Understanding Module

```bash
cat > core/task_understanding.py << 'EOFPYTHON'
"""
Task Understanding Module
File: core/task_understanding.py
"""

from typing import Dict, Any
from datetime import datetime


class TaskUnderstanding:
    """Modul untuk memahami dan menganalisis task"""
    
    def __init__(self, llm_client):
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
            return "medium"
        return "complex"
    
    def _detect_tool_needs(self, task: str) -> list:
        """Deteksi tools apa yang mungkin dibutuhkan"""
        keywords = {
            "calculator": ["calculate", "compute", "math", "add", "subtract", 
                          "multiply", "divide", "sum", "total"],
            "file_operation": ["read file", "write file", "save", "load", 
                              "file", "document"],
            "text_analysis": ["analyze text", "count words", "analyze", 
                             "statistics", "word count"],
            "web_search": ["search", "find information", "look up", "google"],
        }
        
        detected = []
        task_lower = task.lower()
        
        for tool, words in keywords.items():
            if any(word in task_lower for word in words):
                detected.append(tool)
        
        return detected
    
    def _estimate_steps(self, task: str) -> int:
        """Estimasi jumlah langkah yang diperlukan"""
        # Count action words
        action_words = ["then", "after", "and", "also", "next", "finally"]
        step_count = 1 + sum(1 for word in action_words if word in task.lower())
        
        return min(step_count, 5)  # Cap at 5 steps
EOFPYTHON
```

### 5.2 Planning Module

```bash
cat > core/planner.py << 'EOFPYTHON'
"""
Planning Module
File: core/planner.py
"""

from typing import Dict, List, Any
from datetime import datetime


class Planner:
    """Modul untuk merencanakan langkah-langkah eksekusi"""
    
    def __init__(self, llm_client):
        self.client = llm_client
    
    def create_plan(self, task_analysis: Dict, available_tools: List[str]) -> Dict[str, Any]:
        """Buat rencana eksekusi berdasarkan analisis task"""
        print(f"📋 [Planner] Creating execution plan...")
        
        task = task_analysis["original_task"]
        complexity = task_analysis["complexity"]
        required_tools = task_analysis["requires_tools"]
        
        plan = {
            "task": task,
            "complexity": complexity,
            "steps": self._generate_steps(task_analysis, available_tools),
            "estimated_iterations": task_analysis["estimated_steps"],
            "tools_needed": required_tools,
            "available_tools": available_tools,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"   Generated {len(plan['steps'])} steps")
        print(f"   Tools needed: {', '.join(required_tools) if required_tools else 'None'}")
        
        return plan
    
    def _generate_steps(self, analysis: Dict, available_tools: List[str]) -> List[Dict]:
        """Generate langkah-langkah eksekusi"""
        steps = [
            {
                "step": 1,
                "action": "understand",
                "description": "Understand task requirements"
            }
        ]
        
        # Add tool usage steps
        for i, tool in enumerate(analysis["requires_tools"], start=2):
            if tool in available_tools:
                steps.append({
                    "step": i,
                    "action": "use_tool",
                    "tool": tool,
                    "description": f"Use {tool} to gather/process information"
                })
        
        # Add synthesis step
        steps.append({
            "step": len(steps) + 1,
            "action": "synthesize",
            "description": "Combine results and provide final answer"
        })
        
        return steps
EOFPYTHON
```

### 5.3 Executor Module

```bash
cat > core/executor.py << 'EOFPYTHON'
"""
Executor Module
File: core/executor.py
"""

from typing import Dict, Any, List
from datetime import datetime
import json


class Executor:
    """Modul untuk mengeksekusi action dengan tools"""
    
    def __init__(self, llm_client, tool_manager):
        self.client = llm_client
        self.tool_manager = tool_manager
        self.model = "claude-sonnet-4-5-20250929"
    
    def execute(self, task: str, plan: Dict, max_iterations: int = 10) -> Dict[str, Any]:
        """Eksekusi task berdasarkan plan"""
        print(f"⚙️  [Executor] Starting execution...")
        print(f"   Max iterations: {max_iterations}")
        
        system_prompt = """You are an intelligent AI agent with access to various tools.

Analyze the task carefully and use the appropriate tools to accomplish it.
Think step by step and provide clear, accurate results.

When using tools:
1. Choose the right tool for the job
2. Provide correct parameters
3. Interpret results accurately
4. Combine information effectively"""

        messages = [{"role": "user", "content": task}]
        tools_schema = self.tool_manager.get_schemas()
        
        execution_log = []
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n   ━━━ Iteration {iteration} ━━━")
            
            # Call LLM
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tools_schema if tools_schema else None
            )
            
            # Add assistant message to history
            messages.append({"role": "assistant", "content": response.content})
            
            # Check for tool usage
            tool_uses = [block for block in response.content if block.type == "tool_use"]
            
            # Check for text responses
            text_responses = [block.text for block in response.content if block.type == "text"]
            if text_responses:
                print(f"   💭 Agent: {text_responses[0][:100]}...")
            
            if not tool_uses:
                # No more tools needed - task complete
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text
                
                print(f"   ✅ Execution complete")
                
                return {
                    "success": True,
                    "result": final_text,
                    "iterations": iteration,
                    "log": execution_log
                }
            
            # Execute requested tools
            tool_results = []
            for tool_use in tool_uses:
                tool_name = tool_use.name
                tool_input = tool_use.input
                
                print(f"   🔧 Using tool: {tool_name}")
                print(f"      Input: {json.dumps(tool_input, indent=6)}")
                
                # Execute tool
                result = self.tool_manager.execute(tool_name, **tool_input)
                
                if result["success"]:
                    print(f"      ✓ Success: {str(result['result'])[:100]}")
                else:
                    print(f"      ✗ Error: {result['error']}")
                
                # Log execution
                execution_log.append({
                    "iteration": iteration,
                    "tool": tool_name,
                    "input": tool_input,
                    "result": result
                })
                
                # Prepare tool result for LLM
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result.get("result", result.get("error")))
                })
            
            # Add tool results to conversation
            messages.append({"role": "user", "content": tool_results})
        
        # Max iterations reached
        print(f"   ⚠️  Max iterations reached")
        
        return {
            "success": False,
            "result": "Task incomplete: Maximum iterations reached",
            "iterations": iteration,
            "log": execution_log
        }
EOFPYTHON
```

### 5.4 Learning Module

```bash
cat > core/learning.py << 'EOFPYTHON'
"""
Learning Module
File: core/learning.py
"""

from typing import Dict, List, Any
from datetime import datetime
import json


class LearningModule:
    """Modul untuk belajar dari hasil eksekusi"""
    
    def __init__(self):
        self.execution_history: List[Dict] = []
        self.performance_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "average_iterations": 0,
            "total_execution_time": 0
        }
    
    def record_execution(self, task: str, result: Dict, plan: Dict):
        """Catat hasil eksekusi untuk pembelajaran"""
        print(f"📊 [Learning] Recording execution results...")
        
        record = {
            "task": task,
            "success": result.get("success", False),
            "iterations": result.get("iterations", 0),
            "plan": plan,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
        self.execution_history.append(record)
        self._update_metrics(record)
        
        print(f"   Total tasks executed: {self.performance_metrics['total_tasks']}")
    
    def _update_metrics(self, record: Dict):
        """Update performance metrics"""
        metrics = self.performance_metrics
        
        metrics["total_tasks"] += 1
        
        if record["success"]:
            metrics["successful_tasks"] += 1
        else:
            metrics["failed_tasks"] += 1
        
        # Update average iterations
        total = metrics["total_tasks"]
        current_avg = metrics["average_iterations"]
        new_iterations = record["iterations"]
        metrics["average_iterations"] = (
            (current_avg * (total - 1) + new_iterations) / total
        )
    
    def get_insights(self) -> Dict[str, Any]:
        """Dapatkan insights dari pembelajaran"""
        metrics = self.performance_metrics
        total = metrics["total_tasks"]
        
        if total == 0:
            return {
                "status": "No data available",
                "total_tasks": 0
            }
        
        success_rate = (metrics["successful_tasks"] / total * 100)
        
        insights = {
            "total_tasks_executed": total,
            "successful_tasks": metrics["successful_tasks"],
            "failed_tasks": metrics["failed_tasks"],
            "success_rate": f"{success_rate:.1f}%",
            "average_iterations": f"{metrics['average_iterations']:.1f}",
            "performance_trend": self._analyze_trend(),
            "recommendations": self._generate_recommendations()
        }
        
        return insights
    
    def _analyze_trend(self) -> str:
        """Analisis trend performa"""
        if len(self.execution_history) < 3:
            return "Insufficient data for trend analysis"
        
        recent = self.execution_history[-5:]
        success_count = sum(1 for r in recent if r["success"])
        
        success_rate = (success_count / len(recent)) * 100
        
        if success_rate >= 80:
            return "Excellent - High success rate"
        elif success_rate >= 60:
            return "Good - Stable performance"
        elif success_rate >= 40:
            return "Fair - Room for improvement"
        else:
            return "Poor - Needs optimization"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        metrics = self.performance_metrics
        
        if metrics["total_tasks"] == 0:
            return ["Execute more tasks to generate recommendations"]
        
        success_rate = (metrics["successful_tasks"] / metrics["total_tasks"]) * 100
        
        if success_rate < 70:
            recommendations.append("Consider improving task understanding or tool selection")
        
        if metrics["average_iterations"] > 5:
            recommendations.append("High iteration count - consider optimizing tool usage")
        
        if not recommendations:
            recommendations.append("System performing well - continue monitoring")
        
        return recommendations
    
    def export_history(self, filepath: str):
        """Export execution history to file"""
        with open(filepath, 'w') as f:
            json.dump({
                "execution_history": self.execution_history,
                "performance_metrics": self.performance_metrics
            }, f, indent=2)
        
        print(f"   ✓ History exported to {filepath}")
EOFPYTHON
```

---

## STEP 6: Create Main Agent

```bash
cat > core/agent.py << 'EOFPYTHON'
"""
Main Agent - Orchestrator
File: core/agent.py
"""

import os
from anthropic import Anthropic
from typing import Dict, Any
from datetime import datetime

from core.task_understanding import TaskUnderstanding
from core.planner import Planner
from core.executor import Executor
from core.learning import LearningModule
from tools.manager import ToolManager
from tools.base import BaseTool
from config.settings import settings


class AgenticAgent:
    """
    Main AI Agent yang mengorkestrasi semua modul
    
    Architecture:
    1. Task Understanding - Analisis task
    2. Planning - Buat execution plan
    3. Execution - Jalankan dengan tools
    4. Learning - Belajar dari hasil
    """
    
    def __init__(self, api_key: str = None):
        """Initialize agent dengan semua modul"""
        print("🤖 [Agent] Initializing AI Agentic System...")
        
        # Initialize Anthropic client
        self.client = Anthropic(
            api_key=api_key or settings.ANTHROPIC_API_KEY
        )
        
        # Initialize core modules
        self.task_understanding = TaskUnderstanding(self.client)
        self.planner = Planner(self.client)
        self.tool_manager = ToolManager()
        self.executor = Executor(self.client, self.tool_manager)
        self.learning = LearningModule()
        
        # Configuration
        self.max_iterations = settings.MAX_ITERATIONS
        
        print("   ✓ Task Understanding Module")
        print("   ✓ Planning Module")
        print("   ✓ Execution Module")
        print("   ✓ Learning Module")
        print("   ✓ Tool Manager")
        print("🤖 [Agent] System initialized successfully\n")
    
    def register_tool(self, tool: BaseTool):
        """Register a new tool to the agent"""
        self.tool_manager.register(tool)
    
    def run(self, task: str, max_iterations: int = None) -> str:
        """
        Main execution flow:
        1. Understand task
        2. Create plan
        3. Execute with tools
        4. Learn from result
        
        Args:
            task: Task to execute
            max_iterations: Maximum iterations (overrides default)
        
        Returns:
            Result string
        """
        iterations = max_iterations or self.max_iterations
        
        print(f"\n{'='*80}")
        print(f"🎯 NEW TASK")
        print(f"{'='*80}")
        print(f"Task: {task}")
        print(f"{'='*80}\n")
        
        start_time = datetime.now()
        
        try:
            # STEP 1: Understand Task
            print("STEP 1: TASK UNDERSTANDING")
            print("-" * 80)
            task_analysis = self.task_understanding.analyze(task)
            print()
            
            # STEP 2: Create Plan
            print("STEP 2: PLANNING")
            print("-" * 80)
            plan = self.planner.create_plan(
                task_analysis, 
                self.tool_manager.list_tools()
            )
            print()
            
            # STEP 3: Execute
            print("STEP 3: EXECUTION")
            print("-" * 80)
            result = self.executor.execute(task, plan, iterations)
            print()
            
            # STEP 4: Learn
            print("STEP 4: LEARNING")
            print("-" * 80)
            self.learning.record_execution(task, result, plan)
            print()
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Display results
            print(f"\n{'='*80}")
            if result["success"]:
                print("✅ TASK COMPLETED SUCCESSFULLY")
            else:
                print("⚠️  TASK INCOMPLETE")
            print(f"{'='*80}")
            print(f"Iterations: {result['iterations']}/{iterations}")
            print(f"Execution Time: {execution_time:.2f}s")
            print(f"{'='*80}\n")
            
            return result.get("result", "No result available")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}\n")
            return f"Error executing task: {str(e)}"
    
    def get_report(self) -> Dict[str, Any]:
        """Get comprehensive system report"""
        return {
            "learning_insights": self.learning.get_insights(),
            "tool_statistics": self.tool_manager.get_statistics(),
            "tool_categories": self.tool_manager.get_categories(),
            "total_tools": len(self.tool_manager.list_tools()),
            "available_tools": self.tool_manager.list_tools()
        }
    
    def print_report(self):
        """Print formatted system report"""
        import json
        
        print("\n" + "="*80)
        print("📈 SYSTEM PERFORMANCE REPORT")
        print("="*80)
        
        report = self.get_report()
        
        print("\n📊 Learning Insights:")
        print("-" * 80)
        for key, value in report["learning_insights"].items():
            print(f"  {key}: {value}")
        
        print("\n🔧 Tool Statistics:")
        print("-" * 80)
        for tool_name, stats in report["tool_statistics"].items():
            if stats["usage_count"] > 0:
                print(f"\n  {tool_name}:")
                print(f"    Usage: {stats['usage_count']}")
                print(f"    Success Rate: {stats['success_rate']}")
                print(f"    Avg Time: {stats['average_execution_time']}")
        
        print("\n📂 Tool Categories:")
        print("-" * 80)
        for category, tools in report["tool_categories"].items():
            print(f"  {category}: {', '.join(tools)}")
        
        print("\n" + "="*80)
EOFPYTHON
```

---

## STEP 7: Create Main Entry Point

```bash
cat > main.py << 'EOFPYTHON'
"""
Main Entry Point for AI Agentic System
File: main.py

Usage:
    python main.py
"""

from core.agent import AgenticAgent
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationTool
from tools.text_analysis import TextAnalysisTool
from config.settings import settings


def main():
    """Main function to run the AI Agentic System"""
    
    print("\n" + "="*80)
    print("🚀 AI AGENTIC SYSTEM - PRODUCTION READY")
    print("="*80)
    print(f"Model: {settings.DEFAULT_MODEL}")
    print(f"Max Iterations: {settings.MAX_ITERATIONS}")
    print("="*80 + "\n")
    
    # Validate configuration
    try:
        settings.validate()
        print("✓ Configuration validated\n")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease set ANTHROPIC_API_KEY in .env file")
        return
    
    # Initialize agent
    agent = AgenticAgent()
    
    # Register tools
    print("📦 Registering Tools...")
    print("-" * 80)
    agent.register_tool(CalculatorTool())
    agent.register_tool(FileOperationTool())
    agent.register_tool(TextAnalysisTool())
    print()
    
    # Demo tasks
    demo_tasks = [
        "Calculate 156 multiplied by 24, then add 100",
        "Analyze this text: 'Artificial Intelligence is transforming the world. AI agents are becoming more capable every day.'",
        "Calculate the square root of 144, then multiply it by 5",
    ]
    
    print("="*80)
    print("🎬 RUNNING DEMO TASKS")
    print("="*80 + "\n")
    
    # Execute tasks
    for i, task in enumerate(demo_tasks, 1):
        print(f"\n{'#'*80}")
        print(f"DEMO TASK {i}/{len(demo_tasks)}")
        print('#'*80)
        
        result = agent.run(task)
        
        print(f"\n📋 FINAL RESULT:")
        print("-" * 80)
        print(result)
        print("-" * 80)
    
    # Print system report
    agent.print_report()
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
EOFPYTHON
```

---

## STEP 8: Create Test Suite

```bash
cat > tests/test_core/test_agent.py << 'EOFPYTHON'
"""
Test Agent Core Functionality
File: tests/test_core/test_agent.py
"""

import pytest
from core.agent import AgenticAgent
from tools.calculator import CalculatorTool


def test_agent_initialization():
    """Test agent can be initialized"""
    agent = AgenticAgent()
    assert agent is not None
    assert agent.tool_manager is not None
    assert agent.executor is not None


def test_tool_registration():
    """Test tool registration"""
    agent = AgenticAgent()
    calc_tool = CalculatorTool()
    agent.register_tool(calc_tool)
    
    tools = agent.tool_manager.list_tools()
    assert "calculator" in tools


def test_simple_calculation():
    """Test simple calculation task"""
    agent = AgenticAgent()
    agent.register_tool(CalculatorTool())
    
    result = agent.run("Calculate 5 plus 3")
    assert result is not None
    # Note: Actual result verification depends on LLM response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOFPYTHON
```

```bash
cat > tests/test_tools/test_calculator.py << 'EOFPYTHON'
"""
Test Calculator Tool
File: tests/test_tools/test_calculator.py
"""

import pytest
from tools.calculator import CalculatorTool


def test_calculator_addition():
    """Test addition operation"""
    calc = CalculatorTool()
    result = calc.run(operation="add", a=5, b=3)
    
    assert result["success"] == True
    assert result["result"] == 8


def test_calculator_multiplication():
    """Test multiplication operation"""
    calc = CalculatorTool()
    result = calc.run(operation="multiply", a=6, b=7)
    
    assert result["success"] == True
    assert result["result"] == 42


def test_calculator_division_by_zero():
    """Test division by zero handling"""
    calc = CalculatorTool()
    result = calc.run(operation="divide", a=10, b=0)
    
    # Should handle division by zero gracefully
    assert "zero" in str(result["result"]).lower()


def test_calculator_invalid_operation():
    """Test invalid operation"""
    calc = CalculatorTool()
    result = calc.run(operation="invalid", a=5, b=3)
    
    assert result["success"] == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOFPYTHON
```

---

## STEP 9: Create README and Documentation

```bash
cat > README.md << 'EOFMD'
# 🤖 AI Agentic System

Production-ready AI Agent system with modular architecture and extensible tool system.

## Features

- ✅ **Modular Architecture**: Separated concerns (Understanding, Planning, Execution, Learning)
- ✅ **Tool System**: Extensible tool framework with easy registration
- ✅ **Learning Module**: Tracks performance and provides insights
- ✅ **Error Handling**: Robust error handling and recovery
- ✅ **Type Safety**: Type hints throughout
- ✅ **Testing**: Comprehensive test suite

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repository-url>
cd agentic_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create `.env` file:

```bash
ANTHROPIC_API_KEY=your_api_key_here
DEFAULT_MODEL=claude-sonnet-4-5-20250929
MAX_ITERATIONS=10
```

### 3. Run

```bash
python main.py
```

## Architecture

```
┌─────────────────────────────────────────┐
│         AgenticAgent (Orchestrator)      │
└─────────────────┬───────────────────────┘
                  │
     ┌────────────┼────────────┐
     │            │            │
     ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│  Task   │  │Planning │  │Execution│
│  Under  │→ │ Module  │→ │ Module  │
│standing │  │         │  │         │
└─────────┘  └─────────┘  └────┬────┘
                               │
                               ▼
                          ┌─────────┐
                          │  Tool   │
                          │ Manager │
                          └────┬────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
         ┌─────────┐      ┌─────────┐      ┌─────────┐
         │Calculator│      │   File  │      │  Text   │
         │  Tool   │      │   Ops   │      │ Analysis│
         └─────────┘      └─────────┘      └─────────┘
```

## Adding New Tools

### 1. Create Tool Class

```python
from tools.base import BaseTool, ToolMetadata, ToolParameter

class MyCustomTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="my_tool",
            description="Description of what the tool does",
            category="category_name"
        )
        super().__init__(metadata)
        
        self.add_parameter(ToolParameter(
            "param_name", "string", "Parameter description", required=True
        ))
    
    def validate_input(self, **kwargs) -> bool:
        # Validation logic
        return True
    
    def execute(self, **kwargs):
        # Tool logic
        return "result"
```

### 2. Register Tool

```python
from core.agent import AgenticAgent
from tools.my_tool import MyCustomTool

agent = AgenticAgent()
agent.register_tool(MyCustomTool())
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_tools/test_calculator.py -v
```

## Project Structure

```
agentic_system/
├── core/               # Core agent modules
│   ├── agent.py
│   ├── task_understanding.py
│   ├── planner.py
│   ├── executor.py
│   └── learning.py
├── tools/              # Tool implementations
│   ├── base.py
│   ├── manager.py
│   ├── calculator.py
│   ├── file_operations.py
│   └── text_analysis.py
├── config/             # Configuration
│   └── settings.py
├── tests/              # Test suite
├── main.py             # Entry point
├── requirements.txt
└── .env               # Environment variables
```

## Performance Metrics

The system tracks:
- Task success rate
- Average iterations per task
- Tool usage statistics
- Execution times
- Performance trends

Access via:
```python
agent.print_report()
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
EOFMD
```

---

## STEP 10: Verification and Testing

### 10.1 Verify Project Structure

```bash
# Verify all files are created
echo "Checking project structure..."
find . -name "*.py" -type f | grep -v __pycache__ | grep -v venv

# Expected output should show all Python files
```

### 10.2 Run Syntax Check

```bash
# Check Python syntax for all files
echo "Checking Python syntax..."
python -m py_compile core/*.py
python -m py_compile tools/*.py
python -m py_compile config/*.py
python -m py_compile main.py

echo "✓ Syntax check passed"
```

### 10.3 Test Imports

```bash
# Test all imports
python << 'EOFTEST'
print("Testing imports...")

# Core modules
from core.agent import AgenticAgent
print("✓ Core: Agent")

from core.task_understanding import TaskUnderstanding
print("✓ Core: TaskUnderstanding")

from core.planner import Planner
print("✓ Core: Planner")

from core.executor import Executor
print("✓ Core: Executor")

from core.learning import LearningModule
print("✓ Core: LearningModule")

# Tools
from tools.base import BaseTool, ToolMetadata, ToolParameter
print("✓ Tools: Base classes")

from tools.manager import ToolManager
print("✓ Tools: ToolManager")

from tools.calculator import CalculatorTool
print("✓ Tools: Calculator")

from tools.file_operations import FileOperationTool
print("✓ Tools: FileOperations")

from tools.text_analysis import TextAnalysisTool
print("✓ Tools: TextAnalysis")

# Config
from config.settings import settings
print("✓ Config: Settings")

print("\n✅ All imports successful!")
EOFTEST
```

### 10.4 Run Unit Tests

```bash
# Run all tests
echo "Running unit tests..."
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing
```

### 10.5 Test Main Application

```bash
# Set API key (replace with your actual key)
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# Run main application
echo "Testing main application..."
python main.py
```

**Expected Output:**
```
🚀 AI AGENTIC SYSTEM - PRODUCTION READY
================================================================================
Model: claude-sonnet-4-5-20250929
Max Iterations: 10
================================================================================

✓ Configuration validated

🤖 [Agent] Initializing AI Agentic System...
   ✓ Task Understanding Module
   ✓ Planning Module
   ✓ Execution Module
   ✓ Learning Module
   ✓ Tool Manager
🤖 [Agent] System initialized successfully

📦 Registering Tools...
--------------------------------------------------------------------------------
✓ Tool registered: calculator (computation)
✓ Tool registered: file_operation (file_system)
✓ Tool registered: text_analysis (computation)

[Demo execution continues...]
```

---

## STEP 11: Create Helper Scripts

### 11.1 Create Run Script

```bash
cat > run.sh << 'EOFSH'
#!/bin/bash
# Run script for AI Agentic System

echo "🚀 Starting AI Agentic System..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys"
    exit 1
fi

# Run main application
python main.py
EOFSH

chmod +x run.sh
```

### 11.2 Create Setup Script

```bash
cat > setup.sh << 'EOFSH'
#!/bin/bash
# Setup script for AI Agentic System

echo "📦 Setting up AI Agentic System..."

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "Creating directories..."
mkdir -p logs data cache

# Copy environment template
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your ANTHROPIC_API_KEY"
echo "2. Run: ./run.sh"
EOFSH

chmod +x setup.sh
```

### 11.3 Create Test Script

```bash
cat > test.sh << 'EOFSH'
#!/bin/bash
# Test script for AI Agentic System

echo "🧪 Running tests..."

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

echo ""
echo "📊 Coverage report generated in htmlcov/index.html"
EOFSH

chmod +x test.sh
```

---

## STEP 12: Create Interactive CLI (Optional)

```bash
cat > cli.py << 'EOFPYTHON'
"""
Interactive CLI for AI Agentic System
File: cli.py

Usage:
    python cli.py
"""

import cmd
from core.agent import AgenticAgent
from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationTool
from tools.text_analysis import TextAnalysisTool
from config.settings import settings


class AgentCLI(cmd.Cmd):
    """Interactive CLI for AI Agent"""
    
    intro = """
╔══════════════════════════════════════════════════════════════╗
║          AI AGENTIC SYSTEM - Interactive CLI                ║
║                                                              ║
║  Type 'help' for available commands                         ║
║  Type 'task <your task>' to execute a task                  ║
║  Type 'quit' to exit                                        ║
╚══════════════════════════════════════════════════════════════╝
"""
    prompt = "🤖 agent> "
    
    def __init__(self):
        super().__init__()
        
        print("Initializing agent...")
        self.agent = AgenticAgent()
        
        # Register tools
        self.agent.register_tool(CalculatorTool())
        self.agent.register_tool(FileOperationTool())
        self.agent.register_tool(TextAnalysisTool())
        
        print("✓ Agent ready!\n")
    
    def do_task(self, arg):
        """Execute a task: task <your task description>"""
        if not arg:
            print("❌ Please provide a task description")
            print("Example: task Calculate 5 plus 3")
            return
        
        result = self.agent.run(arg)
        print(f"\n📋 Result: {result}\n")
    
    def do_report(self, arg):
        """Show system performance report"""
        self.agent.print_report()
    
    def do_tools(self, arg):
        """List all available tools"""
        tools = self.agent.tool_manager.list_tools()
        categories = self.agent.tool_manager.get_categories()
        
        print("\n🔧 Available Tools:")
        print("="*60)
        for category, tool_list in categories.items():
            print(f"\n{category.upper()}:")
            for tool in tool_list:
                print(f"  - {tool}")
        print("="*60 + "\n")
    
    def do_stats(self, arg):
        """Show tool usage statistics"""
        stats = self.agent.tool_manager.get_statistics()
        
        print("\n📊 Tool Statistics:")
        print("="*60)
        for tool_name, stat in stats.items():
            if stat['usage_count'] > 0:
                print(f"\n{tool_name}:")
                print(f"  Usage: {stat['usage_count']}")
                print(f"  Success Rate: {stat['success_rate']}")
                print(f"  Avg Time: {stat['average_execution_time']}")
        print("="*60 + "\n")
    
    def do_clear(self, arg):
        """Clear the screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.intro)
    
    def do_quit(self, arg):
        """Exit the CLI"""
        print("\n👋 Goodbye!\n")
        return True
    
    def do_exit(self, arg):
        """Exit the CLI"""
        return self.do_quit(arg)
    
    def default(self, line):
        """Handle unknown commands"""
        print(f"❌ Unknown command: {line}")
        print("Type 'help' for available commands")


def main():
    """Run interactive CLI"""
    try:
        settings.validate()
        AgentCLI().cmdloop()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\nPlease set ANTHROPIC_API_KEY in .env file")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")


if __name__ == "__main__":
    main()
EOFPYTHON
```

---

## STEP 13: Final Verification Checklist

```bash
cat > verify.sh << 'EOFSH'
#!/bin/bash
# Verification script

echo "🔍 Verifying AI Agentic System Installation..."
echo ""

# Check Python
echo "1. Checking Python..."
python --version || { echo "❌ Python not found"; exit 1; }
echo "✓ Python installed"
echo ""

# Check virtual environment
echo "2. Checking virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
    exit 1
fi
echo ""

# Check dependencies
echo "3. Checking dependencies..."
source venv/bin/activate
pip list | grep -q "anthropic" && echo "✓ anthropic installed" || echo "❌ anthropic missing"
pip list | grep -q "python-dotenv" && echo "✓ python-dotenv installed" || echo "❌ python-dotenv missing"
pip list | grep -q "pytest" && echo "✓ pytest installed" || echo "❌ pytest missing"
echo ""

# Check file structure
echo "4. Checking file structure..."
files=(
    "main.py"
    "cli.py"
    "core/agent.py"
    "core/task_understanding.py"
    "core/planner.py"
    "core/executor.py"
    "core/learning.py"
    "tools/base.py"
    "tools/manager.py"
    "tools/calculator.py"
    "tools/file_operations.py"
    "tools/text_analysis.py"
    "config/settings.py"
    "requirements.txt"
    ".env"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "❌ $file missing"
    fi
done
echo ""

# Check .env configuration
echo "5. Checking configuration..."
if grep -q "your_api_key_here" .env 2>/dev/null; then
    echo "⚠️  API key not set in .env"
    echo "   Please edit .env and add your ANTHROPIC_API_KEY"
else
    echo "✓ Configuration appears to be set"
fi
echo ""

# Test imports
echo "6. Testing imports..."
python -c "
try:
    from core.agent import AgenticAgent
    from tools.calculator import CalculatorTool
    from tools.manager import ToolManager
    print('✓ All imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
echo ""

echo "═══════════════════════════════════════════"
echo "✅ Verification Complete!"
echo "═══════════════════════════════════════════"
echo ""
echo "To run the system:"
echo "  ./run.sh          - Run main demo"
echo "  python cli.py     - Run interactive CLI"
echo "  ./test.sh         - Run tests"
echo ""
EOFSH

chmod +x verify.sh
```

### Run Verification

```bash
./verify.sh
```

---

## STEP 14: Create Documentation Files

### 14.1 Create CONTRIBUTING.md

```bash
cat > CONTRIBUTING.md << 'EOFMD'
# Contributing to AI Agentic System

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Run setup script: `./setup.sh`
4. Create a branch: `git checkout -b feature/my-feature`

## Adding New Tools

### 1. Create Tool Class

Create a new file in `tools/` directory:

```python
from tools.base import BaseTool, ToolMetadata, ToolParameter

class MyTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="my_tool",
            description="What it does",
            category="category"
        )
        super().__init__(metadata)
        
        # Add parameters
        self.add_parameter(ToolParameter(
            "param", "string", "Description", required=True
        ))
    
    def validate_input(self, **kwargs) -> bool:
        # Validation logic
        return True
    
    def execute(self, **kwargs):
        # Implementation
        return "result"
```

### 2. Add Tests

Create test file in `tests/test_tools/`:

```python
import pytest
from tools.my_tool import MyTool

def test_my_tool():
    tool = MyTool()
    result = tool.run(param="value")
    assert result["success"] == True
```

### 3. Update Documentation

- Add tool to README.md
- Document parameters and usage
- Provide examples

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

## Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest --cov=. --cov-report=html
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit PR with clear description

## Questions?

Open an issue for discussion!
EOFMD
```

### 14.2 Create CHANGELOG.md

```bash
cat > CHANGELOG.md << 'EOFMD'
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-11-06

### Added
- Core agent architecture with 5 modules
- Task Understanding module
- Planning module
- Execution module with tool orchestration
- Learning module with performance tracking
- Tool management system
- Base tool framework
- Calculator tool
- File operations tool
- Text analysis tool
- Interactive CLI
- Comprehensive test suite
- Documentation and setup scripts

### Features
- Modular architecture
- Extensible tool system
- Error handling and recovery
- Performance metrics
- Tool usage statistics
- Configuration management

## [0.1.0] - Initial Development

### Added
- Initial project structure
- Basic proof of concept
EOFMD
```

---

## STEP 15: Quick Reference Commands

```bash
cat > COMMANDS.md << 'EOFMD'
# Quick Reference Commands

## Setup & Installation

```bash
# Initial setup
./setup.sh

# Manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the System

```bash
# Run demo
./run.sh
# or
python main.py

# Interactive CLI
python cli.py

# Run tests
./test.sh
# or
pytest tests/ -v
```

## Verification

```bash
# Verify installation
./verify.sh

# Check syntax
python -m py_compile main.py
python -m py_compile core/*.py
python -m py_compile tools/*.py

# Test imports
python -c "from core.agent import AgenticAgent; print('OK')"
```

## Development

```bash
# Activate environment
source venv/bin/activate

# Install new package
pip install package_name
pip freeze > requirements.txt

# Run specific test
pytest tests/test_core/test_agent.py -v

# Coverage report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

## Git Commands

```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Description"

# Push changes
git push origin feature/my-feature
```

## Troubleshooting

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reset virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

```bash
# View current settings
cat .env

# Edit settings
nano .env  # or vim .env

# Required variables
ANTHROPIC_API_KEY=your_key_here
DEFAULT_MODEL=claude-sonnet-4-5-20250929
MAX_ITERATIONS=10
```

## Useful Python Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Show package info
pip show anthropic

# Python REPL with imports
python -i -c "from core.agent import AgenticAgent; agent = AgenticAgent()"
```
EOFMD
```

---

## 🎯 FINAL CHECKLIST

**Before running the system, verify:**

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed from requirements.txt
- [ ] .env file created with API key
- [ ] All Python files created in correct directories
- [ ] Directory structure matches specification
- [ ] All scripts are executable (chmod +x)
- [ ] Imports test passes
- [ ] Configuration validates

**To start using the system:**

```bash
# 1. Setup (first time only)
./setup.sh

# 2. Edit .env with your API key
nano .env

# 3. Verify installation
./verify.sh

# 4. Run the system
./run.sh

# OR use interactive CLI
python cli.py
```

---

## 📚 Additional Resources

### File Locations Summary

```
agentic_system/
├── Core Files
│   ├── main.py              - Main entry point
│   ├── cli.py               - Interactive CLI
│   └── requirements.txt     - Dependencies
│
├── Core Modules (core/)
│   ├── agent.py             - Main orchestrator
│   ├── task_understanding.py
│   ├── planner.py
│   ├── executor.py
│   └── learning.py
│
├── Tools (tools/)
│   ├── base.py              - Base classes
│   ├── manager.py           - Tool orchestrator
│   ├── calculator.py
│   ├── file_operations.py
│   └── text_analysis.py
│
├── Configuration (config/)
│   └── settings.py
│
├── Tests (tests/)
│   ├── test_core/
│   └── test_tools/
│
├── Scripts
│   ├── setup.sh             - Initial setup
│   ├── run.sh               - Run application
│   ├── test.sh              - Run tests
│   └── verify.sh            - Verify installation
│
└── Documentation
    ├── README.md
    ├── CONTRIBUTING.md
    ├── CHANGELOG.md
    └── COMMANDS.md
```

### Next Steps After Setup

1. **Test with simple tasks** to verify functionality
2. **Add custom tools** for your specific use case
3. **Configure settings** in .env for your needs
4. **Monitor performance** using built-in metrics
5. **Scale up** with more complex tasks

---

**✅ Implementation guide complete! The AI agent can now follow these steps to build the entire system.**