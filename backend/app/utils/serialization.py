import numpy as np
from typing import Any


def convert_to_serializable(obj: Any) -> Any:
    """
    Convert numpy types and other non-serializable objects to JSON-serializable types
    """
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif hasattr(obj, 'item'):  
        try:
            return obj.item()
        except:
            return str(obj)
    else:
        return obj