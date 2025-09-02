import os
from .config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    file_abs_path = os.path.join(os.path.abspath(working_directory), file_path)

    if not os.path.isfile(file_abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    if not os.path.abspath(working_directory) in file_abs_path or '../' in file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    with open(file_abs_path, 'r') as f:
        try:
            text = f.read(MAX_CHARS + 1) 
            if len(text) > MAX_CHARS:
                return f'{text} [...File "{file_path}" truncated at 10000 characters]'
            else:
                return text
        except Exception as e:
            return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Show content of specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that contents will be shown of. The file path is constructed using the working directory.",
            ),
        },
    ),
)

    
    

    