import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    file_abs_path = os.path.join(os.path.abspath(working_directory), file_path)
    if os.path.commonpath([os.path.abspath(file_abs_path), os.path.abspath(working_directory)]) != os.path.abspath(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(
            ['python', file_abs_path] + args,
            timeout=30,
            capture_output=True,
            cwd=working_directory,
            text=True
            )
    except Exception as e:
        return f'Error: executing Python file: {e}'

    output = f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}'

    if completed_process.returncode != 0:
        return f'{output}. Process exited with code {completed_process.returncode}'
    else:
        return output
        