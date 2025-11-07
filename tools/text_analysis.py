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
