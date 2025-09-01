import os

def write_file(working_directory, file_path, content):
    file_abs_path = os.path.join(os.path.abspath(working_directory), file_path)
    if not working_directory in file_abs_path or '../' in file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(file_abs_path, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
        