"""Persistence module for saving and loading calculator history."""

import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class HistoryPersistence:
    """Handles saving and loading calculator history to/from JSON files."""
    
    def __init__(self, file_path: str = "calculator_history.json"):
        self.file_path = Path(file_path)
    
    def save_history(self, operations: List[Dict[str, Any]]) -> bool:
        """Save operations history to a JSON file."""
        try:
            # Convert datetime objects to strings for JSON serialization
            serializable_ops = []
            for op in operations:
                op_copy = op.copy()
                if 'timestamp' in op_copy and isinstance(op_copy['timestamp'], datetime):
                    op_copy['timestamp'] = op_copy['timestamp'].isoformat()
                serializable_ops.append(op_copy)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_ops, f, indent=2, ensure_ascii=False)
            
            return True
        except (IOError, OSError) as e:
            print(f"Error saving history: {e}")
            return False
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Load operations history from a JSON file."""
        try:
            if not self.file_path.exists():
                return []
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                operations = json.load(f)
            
            # Convert timestamp strings back to datetime objects
            for op in operations:
                if 'timestamp' in op and isinstance(op['timestamp'], str):
                    op['timestamp'] = datetime.fromisoformat(op['timestamp'])
            
            return operations
        except (IOError, OSError, json.JSONDecodeError) as e:
            print(f"Error loading history: {e}")
            return []
    
    def file_exists(self) -> bool:
        """Check if history file exists."""
        return self.file_path.exists()
    
    def delete_file(self) -> bool:
        """Delete the history file."""
        try:
            if self.file_path.exists():
                self.file_path.unlink()
                return True
            return False
        except OSError as e:
            print(f"Error deleting history file: {e}")
            return False
    
    def get_file_size(self) -> int:
        """Get the size of the history file in bytes."""
        if self.file_path.exists():
            return self.file_path.stat().st_size
        return 0
