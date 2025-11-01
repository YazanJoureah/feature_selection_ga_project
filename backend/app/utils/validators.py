import pandas as pd
import os
from app.utils.error_handlers import APIError

def validate_file(file):
    """Validate uploaded file"""
    if not file or file.filename == '':
        raise APIError("No file provided")
    
    allowed_extensions = {'csv', 'json', 'xlsx', 'xls'}
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_extension not in allowed_extensions:
        raise APIError("Invalid file type. Allowed: CSV, JSON, Excel")
    
    return file_extension

def validate_dataset_content(file_path, file_extension, target_column):
    """Validate dataset content and structure - SIMPLIFIED VERSION"""
    try:
        # Load dataset based on file type
        if file_extension == 'csv':
            df = pd.read_csv(file_path)
        elif file_extension == 'json':
            df = pd.read_json(file_path)
        else:  # Excel files
            df = pd.read_excel(file_path)
        
        # Basic validation
        if df.empty:
            raise APIError("Dataset is empty")
        
        if df.shape[1] < 2:
            raise APIError("Dataset must have at least 2 columns")
        
        if df.shape[0] < 10:
            raise APIError("Dataset must have at least 10 rows")
        
        # Check target column exists
        if target_column not in df.columns:
            available_columns = list(df.columns)
            raise APIError(f"Target column '{target_column}' not found. Available columns: {available_columns}")
        
        return df
        
    except Exception as e:
        raise APIError(f"Invalid dataset file: {str(e)}")