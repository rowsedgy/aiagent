import os
from google.genai import types

def write_file(working_directory, file_path, content):
    file_abs_path = os.path.join(os.path.abspath(working_directory), file_path)
    if os.path.commonpath([os.path.abspath(file_abs_path), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(file_abs_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create the specified file in the supplied working directory if it doesn't exist and write the supplied content to it. If file exists, overwrite the content instead.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to create or overwrite and write content to. Path is created using working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file."
            )
        },
    ),
)
