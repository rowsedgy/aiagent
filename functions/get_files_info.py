import os

def get_files_info(working_directory, directory="."):
    directory_abs_path = os.path.join(os.path.abspath(working_directory), directory)
    if not os.path.isdir(directory_abs_path):
        return f'Error: "{directory}" is not a directory'

    if not os.path.abspath(working_directory) in directory_abs_path or '../' in directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'



    string = f"Results for {'current' if directory == '.' else f'\'{directory}\''} directory"
    for file in os.listdir(directory_abs_path):
        file_path = os.path.join(directory_abs_path, file)
        string += f"\n- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
    
    return string

