from typing import Any, Dict

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries"""
    return {**dict1, **dict2}

def filter_none_values(data: Dict) -> Dict:
    """Remove None values from dictionary"""
    return {k: v for k, v in data.items() if v is not None}